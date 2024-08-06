import tableauserverclient as TSC
import requests
import json
import csv
from datetime import datetime, timedelta
from credentials import username_prod, password_prod, server_address_prod, sitename, csv_file_path

# Create a Tableau auth object and server object using username and password
tableau_auth = TSC.PersonalAccessTokenAuth(username_prod, password_prod, sitename)
server = TSC.Server(server_address_prod, use_server_version=True)

with server.auth.sign_in(tableau_auth):

    workbooks_data = []

    # Retrieve all workbooks using pagination
    req_option = TSC.RequestOptions(pagesize=1000)
    all_workbooks = list(TSC.Pager(server.workbooks, req_option))

    # Iterate through each workbook
    for workbook in all_workbooks:

        # Populate the views for the current workbook with usage statistics
        usage_options = TSC.RequestOptions()
        usage_options.usage = True
        server.workbooks.populate_views(workbook, usage_options)

        # Add workbook data to the list
        workbooks_data.append({
            'id': workbook.id,
            'name': workbook.name,
            'project_name': workbook.project_name,
            'owner': server.users.get_by_id(workbook.owner_id).fullname,
            'updated_at': workbook.updated_at,
            'views': [{
                'view': view.name,
                'total_views': view.total_views
            } for view in workbook.views]
        })

    # Write data to CSV file
    headers = ["Workbook ID", "Workbook Name", "Project Name", "Owner", "Updated At", "View Name", "Total Views"]
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file = f"{csv_file_path}wrkbks_usage_{now}.csv"

# Workbook.owner_username is not populated by default, so we need to find a workaround
# by p

    with open(csv_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for workbook in workbooks_data:
            for view in workbook['views']:
                writer.writerow({
                    "Workbook ID": workbook['id'],
                    "Workbook Name": workbook['name'],
                    "Project Name": workbook['project_name'],
                    "Owner": workbook['owner'],
                    "Updated At": workbook['updated_at'],
                    "View Name": view['view'],
                    "Total Views": view['total_views']
                })

    print(f"CSV file '{csv_file}' created successfully.")