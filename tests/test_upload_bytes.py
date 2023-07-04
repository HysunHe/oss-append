""" Hysun He (hysun.he@oracle.com) @ 2023/07/04 """
import requests

def upload_binary_data(url, data):
    response = requests.post(url=url, data=data)
    print(response.content)
    
    if response.status_code == 200:
        print(response.json())
    else:
        print('Bad')

binary_data = bytes('data to be encoded: 你好, ha', 'utf-8')

upload_url = 'http://localhost:5000/write-bytes?bucket=Hysun_DianJiang&name=demo3.bin&position=90&append=0'

upload_binary_data(upload_url, binary_data)
