import socket
import errno
import sys


class cls_client:
    def __init__(
        self,
        username_client: str,
        buffer: int = 1024,
        host: str = "localhost",
        port: int = 50007,
    ):
        self.__buffer = buffer
        self.__host = host
        self.__port = port
        self.__username_client = username_client

    @property
    def buffer(self):
        return self.__buffer

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def username_client(self):
        return self.__username_client

    def mtd_client_start(self):
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_client.connect((self.host, self.port))
        # Para nao ser tcp
        socket_client.setblocking(False)
        username = self.username_client.encode("utf-8")
        username_header = f"{len(username):<{self.buffer}}".encode("utf-8")
        socket_client.send(username_header + username)

        while True:
            message = input(f"{self.username_client} > ")
            if message:
                message = message.encode("utf-8")
                message_header = f"{len(message):<{self.buffer}}".encode("utf-8")
                socket_client.send(message_header + message)

            try:
                while True:
                    username_header = socket_client.recv(self.buffer)
                    if not len(username_header):
                        print("Connection closed by the server")
                        sys.exit()
                    username_length = int(username_header.decode("utf-8").strip())
                    username = socket_client.recv(username_length).decode("utf-8")
                    message_header = socket_client.recv(self.buffer)
                    message_length = int(message_header.decode("utf-8").strip())
                    message = socket_client.recv(message_length).decode("utf-8")
                    print(f"<{username}> {message}")

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Reading error: {}".format(str(e)))
                    sys.exit()
                continue
