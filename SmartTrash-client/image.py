from time import sleep
import urllib.request
import urllib.parse
import sys
import ssl
import json
import base64
import io
import string
from PIL import Image
import APIKey
try:
    import picamera
except:
    print('cant import picamera')

access_token = ''
image = None
camera = None
result = json

def token():
    global access_token
    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % (
        APIKey.client_id, APIKey.client_secret)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    request = urllib.request.Request(host, headers=headers)
    content = urllib.request.urlopen(request).read().decode("utf-8")
    tokenjson = json.loads(content)
    access_token = tokenjson['access_token']
    print(access_token)  # debug
    return access_token


def image_classify(img):
    global access_token
    global result
    if access_token == '':
        token()
    host = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token=%s" % (
        access_token)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'image': image_to_base64(img),
        'baike_num': 5
    }
    data = urllib.parse.urlencode(data).encode()
    request = urllib.request.Request(host, headers=headers, data=data)
    content = urllib.request.urlopen(request).read().decode("utf-8")
    result = json.loads(content)
    print(content)  # debug
    print(result['result'][0]['keyword'])
    return result


def take():
    global image
    global camera
    stream = io.BytesIO()
    try:
        if camera == None:
            camera = picamera.PiCamera()
        camera.start_preview(fullscreen=False,window=(213, 0, 854, 480))
        # Camera warm-up time
        sleep(2)
        camera.capture(stream, format='jpeg')
    finally:
        camera.close()
        camera=None
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    image = Image.open(stream)
    image.save('/tmp/image.jpg')  # debug
    return image


def get():
    global image
    image = Image.open('/tmp/image.jpg')
    return image


def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def getType(name):
    host = urllib.parse.quote(APIKey.type_host+name, safe=string.printable)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    request = urllib.request.Request(host, headers=headers)
    content = urllib.request.urlopen(request).read().decode("utf-8")
    print(content)  # debug
    return content