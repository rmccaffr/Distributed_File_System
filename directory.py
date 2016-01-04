#!/usr/bin/env python


import SocketServer 
from SocketServer import ThreadingMixIn
import threading 
import socket
import time
from Queue import Queue
import sys
import os
from threading import Lock
import select
import pdb
import base64
import collections
import re
import random

from tcd_server import ThreadedTCPServer
from tcd_server import ThreadedTCPRequestHandler

PORT_RESPONSE = "PORT: %s\n\n"

ERROR_RESPONSE= "FILE_NONEXISTENT: %s"

directory_replications={}
directory_replications_files={}
my_ip="127.0.0.1"

class DirectoryManager(SocketServer.BaseRequestHandler):

    #def __init__(self, folder):
    #    self.DIRECTORY_LOCATION = os.path.join(self.DIRECTORY_NAME, str(self.folder))

    def handle(self):
        while True:
            self.request.setblocking(0)
            timeout_in_seconds=0.1
            data = ''
            while "\n\n" not in data:
                ready = select.select([self.request], [], [], timeout_in_seconds)
                if ready[0]:
                    d = self.request.recv(4096)
                    data += d
                    if len(d) < 4096:
                        break
                else:
                    data=""
            if data =='':
                print "Socket Timeout, closing socket..."
                break    
            #print data
            if data.startswith("UPDATE:") or data.startswith("DOWNLOAD:"): 
                self.incoming_request(data,self.request)

            elif data.startswith("UPLOAD:"):
                self.incoming_upload_request(data,self.request)


    def incoming_upload_request(self,data,request):
        foldername,filename=self.parse_input(data)
        print "Requesting port from directory for:"+foldername
        replication_port= self.directory(foldername)
        self.directory_files(foldername,filename)
        response= PORT_RESPONSE % str(replication_port)
        print "Responding port number: "+str(replication_port)
        request.sendall(response)

    def incoming_request(self,data,request):
        foldername,filename=self.parse_input(data)
        print "Requesting port from directory for:"+foldername
        path=foldername+"/"+filename 
        if path not in directory_replications_files:
            response=ERROR_RESPONSE % filename
            request.sendall(response)
            return
        replication_port= self.directory(foldername)
        response= PORT_RESPONSE % str(replication_port)
        print "Responding port number: "+str(replication_port)
        request.sendall(response)



    def send_request(self,data,ip,port):
        return_data = ""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((my_ip, port))
        sock.sendall(data)
        while "\n\n" not in return_data:
            data = sock.recv(4096)
            if len(data) == 0:
                break
            return_data += data
        sock.close()
        sock = None
        return return_data

    def directory(self,foldername):
        global directory_replications
        if foldername not in directory_replications.keys():
            directory_replications[foldername]=self.assign_port_random()
        return directory_replications[foldername]
    def directory_files(self,foldername,filename):
        global directory_replications_files
        path=foldername+"/"+filename 
        if path not in directory_replications_files.keys():
            directory_replications_files[path]=1


    def parse_input(self,data):
        parser = data.splitlines()
        temp = parser[0].split(' ',1)[1]
        folder=temp.split('/',1)[0]
        filename=temp.split('/',1)[1]
        return folder,filename

    def assign_port_random(self):
        global assigned_ports
        global no_servers
        index= random.randint(0,no_servers-1)
        return list_servers_ports[index]




directory_replications={}
port= int(sys.argv[1])
no_servers=int(sys.argv[2])
no_copies=int(sys.argv[3])
assigned_ports= port+1
lock_server_port=1000
list_servers_ports=[]

for i in range(0,no_servers):
    #os.system("replication_manager.py " + str(assigned_ports+(i*(no_copies+1)))+ " "+str(no_copies)+ " "+str(lock_server_port)
    list_servers_ports.append(assigned_ports)
    assigned_ports=assigned_ports+no_copies+1

print "Ports of directory"
print list_servers_ports
server = ThreadedTCPServer(('127.0.0.1',int(sys.argv[1])), DirectoryManager)
  

if __name__ == "__main__":
    server.serve_forever()
    
