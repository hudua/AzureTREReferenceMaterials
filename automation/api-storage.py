
# need to run Az Login first
#command line: az login --tenant 7aa7ddbc-6504-4dc8-a6e4-ff73df71c91d

#library is pip install azure-storage-file-datalake
#will need to install Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli

import sys

filesystem_name = 'genomics'

from azure.storage.filedatalake import DataLakeServiceClient

# Instantiate a DataLakeServiceClient Azure Identity credentials.
# [START create_datalake_service_client_oauth]
from azure.identity import AzureCliCredential 
token_credential = AzureCliCredential()
datalake_service_client = DataLakeServiceClient("https://{}.dfs.core.windows.net".format("datalakestoragesharedtre"),
                                                credential=token_credential)

file_system_client = datalake_service_client.get_file_system_client(file_system=filesystem_name)
directory_client = file_system_client.get_directory_client(".")
file_client = directory_client.get_file_client("uploaded-file.txt")
local_file = open("compute.yml",'r')
file_contents = local_file.read()
file_client.upload_data(file_contents, overwrite=True)
