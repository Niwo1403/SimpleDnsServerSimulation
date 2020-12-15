# Should be run, to start all DNS server etc.

# std libraries
from time import sleep
from json import loads as load_json
from typing import Callable
# local libraries
from dns.dns_server.dns_server_batch import DnsServerBatch
from dns.recursive_resolver.recursive_resolver import RecursiveResolver
from http_server.http_server_batch import HttpServerBatch
from logger import logger
from proxy import Proxy


def started_as_main() -> bool:
    return __name__ == "__main__"


def main(in_background: bool = False) -> None:
    dns_config, http_config, rec_res_config = load_config()
    dns_servers = run_server_batch(DnsServerBatch, dns_config)
    http_servers = run_server_batch(HttpServerBatch, http_config)
    recursive_resolver = run_recursive_resolver(rec_res_config)
    proxy = run_proxy()
    if not in_background:
        run_till_interrupt(dns_servers, http_servers, recursive_resolver, proxy)


def load_config(
        config_file: str = "../rsrc/config.json") -> ({str: str}, {str: str}):
    config_dic = _load_dict_from_json(config_file)
    dns_config = config_dic["DnsConfig"]
    http_config = config_dic["HttpConfig"]
    rec_res_config = config_dic["RecResConfig"]
    return dns_config, http_config, rec_res_config


def _load_dict_from_json(filename: str) -> {}:
    with open(filename) as file:
        json_str = file.read()
    read_dic = load_json(json_str)
    return read_dic


def run_server_batch(
        batch_class: Callable, config: {str: str}
) -> DnsServerBatch or HttpServerBatch:
    server_batch = batch_class(config)
    server_batch.run_all()
    return server_batch


def run_recursive_resolver(rec_res_config: {str: str}) -> RecursiveResolver:
    root_name_server_addr = rec_res_config["root"]
    rec_resolver = RecursiveResolver(root_name_server_addr)
    rec_resolver.run()
    return rec_resolver


def run_proxy() -> Proxy:
    proxy = Proxy()
    proxy.run()
    return proxy


def run_till_interrupt(
        *stop_after_interrupt: (DnsServerBatch or HttpServerBatch)) -> None:
    try:
        _sleep_forever()
    except KeyboardInterrupt:  # Ctrl + C
        _stop_servers(stop_after_interrupt)
        logger.flush_all()


def _sleep_forever() -> None:
    while True:
        sleep(60)


def _stop_servers(servers: (DnsServerBatch or HttpServerBatch)) -> None:
    for server_batch in servers:
        server_batch.stop()
    logger.log("Processing stopped, sockets will remain blocked until program exits.", flush=True)


if started_as_main():
    main()
