from os import getcwd
from sys import path

cwd = getcwd()
path.append(cwd)
from Task5.components.client import cls_client

username_client = input("Nome de usuario:\n ")
escritor = cls_client(username_client)
escritor.mtd_client_start()
