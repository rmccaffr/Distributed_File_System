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
import collections



class ThreadingPoolMixIn(ThreadingMixIn):
    numThreads=60;  
    def serve_forever(self):
        #print "Server Starting..."
        self.queue = Queue(self.numThreads)
        for x in range(self.numThreads):
            server_thread = threading.Thread(target = self.process_request_thread)
            server_thread.daemon = True
            server_thread.start()
        while True:
            self.handle_request()
        self.server_close()
   
    def process_request_thread(self):
        while True:
            ThreadingMixIn.process_request_thread(self, *self.queue.get())
               
    def handle_request(self):
        # Look after request
        request, client_address = self.get_request()
        print request.gettimeout()
        self.queue.put((request, client_address))
        

            
                        
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
     
     def handle(self):
        pass
            
   

class TCPServerChange(SocketServer.TCPServer,SocketServer.BaseServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        """Constructor.  May be extended, do not override."""
        SocketServer.BaseServer.__init__(self, server_address, RequestHandlerClass)
        self.socket = socket.socket(self.address_family,
                                    self.socket_type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise
 


    
class ThreadedTCPServer(ThreadingPoolMixIn, TCPServerChange):
        pass

        
if __name__ == "__main__":
   pass