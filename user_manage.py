import pymysql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox

from user_form import Ui_Form

class User_Manage(QWidget, Ui_Form):
    def __init__(self):
        super(User_Manage, self).__init__()
        self.setupUi(self)
        self.init_table_head()
        self.pushButton.clicked.connect(self.search_user)
        self.pushButton_2.clicked.connect(self.del_user)

    def init_table_head(self):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels([' ', '编号', '用户名'])
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 180)
        self.tableWidget.setColumnWidth(2, 180)
        self.load_all_users()

    def load_all_users(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password="1234", db="pyqt_login")
        cursor = self.conn.cursor()
        sql = 'select id,username from User'
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
            item.setText(str(data[i][0]))
            self.tableWidget.setItem(i, 1, item)
            item = QTableWidgetItem()
            item.setText(data[i][1])
            self.tableWidget.setItem(i, 2, item)

    def search_user(self):
        username = self.lineEdit.text()
        if username == '':
            sql = 'select id, username from User'
        else:
            sql = 'select id, username from User where username="%s"' % (username)
        cursor = self.conn.cursor()
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
            item.setText(str(data[i][0]))
            self.tableWidget.setItem(i, 1, item)
            item = QTableWidgetItem()
            item.setText(data[i][1])
            self.tableWidget.setItem(i, 2, item)

    def del_user(self):
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
            sql = "delete from user where id = %s" % id
            cursor.execute(sql)
            self.conn.commit()
        self.load_all_users()
    ############################
    # 添加删除sql的操作，delList为要删除的用户
    ############################
