pid=`ps -ef | grep -i "oss_append" | grep -v grep | awk '{print $2}'`
if [[ ! -z "$pid" ]]
then
	echo "Kill old one: $pid"
	kill -9 $pid > /dev/null 2>&1
fi

cd /home/ubuntu/oss-append > /dev/null

nohup python oss_append.py > ~/app.out 2>&1 &

cd - > /dev/null
