import requests

def file_to_bytes(path_file):
    with open(path_file,'rb') as f:
        image_bytes = f.read()
        return image_bytes

def upload_binary_data(url, data):
    response = requests.post(url=url, data=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print('Bad')

binary_data = file_to_bytes('/home/hysunhe/projects/aijianvideo/video1.mp4')
# 调用API
upload_url = 'http://localhost:5000/append-mp4?bucket=Hysun_Bucket&name=video11.mp4&append=1'
upload_binary_data(upload_url, binary_data)