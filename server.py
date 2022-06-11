import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),1338))

s.listen()
print ("Server open for connection...")
while True:
    clientconn, address = s.accept()
    print (f"Connection to {address} established...")
    with clientconn:
        clientconn.send(b"You have been connected to server!")
    
