import re
import socket
import errno
import sys

import re
import json

class cls_client:
    def __init__(
        self,
        buffer: int = 1024,
        host: str = "localhost",
        port: int = 50007,
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

    @property
    def username_client(self):
        return self.__username_client

    @username_client.setter
    def username_client(self, value):
        teste = re.findall(r"^([a-z])", value)
        if len(teste) > 0:
            self.__username_client = value
        else:
            raise ValueError("Nome de usuario invalido: deve comecar com letra")

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, value):
            self.__group = value

    def mtd_create_lst_group(self,group_pattern, text):
        lst_group=re.findall(f'{group_pattern}', text)
        if len(lst_group)==0:
                lst_group=['geral']
        return lst_group

    def mtd_create_dict_message(self,text):
        group_pattern='@(\w+)'
        lst_group = self.mtd_create_lst_group(group_pattern, text)
        text_v2=re.sub(f'{group_pattern}', '', text).strip()
        dict_message = {
            "message": text_v2
            ,"lst_group": lst_group
        }
        return json.dumps(dict_message)


    def mtd_client_start(self):
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_client.connect((self.host, self.port))

        # Para nao ser tcp
        socket_client.setblocking(False)
        dict_user = {
            "user_name": self.username_client
            ,"group": self.group
        }
        dict_user=json.dumps(dict_user)
        username = dict_user.encode("utf-8")

        username_formatted = f"{len(username):<{self.buffer}}"
        username_header_formatted = username_formatted.encode("utf-8")

        username_header_formatted = username_header_formatted + username
        socket_client.send(username_header_formatted)

        while True:
            message_input = input(f"{self.username_client} > ")
            message = self.mtd_create_dict_message(message_input)
            if message:
                message = message.encode("utf-8")
                message_header = f"{len(message):<{self.buffer}}".encode("utf-8")
                socket_client.send(message_header + message)

            try:
                while True:
                    username_header_formatted = socket_client.recv(self.buffer)
                    if not len(username_header_formatted):
                        print("Connection closed by the server")
                        sys.exit()
                    username_length = int(username_header_formatted.decode("utf-8").strip())
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
