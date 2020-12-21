import yaml
import os, uuid
import subprocess
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


def get_blob_count():
    connect_str = get_config('AZURE_STORAGE_CONNECTION_STRING')
    container_name = get_config('IMG_CONTAINER')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    blob_name = [blob.name for blob in blob_list]
    #print(blob_name)
    return blob_name
    # blob_file_name = "sample_img4.png"


# blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_file_name)
# download_file_path = "temp.png"
# with open(download_file_path, "wb") as download_file:
#     download_file.write(blob_client.download_blob().readall())

# return  download_file_path

def get_config(l_key):
    with open("config.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        l_value = data[l_key]

    return l_value


if __name__ == "__main__":
    blob_name_list = get_blob_count()

    if len(blob_name_list) != 0:
        with open("tmp/output.log", "a+") as output:
            for blob_file_name in blob_name_list:
                docker_run_cmd = "docker run -e BLOBNAME={}  -t  veerasan/test-ocrapp:1.1".format(blob_file_name)
                subprocess.call(docker_run_cmd, shell=True, stdout=output,stderr=output)
    else:
        with open("tmp/output.log", "a+") as output:
            output.write("supplier code not found \n")

