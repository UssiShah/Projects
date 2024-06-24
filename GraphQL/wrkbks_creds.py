import tableauserverclient as TSC

# Summary:
# The WrkbksCreds class retrieves all workbooks from a Tableau Server and checks if their connections have embedded credentials.
# It returns a list of dictionaries containing workbook details including whether they have embedded credentials.

class WrkbksCreds:
    def __init__(self, server):
        # Initialize with a Tableau Server instance
        self.server = server

    def get_workbooks_data(self):
        workbooks_data = []

        # Create a dictionary to map user IDs to user objects for easy lookup
        users_dict = {user.id: user for user in TSC.Pager(self.server.users)}

        # Retrieve all workbooks using pagination
        req_option = TSC.RequestOptions(pagesize=1000)
        all_workbooks = list(TSC.Pager(self.server.workbooks, req_option))

        # Iterate through each workbook
        for workbook in all_workbooks:
            # Populate the connections for the current workbook
            self.server.workbooks.populate_connections(workbook)
            embedded_credentials = True
            # Check if any connection has embedded credentials
            for connection in workbook.connections:
                if not connection.embed_password:
                    embedded_credentials = False
                    break
            # Get the full name of the owner using the user dictionary
            owner_name = users_dict[workbook.owner_id].fullname
            # Append the workbook details to the list
            workbooks_data.append({
                'Type': 'Workbook',
                'Name': workbook.name,
                'Owner': owner_name,
                'Folder': workbook.project_name,
                'URL': workbook.webpage_url,
                'Embedded_Credentials': 'Yes' if embedded_credentials else 'No'
            })

        # Return the list of workbook details
        return workbooks_data
