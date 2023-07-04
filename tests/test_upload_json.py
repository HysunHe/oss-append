""" Hysun He (hysun.he@oracle.com) @ 2023/07/04 """
import requests
import base64

def upload_json_with_binary(url, json_data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=json_data)
    
    if response.status_code == 200:
        print('Good')
    else:
        print('Bad')

binary_data = bytes('data to be encoded: 你好', 'utf-8')

json_data = {
    "bucket": "Hysun_DianJiang", 
    "name":"testcase4/test2.txt",
    "position": -1,
    "content": base64.b64encode(binary_data).decode(encoding='utf-8'),
    "destination": "testcase4/test2.txt",
    "append": "0"
}

upload_url = 'http://132.226.236.106:5000/write-json'

upload_json_with_binary(upload_url, json_data)
