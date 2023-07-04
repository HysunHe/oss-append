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

upload_url = 'http://132.226.236.106:5000/write-bytes?bucket=Hysun_DianJiang&name=testcase3/test1.bin&position=-1&append=0&destination=testcase3/test1.bin'

upload_binary_data(upload_url, binary_data)
