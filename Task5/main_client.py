from os import getcwd
from sys import path

cwd = getcwd()
path.append(cwd)
from Task5.components.client import cls_client



while True:
	try:
		username_client = input("Nome de usuario:\n ")
		group = input("Grupo do usuario:\n ")
		escritor = cls_client()
		escritor.username_client=username_client
		escritor.group=group
		break
	except Exception as e:
		print(f"{e}")
		continue
escritor.mtd_client_start()
