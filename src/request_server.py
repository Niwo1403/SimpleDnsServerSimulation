# std imports
import socket
from _thread import start_new_thread
from datetime import datetime
from time import sleep
from typing import Callable
# local imports
from logger import logger


def simulate_network_delay():
    sleep(0.1)


class RequestServer:
    """
    A simple TCP or UDP server, which will accept all requests,
    processes them with the initially set process_request function
    and sends the return of this function as response.
    The server will close the connection after responding once,
    so TCP and UDP can be used.
    """

    TCP_BUFF_SIZE = 1024
    UDP_BUFF_SIZE = 65535  # max udp size

    @staticmethod
    def read_tcp_data(tcp_conn: socket) -> str:
        """
        Reads all data from a tcp connection and returns it.
        :param tcp_conn: Connection to read from.
        :return: The read text.
        """
        recv_data = []
        tmp_data = tcp_conn.recv(RequestServer.TCP_BUFF_SIZE)
        while len(recv_data) == RequestServer.TCP_BUFF_SIZE:
            recv_data.append(tmp_data)
            tmp_data = tcp_conn.recv(RequestServer.TCP_BUFF_SIZE)
        recv_data.append(tmp_data)
        all_bin_data = b"".join(recv_data)
        return all_bin_data.decode()

    def __init__(self,
                 ip_address: str, port: int,
                 process_request: Callable,
                 use_udp: bool = True, log_requests: bool = False
                 ):
        self.sock_information = (ip_address, port)
        self.process_request = process_request
        self.used_udp = use_udp
        self.log_requests = log_requests
        self.socket = None
        self.is_running = False
        logger.register_logger(
            key_obj=self, log_file_name=f"../log/{ip_address}.log"
        )

    def open_socket(self) -> None:
        """
        Opens the socket and starts listening, but won't handle requests.
        """
        socket_type = socket.SOCK_DGRAM if self.used_udp \
            else socket.SOCK_STREAM
        self.socket = socket.socket(socket.AF_INET, socket_type)
        self.socket.bind(self.sock_information)
        if not self.used_udp:
            self.socket.listen(1)
        logger.log(f"Listening on {self._get_binding_info()} for "
                   f"{'UDP' if self.used_udp else 'TCP'}")

    def run(self, in_thread: bool = True) -> None:
        """
        Runs the tcp server,
        by accepting all requests and handle them by calling process_request.
        The function process_request should be set initially,
        will get the requests as argument and returns the response.
        The method open_socket() must be called before run().
        """
        if in_thread:
            start_new_thread(self._process_incoming_requests, ())
        else:
            self._process_incoming_requests()

    def stop_listening(self) -> None:
        """
        Stops listening for requests, but the socket won't be removed.
        """
        self.is_running = False

    def _process_incoming_requests(self) -> None:
        self.is_running = True
        while self.is_running:
            conn_information = self._accept_request()
            start_new_thread(self._handle_new_client, conn_information)

    def _accept_request(self) -> str or (socket, (str, str)):
        return self.socket.recvfrom(RequestServer.UDP_BUFF_SIZE) \
            if self.used_udp else self.socket.accept()

    def _handle_new_client(self,
                           conn: str or socket, client: (str, str)) -> None:
        self._print_client_information(client)
        try:
            self._handle_request(conn, client)
        # ignore exceptions, since the server doesn't care
        finally:
            if not self.used_udp:
                conn.close()
        logger.flush(self)

    def _handle_request(self,
                        conn: str or socket,
                        client: None or (str, str)) -> None:
        """
        Handles an incoming connection request and processes it.
        Arguments should either be a string and None for UDO,
        or a socket object and the client information (str, str) for TCP.
        """
        simulate_network_delay()  # sending request
        recv_msg = conn.decode() if self.used_udp else self.read_tcp_data(conn)
        if self.log_requests:
            logger.log(recv_msg, key_obj=self)
        reply = self.process_request(recv_msg).encode()
        self.socket.sendto(reply, client) if self.used_udp \
            else conn.sendall(reply)
        simulate_network_delay()  # sending response

    def _get_binding_info(self) -> str:
        return ":".join(map(str, self.sock_information))

    def _print_client_information(self, client: (str, str)) -> None:
        """
        Prints ip address and port of client, as well as current timestamp.
        """
        timestamp_separator = "----------"
        logger.log(f"\n{timestamp_separator}\n"
                   f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}: "
                   f"Client connected from {client[0]}:{client[1]}\n"
                   f"{timestamp_separator}", key_obj=self)
