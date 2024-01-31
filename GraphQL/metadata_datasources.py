import json
import csv
import tableauserverclient as TSC
from credentials import username_prod, password_prod, server_address_prod, sitename, csv_file_path, json_file_path
from datetime import datetime

def main():
    query1 = """
    {
        publishedDatasources {
            projectName
            name
            upstreamTables {
                name
                schema
                fullName
                connectionType
                database {
                    name
                }
            }
        }
    }
    """

    query2 = """
    {
        embeddedDatasources {
            name
            upstreamTables {
                name
                schema
                fullName
                connectionType
                database {
                    name
                }
            }
            downstreamWorkbooks {
                name
                projectName
            }
        }
    }
    """

    tableau_auth = TSC.PersonalAccessTokenAuth(username_prod, password_prod, sitename)
    server = TSC.Server(server_address_prod, use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        # Query the Metadata API and store the response in resp
        resp1 = server.metadata.query(query1)
        published_datasources = resp1['data']['publishedDatasources']

        resp2 = server.metadata.query(query2)
        embedded_datasources = resp2['data']['embeddedDatasources']

        # Combine both types of datasources into one list
        datasources = []
        for published_ds in published_datasources:
            datasources.append({
                'DatasourceType': 'Published Datasource',
                'Datasource': published_ds
            })
        for embedded_ds in embedded_datasources:
            datasources.append({
                'DatasourceType': 'Embedded Datasource',
                'Datasource': embedded_ds
            })

        # Generate unique file names with timestamps
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        json_file = json_file_path + f'datasources_{timestamp}.json'
        csv_file = csv_file_path + f'datasources_{timestamp}.csv'

        # Write datasources data to JSON file
        with open(json_file, 'w') as output_file:
            json.dump(datasources, output_file, indent=4)

        # Extracting relevant information from the JSON data
        csv_data = []
        for ds in datasources:
            datasource_type = ds['DatasourceType']
            datasource = ds['Datasource']
            for table in datasource['upstreamTables']:
                if datasource_type == 'Embedded Datasource':
                    workbook_name = datasource['downstreamWorkbooks'][0]['name'] if 'downstreamWorkbooks' in datasource and datasource['downstreamWorkbooks'] else ''
                    project_name = datasource['downstreamWorkbooks'][0]['projectName'] if 'downstreamWorkbooks' in datasource and datasource['downstreamWorkbooks'] else ''
                else:
                    workbook_name = ''
                    project_name = datasource['projectName'] if 'projectName' in datasource else ''
                csv_data.append({
                    'DatasourceType': datasource_type,
                    'DatasourceName': datasource['name'],
                    'TableName': table['name'],
                    'Schema': table['schema'],
                    'FullName': table['fullName'],
                    'ConnectionType': table['connectionType'],
                    'DatabaseName': table['database']['name'],
                    'WorkbookName': workbook_name,
                    'ProjectName': project_name
                })

        # Write data to CSV file
        field_names = ['DatasourceType', 'DatasourceName', 'TableName', 'Schema', 'FullName', 'ConnectionType', 'DatabaseName', 'WorkbookName', 'ProjectName']
        with open(csv_file, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
            csv_writer.writeheader()
            csv_writer.writerows(csv_data)

        print(f'JSON file saved to {json_file}')
        print(f'CSV file saved to {csv_file}')

if __name__ == '__main__':
    main()
