from sys import argv

from src.argument_extractor import ArgumentExtractor


class SimpleDnsServer:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def run(self):
        print(self.ip_address, self.port)


def started_as_main():
    return __name__ == "__main__"


if started_as_main():
    arg_ip, arg_port = ArgumentExtractor(argv).get_arguments()
    dns_server = SimpleDnsServer(arg_ip, arg_port)
    dns_server.run()
