import numpy as np
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
import predict

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.open_button = self.findChild(QtWidgets.QPushButton, 'open_disp_btn') # Find the button
        self.open_button.clicked.connect(self.printButtonPressed) # Remember to pass the definition/method, not the return value!
        self.classify_btn = self.findChild(QtWidgets.QPushButton, 'classify_btn')
        self.classify_btn.clicked.connect(self.classifyBtnClicked)
        self.result_lbl = self.findChild(QtWidgets.QLabel, 'result_lbl')
        self.exit_btn=self.findChild(QtWidgets.QPushButton, 'exit_btn')
        self.exit_btn.clicked.connect(self.exitBtnPressed)
        self.show()

    def printButtonPressed(self):
        # This is executed when the button is pressed
        fname =QtWidgets.QFileDialog.getOpenFileName(self, 'Open image',
                                            './', "Image files (*.jpg, *gif, *.png)")
        self.imgName = fname[0]
        self.open_button.setIcon(QtGui.QIcon(fname[0]))
        self.open_button.setIconSize(QtCore.QSize(720, 1000))
    def classifyBtnClicked(self):
        image = predict.load_image(self.imgName)
        model = predict.load_model()
        prediction = model.predict(image)

        print(prediction)
        print(np.max(prediction))
        print(predict.int_to_word_out[np.argmax(prediction)])
        self.result_lbl.setText(predict.int_to_word_out[np.argmax(prediction)])

    def exitBtnPressed(self):
        QtCore.QCoreApplication.instance().quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()