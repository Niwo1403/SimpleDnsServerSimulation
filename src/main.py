# Should be run, to start all DNS server etc.
from time import sleep

from dns.dns_server_batch import DnsServerBatch


dns_servers = DnsServerBatch({
    "127.0.0.11": "root",
    "127.0.0.12": "telematik",
    "127.0.0.13": "switch.telematik",
    "127.0.0.14": "router.telematik",
    "127.0.0.15": "fuberlin",
    "127.0.0.16": "homework.fuberlin",
    "127.0.0.17": "pcpools.fuberlin"
})
dns_servers.run_all()
while True:
    try:
        sleep(60)
    except KeyboardInterrupt:  # Ctrl + C
        dns_servers.stop_all()
        print("Processing stopped, sockets will remain blocked.")
        break
