""" Hysun He (hysun.he@oracle.com) @ 2023/07/04 """
import requests
import base64

def upload_json_with_binary(url, json_data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=json_data)
    # print(response.content)
    if response.status_code == 200:
        print(response.json())
    else:
        print('Bad')

binary_data = bytes('data to be encoded: 你好, ya', 'utf-8')
json_data = {
    "bucket": "test", 
    "name":"json.bin.1",
    "position": 60,
    "content": base64.b64encode(binary_data).decode(encoding='utf-8'),
    "append": "1"
}
# upload_url = 'http://132.226.236.106:5000/write-json'
upload_url = 'http://158.178.240.219:5000/write-json'
upload_json_with_binary(upload_url, json_data)
