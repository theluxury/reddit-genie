if ps -ef | grep "[r]eddit-elasticsearch-bulk.py" > /dev/null
then
    echo "running"
else
    echo "not working"
    eval "/home/ubuntu/insight/fake-text.sh"
fi
