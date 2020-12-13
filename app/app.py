from flask import Flask, request, jsonify
import pytesseract
import cv2
from pytesseract import Output
#import re

app = Flask(__name__)


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    supplier_code = ["M0086", "P1566"]
    l_result = []
    img_cv = cv2.imread(filename)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img_rgb, lang='eng', output_type=Output.DICT)
    for l_value in boxes['text']:
        if l_value in supplier_code:
            # if len(l_value) > 4 and re.search("^[A-Z]",l_value):
            l_result.append(l_value)

    return l_result


@app.route('/')
def index():
    result = ocr_core('inputdata/sample_img2.png')
    return jsonify({"supplier_code": result})

