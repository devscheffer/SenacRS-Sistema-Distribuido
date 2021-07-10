import socket
import select


class server:
    def __init__(self, buffer=1024, host="localhost", port=50007):
        self.__buffer = buffer
        self.__host = host
        self.__port = port

    @property
    def buffer(self):
        return self.__buffer

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    def fn_receive_from_connection(self, socket_obj_client: socket) -> dict:
        try:
            message_header = socket_obj_client.recv(self.buffer)
            if not len(message_header):
                return False
            message_length = int(message_header.decode("utf-8").strip())
            dict_message = {
                "header": message_header,
                "data": socket_obj_client.recv(message_length),
            }
            return dict_message
        except:
            return False

    def start(self):
        socket_obj_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_obj_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_obj_server.bind((self.host, self.port))
        socket_obj_server.listen()
        sockets_list = [socket_obj_server]

        dct_clients = {}

        print(f"Servidor Escutando em <{self.host}:{self.port}>")

        while True:
            sockets_read, _, sockets_exception = select.select(
                sockets_list, [], sockets_list
            )
            for socket_notified in sockets_read:
                if socket_notified == socket_obj_server:
                    socket_obj_client, client_address = socket_obj_server.accept()
                    user = self.fn_receive_from_connection(socket_obj_client)
                    if user is False:
                        continue
                    sockets_list.append(socket_obj_client)
                    dct_clients[socket_obj_client] = user
                    print(
                        f"Login de novo usuario -> <{client_address[0]}:{client_address[1]}>, usuario: <{user['data'].decode('utf-8')}>"
                    )
                else:
                    message = self.fn_receive_from_connection(socket_notified)
                    if message is False:
                        user_name = dct_clients[socket_notified]["data"].decode("utf-8")
                        print(f"Logout usuario <{user_name}>")
                        sockets_list.remove(socket_notified)
                        dct_clients.pop(socket_notified, None)
                        continue
                    user = dct_clients[socket_notified]
                    user_name = user["data"].decode("utf-8")
                    user_message = message["data"].decode("utf-8")
                    print(f"Mensagem de <{user_name}> : {user_message}")
                    for socket_obj_client in dct_clients:
                        if socket_obj_client != socket_notified:
                            socket_obj_client.send(
                                user["header"]
                                + user["data"]
                                + message["header"]
                                + message["data"]
                            )
            for socket_notified in sockets_exception:
                sockets_list.remove(socket_notified)
                dct_clients.pop(socket_notified, None)
