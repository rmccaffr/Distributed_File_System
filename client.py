import socket
import sys
from time import sleep
from random import randrange

def get_port(data):
	# connect to socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("0.0.0.0", int(sys.argv[1]))) 
	s.settimeout(2)

	# send data
	print "Requesting port for: \"" + data + "\""
	s.sendall(data)

	s.settimeout(2)

	# print received response
	received = s.recv(4096)
	print "Port Rec: \"{}\"".format(received)
	parser = received.splitlines()
 	port = parser[0].split(' ',1)[1]
	return port


if len(sys.argv) < 2 or not sys.argv[1].isdigit():
    sys.exit("Port number required")

# set GET message
data1 = "UPLOAD: foldername1/room1.txt\nUploading the file\n\n"
data2 = "UPLOAD: foldername1/room2.txt\nUploaing the file\n\n"
data3 = "UPLOAD: foldername2/room3.txt\nUploading the file\n"
data4 = "UPDATE: foldername1/room1.txt\nUpdating the  file\n\n"
data5 = "UPDATE: foldername1/room2.txt\nUpdating a file\n\n"
data6 = "UPDATE: foldername2/room3.txt\nUpdating a file\n\n"
data7 = "DOWNLOAD: foldername1/room1.txt\n\n\n"
data8 = "DOWNLOAD: foldername1/room2.txt\n\n\n"
data9 = "DOWNLOAD: foldername2/room3.txt\n\n\n"

#####################################################

#    ULOADING FILES

#####################################################

# send data
print "Sent: \"" + data1 + "\""
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data1)))) 
r.settimeout(2)
r.sendall(data1)

# print received response
received = r.recv(4096)

print "Rec: \"{}\"".format(received)
# wait for key press
raw_input("Press Enter to continue...")

# send data
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data2)))) 
r.settimeout(2)

r.sendall(data2)

# print received response
received = r.recv(4096)
print "Rec: \"{}\"".format(received)

# wait for key press
raw_input("Press Enter to continue...")

# send data
print "Sent: \"" + data3 + "\""

r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data3)))) 
r.settimeout(2)

r.sendall(data3)
# print received response
received = r.recv(4096)
print "Rec: \"{}\"".format(received)

#####################################################

# READ FILES

#####################################################

# wait for key press
raw_input("Press Enter to continue...")

# send data
print "Sent: \"" + data7 + "\""
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data7)))) 
r.settimeout(2)
r.sendall(data7)

# print received response
received = r.recv(4096)

print "Rec: \"{}\"".format(received)
# wait for key press
raw_input("Press Enter to continue...")

# send data
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data8)))) 
r.settimeout(2)

r.sendall(data8)

# print received response
received = r.recv(4096)
print "Rec: \"{}\"".format(received)

# wait for key press
raw_input("Press Enter to continue...")

# send data
print "Sent: \"" + data9 + "\""

r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data9)))) 
r.settimeout(2)

r.sendall(data9)
# print received response
received = r.recv(4096)
print "Rec: \"{}\"".format(received)


#####################################################

#    UPDATING FILES

#####################################################
# wait for key press
raw_input("Press Enter to continue...")

# send data
print "Sent: \"" + data4 + "\""
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data4)))) 
r.settimeout(2)
r.sendall(data4)

# print received response
received = r.recv(4096)

print "Rec: \"{}\"".format(received)
# wait for key press
raw_input("Press Enter to continue...")

# send data
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data5)))) 
r.settimeout(2)

r.sendall(data5)

# print received response
received = r.recv(4096)
print "Rec: \"{}\"".format(received)

# wait for key press
raw_input("Press Enter to continue...")

# send data
print "Sent: \"" + data6 + "\""

r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data6)))) 
r.settimeout(2)

r.sendall(data6)
# print received response
received = r.recv(4096)
print "Rec: \"{}\"".format(received)

#####################################################

# READ FILES

#####################################################

# send data
print "Sent: \"" + data7 + "\""
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data7)))) 
r.settimeout(2)
r.sendall(data7)

# print received response
received = r.recv(4096)

print "Rec: \"{}\"".format(received)
# wait for key press
raw_input("Press Enter to continue...")

# send data
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data8)))) 
r.settimeout(2)

r.sendall(data8)

# print received response
received = r.recv(4096)
print "Rec: \"{}\"".format(received)

# wait for key press
raw_input("Press Enter to continue...")

# send data
print "Sent: \"" + data9 + "\""

r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect(("0.0.0.0", int(get_port(data9)))) 
r.settimeout(2)

r.sendall(data9)
# print received response
received = r.recv(4096)
print "Rec: \"{}\"".format(received)
