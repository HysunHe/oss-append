import cv2
import numpy as np
import base64
import requests

def file_to_numpy(path_file):
    image_np = cv2.imread(path_file)
    return image_np

def numpy_to_bytes(image_np):
    data = cv2.imencode('.jpg', image_np)[1]
    image_bytes = data.tobytes()
    return image_bytes

def upload_binary_data(url, data):
    response = requests.post(url=url, data=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print('Bad')

# 加载图片
image_np = file_to_numpy('/home/hysunhe/projects/aijianvideo/micro_tx.jpg')
# 转换成字节，并用base64编码
binary_data = numpy_to_bytes(image_np)
# 调用API
upload_url = 'http://158.178.240.219:5000/write-bytes?bucket=test&name=bytesimage.jpg&position=531327&append=0'
upload_binary_data(upload_url, binary_data)