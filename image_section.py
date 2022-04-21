# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!
import sys, os
import load_model as mclass
from PyQt5.QtWidgets import *  
from PyQt5.QtGui import * 
from PyQt5 import QtCore
from image_section_form import Ui_Form

class Example(QWidget, Ui_Form):
    
    def __init__(self, parent=None):
        super(Example, self).__init__()
        self.setupUi(self)
        self.l2.hide()
        self.l1.hide()
        self.btn.clicked.connect(self.button_handler_open_file)
        self.btn1.clicked.connect(self.prediction_handler)
        self.btn2.clicked.connect(self.reset_button_handler)
        self.l2.setStyleSheet("background-color: lightgreen")

    def reset_button_handler(self):
        self.l1.hide()
        self.l2.hide()
        self.repaint()

    def prediction_output_handler(self, prediction):
        prediction_text = 'Prediction = {}'.format(prediction)

        self.l2.setText(prediction_text)
        self.l2.show()

    def prediction_handler(self):
        prediction = mclass.predict_image(self.file_path)[0]
        self.prediction_output_handler(prediction)

    def button_handler_open_file(self):

        self.file_path = QFileDialog.getOpenFileName()[0]
        print(self.file_path)
        filename = os.path.basename(self.file_path)

        if filename == '' :
            # or ('img_' not in filename)
            print('Nothing selected OR not a valid MNIST jpg file.')
        else:
            print('File: \'{}\' being selected!'.format(filename))
            
            im_pixmap = QPixmap(self.file_path)

            self.l1.setPixmap(im_pixmap)
            self.l1.show()

def main():

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()