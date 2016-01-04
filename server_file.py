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

UPLOAD_SYNTAX = "UPLOAD: [a-zA-Z0-9_.]*\nDATA: .*\n\n"
UPDATE_REGEX = "UPDATE: [a-zA-Z0-9_.]*\nDATA: .*\n\n"
UPDATE_HEADER = "UPDATE: %s\nDATA: %s\n\n"
DOWNLOAD_REGEX = "DOWNLOAD: [a-zA-Z0-9_.]*\n\n"

UPLOAD_RESPONSE ="FILE: %s\nUPLOAD SUCESSS\n\n"
UPDATE_RESPONSE ="FILE: %s\nUPDATE SUCESSS\n\n"
DOWNLOAD_RESPONSE ="FILE: %s\nSUCESSS\n\n"


from urllib2 import urlopen
#my_ip = urlopen('http://ip.42.pl/raw').read()
my_ip=''
port= int(sys.argv[1])
class FileServer(SocketServer.BaseRequestHandler):

    DIRECTORY_PATH =os.getcwd()+"/Directory_Server_Files/"
    DIRECTORY_NAME = str(port)
    if not os.path.exists(DIRECTORY_PATH+"/"+DIRECTORY_NAME):
        os.makedirs(DIRECTORY_PATH+DIRECTORY_NAME)
    DIRECTORY_LOCATION=os.path.join(DIRECTORY_PATH,DIRECTORY_NAME)

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
            if data.startswith("UPLOAD:"):
                self.upload(data,self.request)

            elif data.startswith("DOWNLOAD:"):
                self.download(data,self.request)

            elif data.startswith("UPDATE:"):
                self.update(data,self.request)


    def upload(self,data,request):
        self.write(data)
        parser = data.splitlines()
        folder,filename = self.parse_input(data)
        print "Uploading file:"+filename
        response= str(UPLOAD_RESPONSE % (folder+"/"+filename))
        request.sendall(response)

    def download(self,data,request):
        folder,filename = self.parse_input(data)
        path = os.path.join(self.DIRECTORY_LOCATION+"/"+folder, filename)
        file_handle = open(path, "r+")
        output=file_handle.read()
        response=DOWNLOAD_RESPONSE%output
        print "Downloading file:"+filename
        print response
        request.sendall(response)

    def update(self,data,request):
        self.write(data)
        parser = data.splitlines()
        filename = parser[0].split(' ',1)[1]
        response= str(UPDATE_RESPONSE % filename)
        print "Updating file:"+filename
        request.sendall(response)

    def write(self, input_data):
        # Function that process an update/upload request and writes data to the server
        self.create_folder(input_data)
        parser = input_data.splitlines()
        #print request
        #print request[0]
        data = parser[1]    
        folder,filename=self.parse_input(input_data)   
        path = os.path.join(self.DIRECTORY_LOCATION+"/"+folder, filename)
        file_handle = open(path, "w+")
        file_handle.write(data)

    def create_folder(self,data):
        foldername,filename=self.parse_input(data)
        print "Create folder"
        if not os.path.exists(self.DIRECTORY_PATH+"/"+self.DIRECTORY_NAME+"/"+foldername):
            os.makedirs(self.DIRECTORY_PATH+self.DIRECTORY_NAME+"/"+foldername+"/")
            print "folder created"

    def parse_input(self,data):
        parser = data.splitlines()
        temp = parser[0].split(' ',1)[1]
        folder=temp.split('/',1)[0]
        filename=temp.split('/',1)[1]
        return folder,filename





server = ThreadedTCPServer(('127.0.0.1',int(sys.argv[1])), FileServer)
print "Created File Server on port number:"+ str(sys.argv[1])

if __name__ == "__main__":
    server.serve_forever()
    
