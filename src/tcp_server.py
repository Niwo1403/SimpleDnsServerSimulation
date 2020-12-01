import socket
from _thread import start_new_thread
from datetime import datetime


def read_data(conn) -> str:
    """
    Reads all data from connection and returns it.
    :param conn: Connection to read from.
    :return: The read text.
    """
    recv_data = []
    tmp_data = conn.recv(TcpServer.BUFF_SIZE)
    while len(recv_data) == TcpServer.BUFF_SIZE:
        recv_data.append(tmp_data)
        tmp_data = conn.recv(TcpServer.BUFF_SIZE)
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


class TcpServer:
    """
    A simple tcp server, which will accept all requests, processes them with the initially set process_request function
    and respond with the return of this function.
    """

    BUFF_SIZE = 1024

    def __init__(self, ip_address, port, process_request, log_requests=False):
        self.sock_information = (ip_address, port)
        self.process_request = process_request
        self.log_requests = log_requests
        self.tcp_socket = None
        self.is_running = False

    def open_socket(self) -> None:
        """
        Opens the socket and starts listening, but won't handle requests.
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind(self.sock_information)
        self.tcp_socket.listen(1)
        print("Listening on", self._get_binding_info())

    def run(self, in_thread=True) -> None:
        """
        Runs the tcp server, by accepting all requests and handle them by calling process_request.
        The function process_request should be set initially,
        will get the requests as argument and returns the response.
        """
        if in_thread:
            start_new_thread(self._process_requests, ())
        else:
            self._process_requests()

    def stop_listening(self) -> None:
        """
        Stops listening for requests, but the socket won't be removed.
        """
        self.is_running = False

    def _process_requests(self) -> None:
        self.is_running = True
        while self.is_running:
            conn_information = self.tcp_socket.accept()
            start_new_thread(self._handle_client, conn_information)

    def _handle_client(self, conn, client) -> None:
        _print_client_information(client)
        try:
            recv_msg = read_data(conn)
            if self.log_requests:
                print(recv_msg)
            reply = self.process_request(recv_msg)
            conn.sendall(reply.encode())
        # ignore exceptions, since the server doesn't care
        finally:
            conn.close()

    def _get_binding_info(self) -> str:
        return ":".join(map(str, self.sock_information))
