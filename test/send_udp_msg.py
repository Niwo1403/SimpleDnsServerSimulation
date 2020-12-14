# std libraries
import socket
from sys import argv
from datetime import datetime
# local
from dns.dns_message import DnsMessage

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

dns_msg = DnsMessage.new_dns_request()
dns_msg.set_req(msg, recursion_desired=True)
msg = dns_msg.build_message()

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

start_time = datetime.now()
clientSock.sendto(msg.encode(), (ip_address, port))
data, server = clientSock.recvfrom(4096)
end_time = datetime.now()

delta_time = end_time - start_time

sep = "----------"
print(
    "Time:", delta_time, sep,
    "Request:", msg, sep,
    "Response:", data.decode(), sep,
    "server IP & port:", server,
    sep="\n"
)
