#Download and learn about Azcopy here: https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10

azcopy login --tenant-id=[tenant-id]
azcopy copy './<file-name>.csv' 'https://datalakestoragesharedtre.dfs.core.windows.net/genomics/<file-name>.csv'
