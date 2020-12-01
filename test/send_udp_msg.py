import socket
from sys import argv


if len(argv) < 3:
    ip_address = input("Enter ip address: ")
    port = input("Enter port: ")
    msg = input("Enter text to send: ")
else:
    ip_address = argv[1]
    port = argv[2]
    if len(argv) > 3:
        msg = "".join(argv[3:])
    else:
        msg = input("Enter text to send: ")
port = int(port)

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(msg.encode(), (ip_address, port))
data, server = clientSock.recvfrom(4096)

print("Data:", data.decode(), "IP & port:", server, sep="\n")
