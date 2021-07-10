from os import getcwd
from sys import path

cwd = getcwd()
path.append(cwd)
from Task5.components.server import server

res=server()
res.start()
