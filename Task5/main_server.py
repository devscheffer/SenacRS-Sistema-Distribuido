from os import getcwd
from sys import path

cwd = getcwd()
path.append(cwd)
from Task5.components.server import server

from threading import Thread

mural = server()
mural.mtd_server_start()
