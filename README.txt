Upload with JSON payload:
-------------------------------
binary_data = bytes('data to be encoded: 你好, ya', 'utf-8')
json_data = {
    "bucket": "test", 
    "name":"json.bin.1",
    "position": 60,
    "content": base64.b64encode(binary_data).decode(encoding='utf-8'),
    "append": "1"  # "0"代表文件将上传至对象存储；"1"表示内容将追加至已有文件
}

headers = {'Content-Type': 'application/json'}
upload_url = 'http://158.178.240.219:5000/write-json'

response = requests.post(url=upload_url, headers=headers, json=json_data)
if response.status_code == 200:
    print(response.json())
else:
    print('Bad')

返回值：
    {'current_file_position': 30, 'location': '', 'status': 'ok'}


Upload with bytes payload:
-------------------------------
binary_data = bytes('data to be encoded: 你好, ha', 'utf-8')
upload_url = 'http://158.178.240.219:5000/write-bytes?bucket=Hysun_Bucket&name=demo2.bin&position=0&append=1'

response = requests.post(url=upload_url, data=binary_data)
if response.status_code == 200:
    print(response.json())
else:
    print('Bad')

返回值：
    {'current_file_position': 30, 'location': '', 'status': 'ok'}