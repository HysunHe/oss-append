Incremental sync file to Oracle object storage.

curl -i -X POST --data-binary "ZGF0YSB0byBiZSBlbmNvZGVkOiDkvaDlpb0=" 'http://localhost:5000/write-bytes?bucket=Hysun_DianJiang&name=demo1.bin&position=0&append=1'

curl -i -H "Content-Type: application/json" -X POST -d '{"bucket": "Hysun_DianJiang", "name":"demo2.bin", "position": -1, "content": "ZGF0YSB0byBiZSBlbmNvZGVkOiDkvaDlpb0=", "append": "1"}' http://localhost:5000/write-json