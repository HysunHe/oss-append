import cv2
import numpy as np
import base64
import requests

def file_to_numpy(path_file):
    image_np = cv2.imread(path_file)
    return image_np

def numpy_to_base64(image_np):
    data = cv2.imencode('.jpg', image_np)[1]
    image_bytes = data.tobytes()
    image_base4 = base64.b64encode(image_bytes).decode('utf8')
    return image_base4

def upload_json_with_binary(url, json_data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=json_data)
    
    if response.status_code == 200:
        print(response.json())
    else:
        print('Bad')


# 加载图片
image_np = file_to_numpy('/home/hysunhe/projects/aijianvideo/goodgoodstudy.jpg')
# 转换成字节，并用base64编码
binary_data_base64 = numpy_to_base64(image_np)
# 调用API
json_data = {
    "bucket": "test", 
    "name":"myimage1.jpg",
    "position": 25526,
    "content": binary_data_base64,
    "append": "0"
}
upload_json_with_binary('http://158.178.240.219:5000/write-json', json_data)