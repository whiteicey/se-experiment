from PyQt5.QtCore import QThread
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

class ftp_thread(QThread):
    def __init__(self):
        super(ftp_thread, self).__init__()

    def run(self):
        start()


def start():
    authorizer = DummyAuthorizer()
    if not os.path.isdir('./ftpfile'):
        os.mkdir('./ftpfile')
    authorizer.add_user('user', '12345', './ftpfile', perm='elradfmwM')

    handler = FTPHandler
    handler.authorizer = authorizer

    address = ('127.0.0.1', 2121)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()


if __name__ == '__main__':
    start()
