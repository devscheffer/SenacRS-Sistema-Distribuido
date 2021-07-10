import socket
import select
import errno
import sys


class cls_client:
	def __init__(self):
		pass
	def start(self):
		buffer = 1024

		host = "localhost"
		port = 50007

		username_client = input("Nome de usuario:\n ")

		socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_client.connect((host, port))
		# Para nao ser tcp
		socket_client.setblocking(False)
		username = username_client.encode('utf-8')
		username_header = f"{len(username):<{buffer}}".encode('utf-8')
		socket_client.send(username_header + username)

		while True:
			message = input(f'{username_client} > ')
			if message:
				message = message.encode('utf-8')
				message_header = f"{len(message):<{buffer}}".encode('utf-8')
				socket_client.send(message_header + message)

			try:
				while True:
					username_header = socket_client.recv(buffer)
					if not len(username_header):
						print('Connection closed by the server')
						sys.exit()
					username_length = int(username_header.decode('utf-8').strip())
					username = socket_client.recv(username_length).decode('utf-8')
					message_header = socket_client.recv(buffer)
					message_length = int(message_header.decode('utf-8').strip())
					message = socket_client.recv(message_length).decode('utf-8')
					print(f'<{username}> {message}')

			except IOError as e:
				if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
					print('Reading error: {}'.format(str(e)))
					sys.exit()
				continue

