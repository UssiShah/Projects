import tableauserverclient as TSC

# Summary:
# The TpsCreds class retrieves all published datasources from a Tableau Server and checks if their connections have embedded credentials.
# It returns a list of dictionaries containing datasource details including whether they have embedded credentials.

class TpsCreds:
    def __init__(self, server):
        # Initialize with a Tableau Server instance
        self.server = server

    def get_datasources_data(self):
        datasources_data = []

        # Create a dictionary to map user IDs to user objects for easy lookup
        users_dict = {user.id: user for user in TSC.Pager(self.server.users)}

        # Retrieve all datasources using pagination
        req_option = TSC.RequestOptions(pagesize=1000)
        all_datasources = list(TSC.Pager(self.server.datasources, req_option))

        # Iterate through each datasource
        for datasource in all_datasources:
            # Populate the connections for the current datasource
            self.server.datasources.populate_connections(datasource)
            has_embedded_credentials = True
            # Check if any connection has embedded credentials
            for connection in datasource.connections:
                if connection.embed_password == False:
                    has_embedded_credentials = False
                    break
            # Get the full name of the owner using the user dictionary
            owner_name = users_dict[datasource.owner_id].fullname
            # Construct the URL for the datasource
            # datasource_url = f"{self.server.baseurl}/#/site/{self.server.site_id}/datasources/{datasource.id}"

            # Directly fetch the URL. (TSC is buggy as of now because datasource.webpage_url returns a null. See progress here: https://github.com/tableau/server-client-python/issues/1310)
            datasource_url = datasource.webpage_url
            # Append the datasource details to the list
            datasources_data.append({
                'Type': 'Datasource',
                'Name': datasource.name,
                'Owner': owner_name,
                'Folder': datasource.project_name,
                'URL': datasource_url,  
                'Embedded_Credentials': 'Yes' if has_embedded_credentials else 'No'
            })

        # Return the list of datasource details
        return datasources_data
