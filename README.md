# Distributed_File_System

Compile
Bash script that starts up a directory, locking, replicalcation manager and file server on different ports on localhost

bash compile.sh 
[starting_port] [no_severs] [no_copies]

User will be prompted to enter a start port number, amount of replicant managers and how many replicas each manager will have.
Starting port 8000 is recommended as Locking server is put on port 8888. 

Test

python client.py [starting_port]
starting_port must be the same as compile. 


Implementation:

Follow of events:

Client -> Directory: Looking or Creating port number for a foldername
Client <- Directory: Reply with a port number if this foldername already exists or picks a server at random to now host till on
Client -> Replication Manager: Querys replication using port from directory. Replication manager holds ports of all the copies of the file. It also interacts with locking server for file locking
Replication Manager -> Locking Server: Request lock on file
Replication Manager <- Locking Server: Successful lock
Replication Manager -> Primary, executes query
Repication Manager <- Primary, success
Client < - Replication Manager: Replies with result of the query.
  Replication -> Secondary , etc ... Up till number of Copies (Partial Ordering )
  Replication Manager -> Unlocking Server: Request unlock on file
  Replication Manager <- Unlocking Server: Successful unlock


