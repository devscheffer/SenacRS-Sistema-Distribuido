import socket
import select


class server:
    def __init__(
        self,
		buffer: int = 1024,
		host: str = "localhost",
		port: int = 50007
    ) -> None:
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

    def mtd_receive_from_connection(self, socket_obj_client: socket) -> dict:
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

    def mtd_user_logout(self, message:dict, dct_clients:dict, socket_notified:socket, sockets_list:list)->tuple:
        dct_clients_v2 = dct_clients
        sockets_list_v2 = sockets_list
        if message is False:
            user_name = dct_clients_v2[socket_notified]["data"].decode("utf-8")
            print(f"Logout usuario <{user_name}>")
            sockets_list_v2.remove(socket_notified)
            dct_clients_v2.pop(socket_notified, None)
            return dct_clients_v2, sockets_list_v2

    def mtd_user_login(self,sockets_list,dct_clients,socket_obj_client,client_address,user):
        sockets_list.append(socket_obj_client)
        dct_clients[socket_obj_client] = user
        print(
            f"Login de novo usuario -> <{client_address[0]}:{client_address[1]}>, usuario: <{user['data'].decode('utf-8')}>"
        )
    def mtd_send_to_connection(self, message:dict, dct_clients:dict, socket_notified:socket)->None:
        user = dct_clients[socket_notified]
        user_name = user["data"].decode("utf-8")
        user_message = message["data"].decode("utf-8")
        print(f"Mensagem de <{user_name}> : {user_message}")
        for socket_obj_client in dct_clients:
            if socket_obj_client != socket_notified:
                socket_obj_client.send(
                    user["header"] + user["data"] + message["header"] + message["data"]
                )

    def mtd_server_start(self):
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
                    user = self.mtd_receive_from_connection(socket_obj_client)
                    if user is False:
                        continue
                    sockets_list.append(socket_obj_client)
                    dct_clients[socket_obj_client] = user
                    print(
                        f"Login de novo usuario -> <{client_address[0]}:{client_address[1]}>, usuario: <{user['data'].decode('utf-8')}>"
                    )
                else:
                    message = self.mtd_receive_from_connection(socket_notified)
                    if message is False:
                        dct_clients, sockets_list = self.mtd_user_logout(
                            message, dct_clients, socket_notified, sockets_list
                        )
                        continue
                    self.mtd_send_to_connection(message, dct_clients, socket_notified)
            for socket_notified in sockets_exception:
                sockets_list.remove(socket_notified)
                dct_clients.pop(socket_notified, None)
