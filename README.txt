Incremental sync file to Oracle object storage.

http://132.226.236.106:5000

curl -i -X POST --data-binary "ZGF0YSB0byBiZSBlbmNvZGVkOiDkvaDlpb0=" 'http://132.226.236.106:5000/write-bytes?bucket=Hysun_DianJiang&name=testcase5/test1.bin&position=-1&append=1&destination=testcase_url/te
st2.bin'

curl -i -H "Content-Type: application/json" -X POST -d '{"bucket": "Hysun_DianJiang", "name":"testcase5/test2.txt", "position": -1, "content": "ZGF0YSB0byBiZSBlbmNvZGVkOiDkvaDlpb0=", "destination": "testcase_curl/aaa.txt", "append": "1"}' http://132.226.236.106:5000/write-json