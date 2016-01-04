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


from tcd_server import ThreadedTCPServer
from tcd_server import ThreadedTCPRequestHandler



from urllib2 import urlopen
my_ip ="127.0.0.1" #urlopen('http://ip.42.pl/raw').read()
print my_ip
directory_replications={}

class ReplicationManager(SocketServer.BaseRequestHandler):
    LOCK_REQUEST = "LOCKFILE: %s\n\n"
    UNLOCK_REQUEST = "UNLOCKFILE: %s\n\n"
    IS_UNLOCKED_REQUEST="ISUNLOCKFILE: %s\n\n"

    #LOCK_RESPONSE_SUCCESS = "SUCCESS LOCKFILE:SUCCESS\n\n"
    #UNLOCK_RESPONSE_SUCCESS= "UNLOCKFILE: [a-zA-Z0-9_.]*\nSTATUS: SUCCESS\n\n"

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
            print "Query on replication manager on port:"+str(port)
            if data.startswith("UPLOAD:") or data.startswith("UPDATE:"):
                self.write(data,self.request)

            elif data.startswith("DOWNLOAD:"):
                self.read(data,self.request)


    def write(self,data,request):
        filename=self.get_filename(data)
        print "Wrinting file:"+filename
        while(self.request_lock(filename)==False):
            pass
        primary_replicant_port=list_file_servers_ports[0]
        response=self.send_request(data,my_ip,primary_replicant_port)
        request.sendall(response)
        for i in list_file_servers_ports:
            if i != list_file_servers_ports[0]:
                self.send_request(data,my_ip,i)
        while(self.request_unlock(filename)==False):
            pass

    def read(self,data,request):
        filename=self.get_filename(data)
        print "Reading File:"+filename
        while(self.is_unlocked(filename)==False):
            pass
        primary_replicant_port=list_file_servers_ports[0]
        reading_port=primary_replicant_port
        response=self.send_request(data,my_ip,reading_port)
        print "Read:"+ response
        request.sendall(response)

    def request_lock(self,filename):
        request=self.LOCK_REQUEST%filename
        response=self.send_request(request,my_ip,lock_server_port)
        if "SUCCESS" in response:
            return True
        else:
            return False
    def request_unlock(self,filename):
        request=self.UNLOCK_REQUEST%filename
        response=self.send_request(request,my_ip,lock_server_port)
        if"SUCCESS" in response:
            return True
        else:
            return False

    def is_unlocked(self,filename):
        request= self.IS_UNLOCKED_REQUEST%filename
        response=self.send_request(request,my_ip,lock_server_port)
        print response
        if "UNLOCKFILE" in response:
            return True
        else: 
            return False
        
    def get_filename(self, input_data):
        parser = input_data.splitlines()
        filename = parser[0].split(' ',1)[1]
        return filename

    def send_request(self,data,ip,port):
        #print "Sending request"+str(data)+"to ip:"+str(ip)+ " port: "+str(port)
        return_data = ""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", port))
        sock.sendall(data)
        while "\n\n" not in return_data:
            data = sock.recv(4096)
            if len(data) == 0:
                break
            return_data += data
        sock.close()
        sock = None
        return return_data

directory_replications={}
port= int(sys.argv[1])
no_copies=int(sys.argv[2])
lock_server_port=int(sys.argv[3])
list_file_servers_ports=[]

for i in range(0,no_copies):
    #os.system("python server_file .py " + str(port+(i+1)))
    print list_file_servers_ports
    list_file_servers_ports.append(port+(i+1))
print " Replication Server on port number:"+ str(sys.argv[1])+" has ports:"+str(list_file_servers_ports)


server = ThreadedTCPServer(('127.0.0.1',int(sys.argv[1])), ReplicationManager)
print "Created Replication Server on port number:"+ str(sys.argv[1])
 

if __name__ == "__main__":
    server.serve_forever()
    
