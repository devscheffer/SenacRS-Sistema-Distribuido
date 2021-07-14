import os
import sys

cwd = os.getcwd()
sys.path.append(cwd)
from Task5.src.server import server

# buffer= 1024
buffer = 10
host = "localhost"
port = 50007

mural = server(buffer=buffer, host=host, port=port)
mural.mtd_server_start()
