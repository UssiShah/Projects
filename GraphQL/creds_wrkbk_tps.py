import tableauserverclient as TSC
import pandas as pd
from credentials import username_prod, password_prod, server_address_prod, sitename, csv_file_path, json_file_path
from wrkbks_creds import WrkbksCreds
from tps_creds import TpsCreds
from datetime import datetime
import csv



# Summary:
# This main script authenticates with Tableau Server, retrieves workbooks and published datasources,
# checks for embedded credentials, and combines the results into a single DataFrame which is then sorted by the owner name.

# Create a Tableau auth object and server object
tableau_auth = TSC.PersonalAccessTokenAuth(username_prod, password_prod, sitename)
server = TSC.Server(server_address_prod, use_server_version=True)

# Sign in to the server
with server.auth.sign_in(tableau_auth):
    # Instantiate the WrkbksCreds and TpsCreds classes via wrkbks_creds and tps_creds objects.
    wrkbks_creds = WrkbksCreds(server)
    tps_creds = TpsCreds(server)

    # Get the data for workbooks and datasources
    workbooks_data = wrkbks_creds.get_workbooks_data()
    datasources_data = tps_creds.get_datasources_data()

    # Combine the data into a single list
    combined_data = workbooks_data + datasources_data
    
    # Create a DataFrame from the combined data
    df = pd.DataFrame(combined_data)

    # Sort the DataFrame by the 'Owner' column
    df_sorted = df.sort_values(by='Owner')

# Display the sorted DataFrame
print(df_sorted)

# Write the sorted DataFrame to a CSV file
now = datetime.now().strftime("%Y%m%d%H%M")
csv_file = f"{csv_file_path}creds_wrkbks_and_tps_{now}.csv"
df_sorted.to_csv(csv_file, index=False, columns=["Type", "Name", "Owner", "Folder", "URL", "Embedded_Credentials"])

print(f"CSV file '{csv_file}' created successfully.")