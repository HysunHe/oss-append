import cv2
import numpy as np
import base64
import requests

def upload_json_with_binary(url, json_data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, headers=headers, json=json_data)
    
    if response.status_code == 200:
        print(response.json())
    else:
        print('Bad')

def file_to_base64(path_file):
    with open(path_file,'rb') as f:
        image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf8')
        return image_base64

binary_data_base64 = file_to_base64('/home/hysunhe/projects/aijianvideo/video1.mp4')
# 调用API
json_data = {
    "bucket": "Hysun_Bucket", 
    "name":"video88.mp4",
    "position": 0,
    "content": binary_data_base64,
    "append": "1"
}
upload_json_with_binary('http://localhost:5000/append-mp4-json', json_data)