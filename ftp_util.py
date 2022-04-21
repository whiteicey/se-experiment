import ftplib
from ftplib import FTP
import uuid


class FTP_Util:
    def __init__(self, host, port, user, passwd):
        self.ftp = FTP()
        self.connect = None
        self.port = port
        self.host = host
        self.user = user
        self.passwd = passwd

    def connect_ftp(self):
        self.connect = self.ftp.connect(self.host, self.port)
        self.ftp.login(self.user, self.passwd)
        print("连接成功")
        return True

    def upLoad(self, filepath):
        f = open(filepath, 'rb')
        suff = filepath.split('.')[-1]
        newFilename = str(uuid.uuid1()) + '.' + suff
        print(newFilename)
        try:
            self.ftp.storbinary('STOR %s' % newFilename, f)
        except ftplib.error_perm:
            return "fail"
        return newFilename

    def downLoad(self, filename):
        tempfilename = str(uuid.uuid1())
        f = open(tempfilename, 'wb').write()
        try:
            self.ftp.retrbinary('RETR %s' % filename, f)
        except ftplib.error_perm:
            return "fail"
        return tempfilename

    def del_file(self,filename):
        try:
            self.ftp.delete(filename)
        except ftplib.error_perm:
            return False
        return True

    def close_connect(self):
        self.ftp.close()