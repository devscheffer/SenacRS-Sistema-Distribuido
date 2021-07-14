import re
import socket
import errno
import sys

import re
import json


class cls_client:
	def __init__(
		self,
		client_user_name: str,
		group: str,
		buffer: int = 1024,
		host: str = "localhost",
		port: int = 50007,
	) -> None:
		self.__buffer = buffer
		self.__host = host
		self.__port = port
		self.client_user_name = client_user_name
		self.group = group

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
	def client_user_name(self):
		return self._client_user_name

	@client_user_name.setter
	def client_user_name(self, value):
		first_char = re.findall(r"^([a-z])", value)
		if len(first_char) > 0:
			self._client_user_name = value
		else:
			raise ValueError("Nome de usuario invalido: deve comecar com letra")

	@property
	def group(self):
		return self._group

	@group.setter
	def group(self, value):
		self._group = value

	def __mtd_create_lst_group(self, group_pattern, text):
		lst_group = re.findall(f"{group_pattern}", text)
		if len(lst_group) == 0:
			lst_group = ["geral"]
		return lst_group

	def __mtd_create_dict_message(self, text):
		group_pattern = "@(\w+)"
		lst_group = self.__mtd_create_lst_group(group_pattern, text.lower())
		text_v2 = re.sub(f"{group_pattern}", "", text).strip()
		dict_message = {"message": text_v2, "lst_group": lst_group}
		return json.dumps(dict_message)

	def mtd_client_start(self):
		socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_client.connect((self.host, self.port))

		# Para nao ser tcp
		socket_client.setblocking(False)
		dict_user = {"user_name": self.client_user_name, "group": self.group}
		dict_user = json.dumps(dict_user).encode("utf-8")

		username_formatted = f"{len(dict_user):<{self.buffer}}".encode("utf-8")

		user_info = username_formatted + dict_user
		socket_client.send(user_info)

		while True:
			message_input = input(f"{self.client_user_name} > ")
			message = self.__mtd_create_dict_message(message_input)
			if message:
				message = message.encode("utf-8")
				message_header = f"{len(message):<{self.buffer}}".encode("utf-8")
				socket_client.send(message_header + message)

			try:
				while True:
					user_info = socket_client.recv(self.buffer)
					if not len(user_info):
						print("Connection closed by the server")
						sys.exit()
					username_length = int(
						user_info.decode("utf-8").strip()
					)
					user = socket_client.recv(username_length).decode("utf-8")
					message_header = socket_client.recv(self.buffer)
					message_length = int(message_header.decode("utf-8").strip())
					message = socket_client.recv(message_length).decode("utf-8")
					user = json.loads(user)
					message = json.loads(message)
					print(f"-> Mensagem de <{user['user_name']}>")
					print(f"	{message['message']}")

			except IOError as e:
				if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
					print("Reading error: {}".format(str(e)))
					sys.exit()
				continue
