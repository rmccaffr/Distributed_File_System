#!/usr/bin/env python


import SocketServer 
from SocketServer import ThreadingMixIn
import threading 
import socket
from Queue import Queue
import sys
import os
from threading import Lock
import select
import pdb
import filelock
import re


from tcd_server import ThreadedTCPServer
from tcd_server import ThreadedTCPRequestHandler

LOCK_REQUEST = "LOCKFILE: %s\n\n"
UNLOCK_REQUEST = "UNLOCKFILE: %s\n\n"
IS_UNLOCKED_REQUEST="ISUNLOCKFILE: %s\n\n"

LOCK_RESPONSE_SUCCESS = "LOCKFILE: %s\nSTATUS: SUCCESS\n\n"
UNLOCK_RESPONSE_SUCCESS= "UNLOCKFILE: %s\nSTATUS: SUCCESS\n\n"

LOCKED=1
UNLOCKED=0

lock_dict={}
class LockServer(SocketServer.BaseRequestHandler):



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
            print data
            if data.startswith("LOCKFILE:"):
                self.lock(data,self.request)
            elif data.startswith("UNLOCKFILE:"):
                self.unlock(data,self.request)
            elif data.startswith("ISUNLOCKFILE:"):
                self.islocked(data,self.request)

    def lock(self,data,request):
        #print "locking"
        filename=self.get_filename(data)
        #print filename
        global lock_dict
        lock_dict[filename]=LOCKED
        response=LOCK_RESPONSE_SUCCESS%filename
        #print response
        #print "locked"
        request.sendall(response)
              
    def unlock(self,data,request):
        filename=self.get_filename(data)
        global lock_dict
        lock_dict[filename]=UNLOCKED
        response=UNLOCK_RESPONSE_SUCCESS%filename
        request.sendall(response)
     

    def islocked(self,data,request):
        filename=self.get_filename(data)
        global lock_dict
        if(lock_dict[filename]==UNLOCKED):
            #print "Sending unlock response"
            response=UNLOCK_RESPONSE_SUCCESS%filename
            request.sendall(response)
        else:
            response=LOCK_RESPONSE_SUCCESS%filename
            request.sendall(response)

    def get_filename(self,data):
        parser = data.splitlines()
        filename = parser[0].split(' ',1)[1]
        return filename



            

server = ThreadedTCPServer(('127.0.0.1',int(sys.argv[1])), LockServer)
  

if __name__ == "__main__":
    server.serve_forever()
    
