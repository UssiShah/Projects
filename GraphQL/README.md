### README.md

## Tableau Credentials

This folder contains three Python scripts designed to interact with Tableau Server, retrieve workbook and datasource information, check for embedded credentials, and compile this data into a CSV file. Below is a summary of each file and instructions on how to use them.

### File Summaries

#### 1. `wrkbks_creds.py`

- **Summary:**
  The `WrkbksCreds` class retrieves all workbooks from Tableau Server and checks if their connections have embedded credentials. It returns a list of dictionaries containing workbook details, including whether they have embedded credentials. 
  - Note: for workbooks that contain several connections, it will return 'Yes' in 'Embedded credentials' column ONLY if all of the connections have embedded credentials. If one or more of the connections do not have embedded credentials it will return a 'No'.

- **Key Functions:**
  - `__init__(self, server)`: Initializes with a Tableau Server instance.
  - `get_workbooks_data(self)`: Retrieves all workbooks, checks for embedded credentials, and returns a list of workbook details.

#### 2. `tps_creds.py`

- **Summary:**
  The `TpsCreds` class retrieves all published datasources from Tableau Server and checks if their connections have embedded credentials. It returns a list of dictionaries containing datasource details, including whether they have embedded credentials.
  - Note: for published datasources that contain several connections, it will return 'Yes' in 'Embedded credentials' column ONLY if all of the connections have embedded credentials. If one or more of the connections do not have embedded credentials it will return a 'No'.

- **Key Functions:**
  - `__init__(self, server)`: Initializes with a Tableau Server instance.
  - `get_datasources_data(self)`: Retrieves all datasources, checks for embedded credentials, constructs the URL for the datasource, and returns a list of datasource details.


#### 3. `creds_wrkbk_tps.py`

- **Summary:**
  This main script authenticates with Tableau Server, retrieves workbooks and published datasources, checks for embedded credentials, and combines the results into a single DataFrame, which is then sorted by the owner name and written to a CSV file.

- **Key Steps:**
  - Authenticates with Tableau Server.
  - Instantiates `WrkbksCreds` and `TpsCreds` classes.
  - Retrieves data for workbooks and datasources.
  - Combines and sorts the data.
  - Writes the data to a CSV file.

### Instructions on How to Use

1. **Set Up Your Environment:**
   - Ensure you have Python and the `tableauserverclient` library installed.
   - Store your Tableau Server credentials in a file named `credentials.py` in the parent directory. The file should define the following variables:
     ```python
     username_prod = 'your_username'
     password_prod = 'your_password'
     server_address_prod = 'your_server_address'
     sitename = 'your_sitename'
     csv_file_path = 'path_to_save_csv/'
     json_file_path = 'path_to_save_json/'
     ```

2. **Run the Main Script:**
   - Navigate to the directory containing the scripts.
   - Run the `creds_wrkbk_tps.py` script:
     ```bash
     python creds_wrkbk_tps.py
     ```

3. **Output:**
   - The script will generate a CSV file containing details of workbooks and datasources, including whether they have embedded credentials. The file will be saved to the path specified in `csv_file_path` with a timestamped filename.

### Additional Information

- **Dependencies:**
  - Python 3.x
  - `tableauserverclient` library

- **Notes:**
  - Ensure the Tableau Server API is accessible from your environment.
  - The `datasource.webpage_url` may return null due to a known bug. You can manually construct the URL as a workaround.
  - Adjust the scripts as necessary to match your Tableau Server configuration and requirements.

This setup will help you automate the retrieval of workbook and datasource information from Tableau Server, check for embedded credentials, and save the results in a structured format.