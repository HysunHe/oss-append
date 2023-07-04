""" Hysun He (hysun.he@oracle.com) @ 2023/07/04 """
import requests

def upload_binary_data(url, data):
    response = requests.post(url=url, data=data)
    
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        print('Good')
    else:
        print('Bad')


binary_data = bytes('data to be encoded: 你好', 'utf-8')

upload_url = 'http://localhost:5000/write-bytes?name=write_bytes.bin&position=0&append=true'

upload_binary_data(upload_url, binary_data)
