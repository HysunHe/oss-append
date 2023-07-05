which conda > /dev/null 2>&1 || (wget -nc https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh -b && eval "$(~/miniconda3/bin/conda shell.bash hook)" && conda init && conda config --set auto_activate_base true);
pip install -r requirements-dev.txt

pid=`ps -ef | grep -i "oss_append" | grep -v grep | awk '{print $2}'`
if [[ ! -z "$pid" ]]
then
	echo "Kill old one: $pid"
	kill -9 $pid > /dev/null 2>&1
fi

cd /home/ubuntu/oss-append > /dev/null

nohup python oss_append.py > ~/app.out 2>&1 &

cd - > /dev/null
