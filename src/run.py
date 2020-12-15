# std libraries
import socket
from sys import argv
from datetime import datetime
# local
from dns.dns_message import DnsMessage
from main import main as run_all_server


run_all_server(in_background=True)


rec_res_address = ("127.0.0.10", 53053)  # recursive resolver
req_domain = "windows.pcpools.fuberlin"

dns_msg = DnsMessage.new_dns_request()
dns_msg.set_req(req_domain, recursion_desired=True)
req_domain = dns_msg.build_message()


def send_req(info: str) -> None:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    start_time = datetime.now()
    client_sock.sendto(req_domain.encode(), rec_res_address)
    data, _ = client_sock.recvfrom(4096)
    end_time = datetime.now()

    delta_time = end_time - start_time

    sep = "----------"
    print(
        "", info,
        "Time:", delta_time, sep,
        "Request:", req_domain, sep,
        "Response:", data.decode(), sep,
        sep="\n"
    )


send_req("--- Cache miss:")
send_req("--- Cache hit:")
