from time import sleep

import tensorflow as tf
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QMessageBox
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import Callback
from train_form import Ui_Form
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class trainPara(QObject):
    progress = pyqtSignal(int, int)
    iffinsh = pyqtSignal()
    def __init__(self):
        super(trainPara, self).__init__()
        self.epoch = 0
        self.batch = 0
        self.finish = False
        self.acc = 0

    def setBatch(self, batch):
        self.progress.emit(self.epoch, batch)

    def setEpoch(self, epoch):
        self.epoch = epoch

    def setFinsh(self):
        self.iffinsh.emit()

    def setAccuracy(self, accuracy):
        self.acc = accuracy

    def getAccuracy(self):
        return self.acc

para = trainPara()


class MyHistory(Callback):

    def on_train_begin(self, logs=None):
        print("训练任务开始！")

    def on_batch_end(self, batch, logs=None):
        para.setBatch(batch)
        para.setAccuracy(logs['accuracy'])

    def on_epoch_begin(self, epoch, logs=None):
        para.setEpoch(epoch)


class MnistTraining(QWidget, Ui_Form):
    def __init__(self, model_type="cnn"):
        super(MnistTraining, self).__init__()
        self.setupUi(self)
        self.batch_val = 32
        self.epoch_val = 5
        self.lr_val = 0.0001
        para.progress.connect(self.set_progress)
        para.iffinsh.connect(self.set_progress_finsh)
        self.pushButton.clicked.connect(self.start_train)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateChart)
        self.drawChart()
    def drawChart(self):
        self.graphicsView.setTitle("正确率", color='008080', size='12pt')
        self.graphicsView.setLabel("bottom", "时间")
        self.graphicsView.setLabel("left", "正确率")
        self.graphicsView.showGrid(x=True, y=True)
        # 背景色改为白色
        self.graphicsView.setBackground('w')
        self.curve = self.graphicsView.plot(
            pen=pg.mkPen('r', width=1)
        )
        self.i = 0
        self.x = []
        self.y = []

    def updateChart(self):
        acc = para.getAccuracy()
        if acc < 0.9:
            return
        self.i += 1
        self.x.append(self.i)
        self.y.append(acc)
        self.curve.setData(self.x, self.y)

    def set_progress(self, epoch, batch):
        presize = 60000 / self.batch_val
        self.progressBar.setValue((batch + presize * epoch) / (presize * self.epoch_val) * 100)

    def set_progress_finsh(self):
        self.timer.stop()
        self.tthread.quit()
        self.progressBar.setValue(100)
        
    def start_train(self):
        print("start_train")
        if self.epoch.text() != '':
            self.epoch_val = int(self.epoch.text())
        if self.batch_size.text() != '':
            self.batch_val = int(self.batch_size.text())
        if self.lr.text() != '':
            self.lr_val = float(self.lr.text())
        self.tthread = trainThread("cnn", self.epoch_val, self.lr_val, self.batch_val)
        self.tthread.start()
        self.timer.start(1000)

class trainThread(QThread):
    def __init__(self, model_type="cnn", epoch=10, lr=0.0001, batch_size=32):
        super().__init__()
        self.model_type = model_type
        self.model_path = "./cnn"
        self.epoch = epoch
        self.lr = lr
        self.batch_size = batch_size
        print("thread init")

    def run(self):
        print("thread run")
        self.train(self.epoch, self.lr, self.batch_size)

    def processData(self, model_type='cnn'):
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        # model_path="./models/cnn"
        x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
        x_test = x_test.reshape(x_test.shape[0], x_train.shape[1], x_train.shape[2], 1)
        self.cnn_input_shape = (x_train.shape[1], x_train.shape[2], 1)

        # convert the data to the right type
        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train /= 255
        x_test /= 255
        y_train = keras.utils.to_categorical(y_train, 10)
        y_test = keras.utils.to_categorical(y_test, 10)

        return x_train, y_train, x_test, y_test

    def cnnTrain(self, epoch_num=5, lr=0.0001, batch_size=32):
        print(epoch_num)
        print(lr)
        print(batch_size)
        optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=lr)
        x, y, x_, y_ = self.processData("cnn")
        self.model = Sequential()

        self.model.add(Conv2D(32, kernel_size=(5, 5), strides=(1, 1),
                              activation='relu',
                              input_shape=self.cnn_input_shape))

        self.model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        self.model.add(Conv2D(64, (5, 5), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Flatten())

        # fully connect nn
        self.model.add(Dense(1000, activation='selu'))
        self.model.add(Dense(10, activation='softmax'))

        self.model.compile(loss=keras.losses.categorical_crossentropy,
                           optimizer=keras.optimizers.Adam(),
                           metrics=['accuracy'])
        myhis = MyHistory()
        self.result = self.model.fit(x, y,
                                     batch_size=batch_size, epochs=epoch_num, verbose=1, callbacks=[myhis])
        para.setFinsh()

    def train(self, epochs=5, lr=0.0001, batch_size=32):
        print(epochs, lr, batch_size)
        self.processData('cnn')
        self.cnnTrain(epoch_num=epochs, lr=lr, batch_size=batch_size)
        print(self.result.history)
        self.draw(self.result)
        self.model.save(self.model_path)
        self.model_json = self.model.to_json()
        with open("./mnist.json", 'w') as file:
            file.write(self.model_json)
        self.model.save_weights('./mnist.h5')

    def draw(self, res):
        x = range(len(res.history['accuracy']))
        plt.plot(x, res.history['accuracy'])
        plt.show()


if __name__ == '__main__':
    mt = MnistTraining("cnn")
    mt.train(5, 0.0001, 32)
