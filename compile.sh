#!/bin/sh


echo "[starting_port] [no_servers] [no_copies]"
read port no_servers no_copies
echo "Create Directory"
echo $port $no_servers $no_copies 
python directory.py $port $no_servers $no_copies &
new_port=$((port))
lock_server_port=8888
python lock_server.py $lock_server_port &

for ((i=1;i<=no_servers;i++)); 
do 
	echo "Create replication"
	new_port=$((new_port+1))
	python replication_manager.py $new_port $no_copies $lock_server_port &
	for ((j=1;j<=no_copies;j++)); 
	do
		echo "Create file server"
		new_port=$((new_port+1))
		python server_file.py $new_port &
	done	
done


