# from flask import Flask, request, jsonify
import pytesseract
import cv2
from pytesseract import Output
# import re
from config import get_config
import os, uuid, time, json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


# app = Flask(__name__)

blob_file_name = os.getenv('BLOBNAME')
connect_str = get_config('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


def download_blob_data():
    container_name_download = get_config('IMG_CONTAINER')
    container_name_backup = get_config('IMG_BACKUP_CONTAINER')
    temp_file_name = get_config('TEMP_FILENAME')
    blob_client_download = blob_service_client.get_blob_client(container=container_name_download, blob=blob_file_name)
    blob_client_backup = blob_service_client.get_blob_client(container=container_name_backup, blob=blob_file_name)

    with open(temp_file_name, "wb") as download_file:
        download_file.write(blob_client_download.download_blob().readall())

    blob_client_backup.start_copy_from_url(blob_client_download.url)
    blob_client_download.delete_blob()
    return temp_file_name


def upload_blob_data(p_result):
    result_dict = {}
    container_name = get_config('RESULT_CONTAINER')
    transaction_id = blob_file_name.split(".")[0]
    local_file_name = transaction_id + str(uuid.uuid4()) + ".json"
    txn_date_time = time.strftime("%d-%m-%Y-%H%M%S"+" GMT")
    result_dict['transaction_id'] = transaction_id
    result_dict['supplier_code'] = p_result[0]
    result_dict['transaction_date_time'] = txn_date_time
    with open(local_file_name, 'w') as outfile:
        json.dumps(result_dict, outfile, indent=4)
        outfile.close()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    with open(local_file_name, "rb") as data:
        blob_client.upload_blob(data)


def ocr_core():
    """
    This function will handle the core OCR processing of images.
    """
    supplier_code = ["M0086", "P1566"]
    l_result = []
    download_file_path = download_blob_data()
    img_cv = cv2.imread(download_file_path)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img_rgb, lang='eng', output_type=Output.DICT)
    for l_value in boxes['text']:
        if l_value in supplier_code:
            # if len(l_value) > 4 and re.search("^[A-Z]",l_value):
            l_result.append(l_value)

    os.remove(download_file_path)
    #upload_blob_data(l_result)
    #print(l_value)

    if len(l_result) == 0:
        pass
    else:
        upload_blob_data(l_result)


if __name__ == '__main__':
    ocr_core()
