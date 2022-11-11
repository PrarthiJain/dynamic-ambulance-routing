import random
import string
import time
from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential
from itertools import cycle
from azure.storage.blob import BlobServiceClient

account_name = 'cs5412storage'
account_url = "https://cs5412storage.blob.core.windows.net"
account_key = 'aHag2cwNa6fY3EEy2V9z6LvI8/vmAWK8l7M2cHFbPMf/PdptJ6zXjeEBdxdvZ0jKqiliU8Y4fN77+AStoacOvA=='
connection_string = 'DefaultEndpointsProtocol=https;AccountName=cs5412storage;AccountKey=aHag2cwNa6fY3EEy2V9z6LvI8/vmAWK8l7M2cHFbPMf/PdptJ6zXjeEBdxdvZ0jKqiliU8Y4fN77+AStoacOvA==;EndpointSuffix=core.windows.net'
default_credential = DefaultAzureCredential()
copy_from_container = 'source-container'
copy_to_container = 'newcontainer'


def copy_azure_files(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    source_blob = (f"https://{account_name}.blob.core.windows.net/{copy_from_container}/{blob_name}")
    # Target
    suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
    target_blobname = f"{suffix}-{blob_name}"
    copied_blob = blob_service_client.get_blob_client(copy_to_container, target_blobname)
    copied_blob.start_copy_from_url(source_blob)


files = []
files_loop = cycle(files)

container = ContainerClient.from_connection_string(conn_str=connection_string, container_name=copy_from_container)
for blob in container.list_blobs():
    files.append(blob.name)

for file in files_loop:
    copy_azure_files(file)
    time.sleep(1)
