import socket
from _thread import start_new_thread
from datetime import datetime


def read_data(tcp_conn) -> str:
    """
    Reads all data from a tcp connection and returns it.
    :param tcp_conn: Connection to read from.
    :return: The read text.
    """
    recv_data = []
    tmp_data = tcp_conn.recv(SimpleServer.TCP_BUFF_SIZE)
    while len(recv_data) == SimpleServer.TCP_BUFF_SIZE:
        recv_data.append(tmp_data)
        tmp_data = tcp_conn.recv(SimpleServer.TCP_BUFF_SIZE)
    recv_data.append(tmp_data)
    all_bin_data = b"".join(recv_data)
    return all_bin_data.decode()


def _print_client_information(client) -> None:
    """
    Prints ip address and port of client, as well as current timestamp.
    """
    timestamp_separator = "----------"
    print(
        "\n", timestamp_separator, "\n",
        datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        ": Client connected from ", client[0], ":", client[1],
        "\n", timestamp_separator,
        sep=""
    )


class SimpleServer:
    """
    A simple tcp or udp server, which will accept all requests,
    processes them with the initially set process_request function
    and sends the return of this function as response.
    """

    TCP_BUFF_SIZE = 1024
    UDP_BUFF_SIZE = 65535  # max udp size

    def __init__(self, ip_address, port, process_request, use_udp=True, log_requests=False):
        self.sock_information = (ip_address, port)
        self.process_request = process_request
        self.used_udp = use_udp
        self.log_requests = log_requests
        self.socket = None
        self.is_running = False

    def open_socket(self) -> None:
        """
        Opens the socket and starts listening, but won't handle requests.
        """
        socket_type = socket.SOCK_DGRAM if self.used_udp else socket.SOCK_STREAM
        self.socket = socket.socket(socket.AF_INET, socket_type)
        self.socket.bind(self.sock_information)
        if not self.used_udp:
            self.socket.listen(1)
        print(
            "Listening on", self._get_binding_info(),
            "for", "UDP" if self.used_udp else "TCP"
        )

    def run(self, in_thread=True) -> None:
        """
        Runs the tcp server,
        by accepting all requests and handle them by calling process_request.
        The function process_request should be set initially,
        will get the requests as argument and returns the response.
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

    def _accept_request(self):
        return self.socket.recvfrom(SimpleServer.UDP_BUFF_SIZE)\
            if self.used_udp else self.socket.accept()

    def _handle_new_client(self, conn, client) -> None:
        _print_client_information(client)
        try:
            self._handle_request(conn, client)
        # ignore exceptions, since the server doesn't care
        finally:
            if not self.used_udp:
                conn.close()

    def _handle_request(self, conn, client):
        recv_msg = conn.decode() if self.used_udp else read_data(conn)
        if self.log_requests:
            print(recv_msg)
        reply = self.process_request(recv_msg).encode()
        self.socket.sendto(reply, client) if self.used_udp else conn.sendall(reply)

    def _get_binding_info(self) -> str:
        return ":".join(map(str, self.sock_information))
