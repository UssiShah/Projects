import csv
import tableauserverclient as TSC
from credentials import username_prod, password_prod, server_address_prod, sitename, csv_file_path
from datetime import datetime

tableau_auth = TSC.PersonalAccessTokenAuth(username_prod, password_prod, sitename)
server = TSC.Server(server_address_prod, use_server_version=True)

with server.auth.sign_in(tableau_auth):
    groups_data = []

    # Get all user groups
    request_options = TSC.RequestOptions(pagesize=1000)
    all_groups = list(TSC.Pager(server.groups, request_options))

    for group in all_groups:
        # Retrieve users within each group
        server.groups.populate_users(group)
        for user in group.users:
            # Store group and user information
            group_info = {
                "Group ID": group.id,
                "Group Name": group.name,
                "User Name": user.name,
                "User ID": user.id,
                "Email": user.email,
                "Last Login": user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "Never logged in"
            }
            groups_data.append(group_info)

    # Write data to a CSV file
    headers = ["Group ID", "Group Name", "User Name", "User ID", "Email", "Last Login"]
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file = f"{csv_file_path}user_groups_{now}.csv"

    with open(csv_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for data in groups_data:
            writer.writerow(data)

    print(f"CSV file '{csv_file}' created successfully.")

