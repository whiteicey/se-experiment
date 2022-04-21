import sys
from PyQt5.QtWidgets import QWidget, QApplication,QMainWindow
from PyQt5.QtGui import QScreen,QPixmap,QImage
from PyQt5 import Qt
from PyQt5.QtCore import QSize
import numpy as np
from writting_ui import  Ui_MainWindow
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import Sequential
import tensorflow as tf

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
json_file = open('./models/mnist.json','r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = tf.keras.models.model_from_json(loaded_model_json)
loaded_model.load_weights("./models/mnist.h5")
loaded_model.compile(optimizer='adam',
                                loss=loss_fn,
                                metrics=["accuracy"])

class MainUIObj(QWidget,Ui_MainWindow):
    def __init__(self):
        super(MainUIObj,self).__init__()
        # self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.widget
        self.pushButton.clicked.connect(self.predictNum)
        self.pushButton_2.clicked.connect(self.clearPad)

        # self.model = load_model("./models/cnn")
    def predictNum(self):
        screen=QApplication.primaryScreen()
        # SmoothTransformation
        img=screen.grabWindow(self.widget.winId()).toImage().scaled(QSize(28,28),  transformMode = 1)
        num_pixel=[]
        for y in range(img.height()):
            for x in range(img.width()):
                curr_pixel=img.pixelColor(x,y).red()
                if curr_pixel!=255: #修改240会导致值全为1，直接暴力255解决问题
                    num_pixel.append(1)
                else:
                    num_pixel.append(0)
        num_pixel=np.array(num_pixel)
        num_pixel=num_pixel.reshape(1,28,28,1)
        index_num=str(np.argmax(loaded_model.predict(num_pixel)[0]))
        # index_num = self.model.predict_classes(num_pixel)
        print(index_num)
        self.plainTextEdit.setPlainText(index_num)



        pass
    def clearPad(self):
        self.widget.clearPad()
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw=MainUIObj()
    mw.show()
    sys.exit(app.exec_())


