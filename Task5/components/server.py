import socket
import select
import json


class server:
    def __init__(
        self, buffer: int = 1024, host: str = "localhost", port: int = 50007
    ) -> None:
        self.__buffer = buffer
        self.__host = host
        self.__port = port
        self.dct_group_clients = {}

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
    def dct_group_clients(self):
        return self.__dct_group_clients

    @dct_group_clients.setter
    def dct_group_clients(self, value):
        self.__dct_group_clients = value

    def mtd_receive_from_connection(self, socket_obj_client: socket) -> dict:
        try:
            message_header = socket_obj_client.recv(self.buffer).decode("utf-8")
            message_length = int(message_header.strip())
            message_data = json.loads(socket_obj_client.recv(message_length).decode("utf-8"))
            if not len(message_header):
                return False
            dict_message = {
                "header": message_header,
                "data": message_data,
            }
            return dict_message
        except:
            return False

    def mtd_user_login(
        self, sockets_list, dct_clients, socket_obj_client, client_address, user
    ):
        sockets_list_v2 = sockets_list
        sockets_list_v2.append(socket_obj_client)
        dct_clients_v2 = dct_clients
        dct_clients_v2[socket_obj_client] = user

        group = user['data']['group']
        user_info = {"socket": socket_obj_client, "user": user}
        for i in [group, 'geral']:
            if i in self.dct_group_clients:
                self.dct_group_clients[i].append(user_info)
            else:
                self.dct_group_clients[i] = [user_info]
        print(f"-> Login de novo usuario")
        print(f"    Endereco: {client_address[0]}:{client_address[1]}")
        print(f"    Usuario : {user['data']['user_name']}")
        print(f"    Grupo   : {user['data']['group']}")
        return dct_clients_v2, sockets_list_v2

    def mtd_user_logout(
        self,
        dict_message: dict,
        dct_clients: dict,
        socket_notified: socket,
        sockets_list: list,
    ) -> tuple:
        dct_clients_v2 = dct_clients
        sockets_list_v2 = sockets_list
        if dict_message is False:
            user_name = dct_clients_v2[socket_notified]['data']
            print(f"-> Logout usuario")
            print(f"    {user_name['user_name']}")
            sockets_list_v2.remove(socket_notified)
            dct_clients_v2.pop(socket_notified, None)
            return dct_clients_v2, sockets_list_v2

    def mtd_send_to_connection(
        self,
        dict_message: dict,
        dct_clients: dict,
        socket_notified: socket,
    ) -> None:
        user = dct_clients[socket_notified]
        if dict_message['data']['message'].strip() == '':
            return None
        print(f"-> Mensagem de <{user['data']['user_name']}> :")
        print(f"    {dict_message['data']['message']}")
        for group in dict_message['data']['lst_group']:
            for client in self.dct_group_clients[group]:
                socket_obj_client = client['socket']
                if socket_obj_client != socket_notified:
                    message_info = (
                        user['header']
                        + json.dumps(user['data'])
                        + dict_message['header']
                        + json.dumps(dict_message['data'])
                        ).encode("utf-8")
                    socket_obj_client.send(message_info)

    def mtd_server_start(self):
        socket_obj_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_obj_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_obj_server.bind((self.host, self.port))
        socket_obj_server.listen()
        sockets_list = [socket_obj_server]

        dct_clients = {}
        print(f"Servidor Escutando em <{self.host}:{self.port}>")
        while True:
            sockets_read, _, sockets_exception = select.select(sockets_list, [], sockets_list)
            for socket_notified in sockets_read:
                if socket_notified == socket_obj_server:
                    socket_obj_client, client_address = socket_obj_server.accept()
                    user = self.mtd_receive_from_connection(socket_obj_client)
                    if user is False:
                        continue
                    dct_clients, sockets_list = self.mtd_user_login(
                        sockets_list,
                        dct_clients,
                        socket_obj_client,
                        client_address,
                        user,
                    )
                else:
                    dict_message = self.mtd_receive_from_connection(socket_notified)
                    if dict_message is False:
                        dct_clients, sockets_list = self.mtd_user_logout(dict_message, dct_clients, socket_notified, sockets_list)
                        continue
                    self.mtd_send_to_connection(dict_message, dct_clients, socket_notified)
            for socket_notified in sockets_exception:
                sockets_list.remove(socket_notified)
                dct_clients.pop(socket_notified, None)
