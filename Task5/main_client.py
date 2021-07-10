from os import getcwd
from sys import path

cwd = getcwd()
path.append(cwd)
from Task5.components.client import cls_client
res = cls_client()
res.start()
