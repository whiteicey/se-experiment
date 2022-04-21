import pymysql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QFileDialog, QPushButton

from pic_form import Ui_Form
from ftp_util import FTP_Util


class Pic_Manage(QWidget, Ui_Form):
    def __init__(self):
        super(Pic_Manage, self).__init__()
        self.setupUi(self)
        self.init_table_head()
        self.ftp = FTP_Util('127.0.0.1', 2121, 'user', '12345')
        self.connect_ftp()
        self.init_sql()
        self.load_all_picture()
        self.pushButton.clicked.connect(self.uploadimg)
        self.pushButton_2.clicked.connect(self.def_file)
    def init_table_head(self):
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels([' ', '编号', '名称', '标签', '操作'])
        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setColumnWidth(1, 40)
        self.tableWidget.setColumnWidth(2, 240)
        self.tableWidget.setColumnWidth(3, 180)
        self.tableWidget.setColumnWidth(3, 90)

    def connect_ftp(self):
        if not self.ftp.connect_ftp():
            QMessageBox.information(self, "提示", "连接失败", QMessageBox.Ok)

    def uploadimg(self):
        file = QFileDialog().getOpenFileName()
        print(file[0])
        upfile = self.ftp.upLoad(file[0])
        if upfile != "fail":
            QMessageBox.information(self, "提示", "上传成功", QMessageBox.Ok)
            cursor = self.conn.cursor()
            sql = "insert into img (name) values ('%s')" % upfile
            cursor.execute(sql)
            self.conn.commit()
            self.load_all_picture()
        else:
            QMessageBox.information(self, "提示", "上传失败", QMessageBox.Ok)

    def def_file(self):
        rowCount = self.tableWidget.rowCount()
        delList = []
        for i in range(0, rowCount):
            item = self.tableWidget.item(i, 0)
            if Qt.Checked == item.checkState():
                delList.append(self.tableWidget.item(i, 1).text())
        if len(delList) == 0:
            QMessageBox.information(self, '错误', '未选择行', QMessageBox.Yes)
            return
        print(delList)
        cursor = self.conn.cursor()
        for id in delList:
            sql = "delete from img where id = %s" % id
            cursor.execute(sql)
            self.conn.commit()
        self.load_all_picture()

    def init_sql(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password="1234", db="pyqt_login")

    def load_all_picture(self):
        cursor = self.conn.cursor()
        sql = 'select id, name, label from img'
        result = cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        resnum = len(data)
        self.tableWidget.setRowCount(resnum)
        for i in range(0, resnum):
            print(data[i])
            item = QTableWidgetItem()
            item.setCheckState(Qt.Unchecked)
            self.tableWidget.setItem(i, 0, item)
            item = QTableWidgetItem()
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setText(str(data[i][0]))
            self.tableWidget.setItem(i, 1, item)
            item = QTableWidgetItem()
            item.setText(data[i][1])
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 2, item)
            item = QTableWidgetItem()
            item.setText(str(data[i][2]))
            self.tableWidget.setItem(i, 3, item)
            btn = QPushButton("标记")
            self.tableWidget.setCellWidget(i, 4, btn)
            btn.clicked.connect(lambda:self.on_tab_btn_click(i))

    def on_tab_btn_click(self, index):
        id = self.tableWidget.item(index, 1).text()
        label = self.tableWidget.item(index, 3).text()
        cursor = self.conn.cursor()
        sql = "update img set label = %s where id = %s" % (label, id)
        cursor.execute(sql)
        self.conn.commit()
        self.load_all_picture()


