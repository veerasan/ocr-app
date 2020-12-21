from flask import Flask, request, jsonify
import pytesseract
import cv2
from pytesseract import Output
# import re
import yaml
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


app = Flask(__name__)

blob_file_name = os.getenv('BLOBNAME')
#blob_file_name = "sample_img2.png"

def get_blob_data():
    connect_str = get_config('AZURE_STORAGE_CONNECTION_STRING')
    container_name = get_config('IMG_CONTAINER')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    #blob_file_name = "sample_img4.png"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_file_name)
    download_file_path = "temp.png"
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

    return  download_file_path

def get_config(l_key):
    with open("config.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        l_value = data[l_key]

    return l_value


def ocr_core():
    """
    This function will handle the core OCR processing of images.
    """
    supplier_code = ["M0086", "P1566"]
    l_result = []
    #download_file_path = "temp.png"
    download_file_path = get_blob_data()
    img_cv = cv2.imread(download_file_path)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img_rgb, lang='eng', output_type=Output.DICT)
    for l_value in boxes['text']:
        if l_value in supplier_code:
            # if len(l_value) > 4 and re.search("^[A-Z]",l_value):
            l_result.append(l_value)

    os.remove(download_file_path)
    return l_result


@app.route('/')
def index():
    #get_blob_data()
    result = ocr_core()
    return jsonify({"supplier_code": result})
