import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1337)) #Host/port


data = s.recv(1338)
print (data)