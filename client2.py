import socket
import sys
from time import sleep
from random import randrange

if len(sys.argv) < 2 or not sys.argv[1].isdigit():
    sys.exit("Port number required")

# set GET message
data1 = "LOCK: Directory_Server_Files/room.txt\n\n"
data2 = "UNLOCK: Directory_Server_Files/room.txt\n\n"
data3 = "DOWNLOAD: room.txt\nJOIN_ID: 0 CLIENT_NAME: client\n"


# connect to socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("0.0.0.0", int(sys.argv[1]))) 
s.settimeout(2)

# send data
print "Sent: \"" + data1 + "\""
s.sendall(data1)

# print received response
received = s.recv(2048)
print "Rec: \"{}\"".format(received)

# wait for key press
raw_input("Press Enter to continue...")

# send data
print "Sent: \"" + data2 + "\""
s.sendall(data2)

# print received response
received = s.recv(2048)
print "Rec: \"{}\"".format(received)

# wait for key press
raw_input("Press Enter to continue...")

# send data
print "Sent: \"" + data3 + "\""
s.sendall(data3)

# print received response
received = s.recv(2048)
print "Rec: \"{}\"".format(received)