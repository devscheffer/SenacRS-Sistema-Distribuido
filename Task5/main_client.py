from os import getcwd
from sys import path

cwd = getcwd()
path.append(cwd)
from Task5.src.client import cls_client


# buffer = 1024
buffer = 10
host = "localhost"
port = 50007

while True:
	try:
		client_user_name = input("Nome de usuario:\n ")
		group = input("Grupo do usuario:\n ")

		escritor = cls_client(
			client_user_name=client_user_name,
			group=group,
			buffer=buffer,
			host=host,
			port=port,
		)
		break
	except Exception as e:
		print(f"{e}")
		continue
escritor.mtd_client_start()
