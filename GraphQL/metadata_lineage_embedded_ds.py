# This script maps the lineage of fields downstream of workbooks.
# If a field is being used in a worksheet, it will be taken into account. 
# All filters, calculated fields, etc are considered at a workbook level. 
# ... 

#### Usage:
#### Make sure to update 'tables_list' with the database tables you want to consider. 

import json
import csv
import tableauserverclient as TSC
from credentials import username_prod, password_prod, server_address_prod, sitename, csv_file_path, json_file_path
from datetime import datetime
import time

def main():
    
    start_time = time.time()

    # List of tables to iterate over
    tables_list = []
    

    # Tableau Server authentication
    tableau_auth = TSC.PersonalAccessTokenAuth(username_prod, password_prod, sitename)
    server = TSC.Server(server_address_prod, use_server_version=True)

    # List to store all rows
    all_rows = []

    for table_name in tables_list:
        # GraphQL query with variables for pagination
        query1 = f"""
        query fields($first: Int, $offset: Int) {{
          databases(filter: {{name: "SMSBI"}}) {{
            tables(filter: {{nameWithin: ["{table_name}"]}}) {{
              fullName
              schema
              database {{
                name
              }}
              downstreamSheetsConnection(first: $first, offset: $offset) {{
                totalCount
                nodes {{
                  name
                  containedInDashboards {{
                    name
                  }}
                  workbook {{
                    name
                    owner {{
                      name
                    }}
                  }}
                  parentEmbeddedDatasources {{
                    name
                    hasUserReference
                    datasourceFilters {{
                      field {{
                        name
                      }}
                    }}
                  }}
                  datasourceFields {{
                    name
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        with server.auth.sign_in(tableau_auth):
            # Initialize variables for pagination
            first = 100  # Adjust as needed
            offset = 0
            total_nodes = float('inf')

            while offset < total_nodes:
                # Execute the GraphQL query with current pagination variables
                resp1 = server.metadata.query(query1, variables={'first': first, 'offset': offset})
                databases = resp1['data']['databases']
                tables = databases[0]['tables']
                downstream_sheets_connection = tables[0]['downstreamSheetsConnection']

                # Retrieve nodes, total count, and offset
                nodes = downstream_sheets_connection['nodes']
                total_nodes = downstream_sheets_connection['totalCount']

                # Extracting relevant information from the nodes
                for sheet in nodes:
                    datasource_filters = sheet.get('parentEmbeddedDatasources', [])[0].get('datasourceFilters', [])
                    datasource_fields = sheet['datasourceFields']

                    for field in datasource_fields:
                        # Append data to the list for each field
                        all_rows.append({
                            'DatabaseName': tables[0]['database']['name'],
                            'TableName': tables[0]['fullName'],
                            'Schema': tables[0]['schema'],
                            'SheetName': sheet['name'],
                            'WorkbookName': sheet['workbook']['name'],
                            'WorkbookOwner': sheet['workbook']['owner']['name'],
                            'ContainedInDashboard': sheet['containedInDashboards'][0]['name'] if sheet['containedInDashboards'] else '',
                            'ParentEmbeddedDatasource': sheet['parentEmbeddedDatasources'][0]['name'] if sheet['parentEmbeddedDatasources'] else '',
                            'HasUserReference': sheet['parentEmbeddedDatasources'][0]['hasUserReference'] if sheet['parentEmbeddedDatasources'] else '',
                            'DatasourceFilters': ', '.join([filter['field']['name'] for filter in datasource_filters]),
                            'DatasourceFields': field['name']
                        })

                # Increment offset for the next pagination
                offset += first

    # Generate a unique file name with a timestamp for downstream data
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    json_file = json_file_path + f'downstream_data_all_tables_expanded_{timestamp}.json'
    csv_file = csv_file_path + f'downstream_data_all_tables_expanded_{timestamp}.csv'

    # Write downstream data to JSON file
    with open(json_file, 'w') as output_file:
        json.dump(all_rows, output_file, indent=4)

    # Write data to CSV file
    field_names = ['DatabaseName', 'TableName', 'Schema', 'SheetName', 'WorkbookName', 'WorkbookOwner',
                   'ContainedInDashboard', 'ParentEmbeddedDatasource', 'HasUserReference', 'DatasourceFilters',
                   'DatasourceFields']
    with open(csv_file, 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
        csv_writer.writeheader()
        csv_writer.writerows(all_rows)
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f'JSON file saved to {json_file}')
    print(f'CSV file saved to {csv_file}')
    print(f"Script execution time: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    main()
