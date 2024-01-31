import json
import csv
from credentials import username_prod, password_prod, server_address_prod, sitename, csv_file_path, json_file_path
from datetime import datetime
import tableauserverclient as TSC

def main():
    query1 = """
    {
      embeddedDatasources {
        workbook {
          id
          name
          projectName
          owner {
            name
          }
        }
        name
        hasUserReference
      }
    }
    """

    tableau_auth = TSC.PersonalAccessTokenAuth(username_prod, password_prod, sitename)
    server = TSC.Server(server_address_prod, use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        # Query the Metadata API and store the response in resp1
        resp1 = server.metadata.query(query1)
        embedded_datasources = resp1['data']['embeddedDatasources']

        # Generate a unique file name with a timestamp for embedded datasources
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        json_file = json_file_path + f'sources_with_user_ref{timestamp}.json'
        csv_file = csv_file_path + f'sources_with_user_ref{timestamp}.csv'

        # Write embedded datasources data to JSON file
        with open(json_file, 'w') as output_file:
            json.dump(embedded_datasources, output_file, indent=4)

        # Extracting relevant information from the JSON data
        csv_data = []
        for datasource in embedded_datasources:
            workbook = datasource['workbook']
            owner = workbook['owner']

            csv_data.append({
                'WorkbookID': workbook['id'],
                'WorkbookName': workbook['name'],
                'ProjectName': workbook['projectName'],
                'OwnerName': owner['name'],
                'DatasourceName': datasource['name'],
                'HasUserReference': datasource['hasUserReference'],
            })

        # Write data to CSV file
        field_names = ['WorkbookID', 'WorkbookName', 'ProjectName', 'OwnerName', 'DatasourceName', 'HasUserReference']
        with open(csv_file, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
            csv_writer.writeheader()
            csv_writer.writerows(csv_data)

        print(f'JSON file saved to {json_file}')
        print(f'CSV file saved to {csv_file}')

if __name__ == '__main__':
    main()
