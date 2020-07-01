# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, request, jsonify, helpers
from loguru import logger
from pathlib import Path
import base64
from PIL import Image, ImageOps
from io import BytesIO
from datetime import *
from flask_api import status
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'



@app.route('/')
def hello():
    print("say")
    return 'hello'

"""
{
    "background": "2-1.png"
    "images": [
        {
            "image": "base64xxxxxx",
            "uid": "xxxxxx"
        },
        {
            "image": "base64xxxxxx",
            "uid": "xxxxxx"
        }
    ]
}
"""
@app.route("/getImage", methods=['POST'])
def getImage():
    if request.method != 'POST':
        return make_response(jsonify({'result': 'invalid method'}), 400)

    seq = str(datetime.now()).replace('-','.').replace(' ','.').replace(':','.')
    req = request.get_json()

    image_path_list = []
    if "background" in req:
        background = req["background"]
    else:
        err = 'Not found background field'
        logger.error(err)
        return make_response(jsonify({'result': err}), 400)
    try:
        for field in req["images"]:
            base64_png = field['image']
            uid = field['uid']
            code = base64.b64decode(base64_png.split(',')[1])
            image_decoded = Image.open(BytesIO(code))
            image_path = Path(app.config['UPLOAD_FOLDER']) / '{0}-{1}.png'.format(seq, uid)
            image_path_list.append(image_path)
            image_decoded.save(image_path)
    except Exception as e:
        logger.error(f"Failed to parse, {e}")
        return make_response(jsonify({'error': str(e)})), status.HTTP_500_INTERNAL_SERVER_ERROR

    converted_image_path = convert_image(image_path_list, background)
    converted_image_url = get_image_url(converted_image_path)

    return make_response(jsonify({'result': 'success', 'image_url': converted_image_url}))


@app.route("/list", methods=['GET'])
def get_image_list():
    if request.method != 'GET':
        return make_response(jsonify({'result': 'invalid method'}), 400)
    image_list = [file_path.split("/")[-1] for file_path in os.listdir("images/convert")]
    image_list.sort(reverse=True)

    image_list_distinct = []
    image_list_distinct = [image for image in image_list if image.split(".")[-1] == "png"]

    return make_response(jsonify({'image': [image_list_distinct]}))


@app.route("/image/<name>", methods=["GET"])
def get_image_data(name):
    if request.method != 'GET':
        return make_response(jsonify({'result': 'invalid method'}), 400)
    pil_img = Image.open(f"images/convert/{name}")
    return serve_pil_image(pil_img)



def serve_pil_image(pil_img):
    bytes_io = BytesIO()
    pil_img.save(bytes_io, "png")
    response = helpers.make_response(bytes_io.getvalue())
    response.headers["Content-type"] = "Image"
    return response


def convert_image(image_path_list, background, background_image_path="images/background"):
    background_image = Image.open(os.path.join(background_image_path, background))
    image_list = [Image.open(image_path) for image_path in image_path_list]
    for image in image_list:
        background_image.paste(image, mask=image)

    seq = str(datetime.now()).replace('-','.').replace(' ','.').replace(':','.')
    converted_image_path = f"images/convert/{seq}.png"

    background_image = ImageOps.mirror(background_image)
    background_image.save(converted_image_path)
    return converted_image_path


def get_image_url(converted_image_path):
    converted_image_url = None
    return converted_image_url


if __name__ == '__main__':
    app.run(host=os.getenv('APP_ADDRESS', '0.0.0.0'), port=9000, debug=True)
