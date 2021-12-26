from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

import appfiles.utils.event as event


class Ytb5(QWidget):
    eventSignal = pyqtSignal(event.Event)

    def __init__(self, assets, logger):
        QWidget.__init__(self)
        self.setWindowFlags(
            Qt.Widget | QtCore.Qt.FramelessWindowHint)
        self.resize(676, 371)

        self.clicked = False

        self.logger = logger

        self.setupUi()
        self.applyQss(assets.getQss(f"main.qss"))

    def setupUi(self):

        self.setWindowTitle("Window")
        self.setObjectName("Window")

        self.quitButton = QtWidgets.QPushButton("Quit", self)
        self.quitButton.setGeometry(QtCore.QRect(600, 0, 75, 23))
        self.quitButton.clicked.connect(self.close)
        self.quitButton.setObjectName("quitButton")

        self.formatComboBox = QtWidgets.QComboBox(self)
        self.formatComboBox.setGeometry(QtCore.QRect(120, 70, 131, 31))
        self.formatComboBox.setObjectName("formatComboBox")

        self.formatLabel = QtWidgets.QLabel("Format:", self)
        self.formatLabel.setGeometry(QtCore.QRect(40, 80, 61, 16))
        self.formatLabel.setObjectName("formatLabel")

        self.titleLabel = QtWidgets.QLabel("Ytb5", self)
        self.titleLabel.setGeometry(QtCore.QRect(70, 20, 181, 41))
        self.titleLabel.setObjectName("titleLabel")

        self.consoleTextEdit = QtWidgets.QTextEdit(self)
        self.consoleTextEdit.setGeometry(QtCore.QRect(0, 200, 381, 171))
        self.consoleTextEdit.setReadOnly(True)
        self.consoleTextEdit.setObjectName("consoleTextEdit")
        # for _ in range(50):
        #     self.consoleTextEdit.append("aaaa")

        self.outputPathLabel = QtWidgets.QLabel("Output path: ", self)
        self.outputPathLabel.setGeometry(QtCore.QRect(40, 120, 47, 13))
        self.outputPathLabel.setObjectName("outputPathLabel")

        self.outputPathDisplayLabel = QtWidgets.QLabel("Path . . .", self)
        self.outputPathDisplayLabel.setGeometry(
            QtCore.QRect(120, 120, 131, 16))
        self.outputPathDisplayLabel.setObjectName("outputPathDisplayLabel")

        self.selectOutputPathButton = QtWidgets.QPushButton(
            "Select path",  self)
        self.selectOutputPathButton.setGeometry(
            QtCore.QRect(290, 110, 111, 23))
        self.selectOutputPathButton.setObjectName("selectOutputPathButton")

        self.linkLabel = QtWidgets.QLabel("Link:", self)
        self.linkLabel.setGeometry(QtCore.QRect(40, 160, 47, 13))
        self.linkLabel.setObjectName("linkLabel")

        self.linkLineEdit = QtWidgets.QLineEdit(self)
        self.linkLineEdit.setGeometry(QtCore.QRect(120, 160, 151, 20))
        self.linkLineEdit.setObjectName("linkLineEdit")

        self.downloadButton = QtWidgets.QPushButton("Download", self)
        self.downloadButton.setGeometry(QtCore.QRect(460, 200, 111, 61))
        self.downloadButton.setObjectName("downloadButton")

    def mousePressEvent(self, event):
        self.clicked = True
        self.old_pos = event.screenPos()

    def mouseReleaseEvent(self, event):
        self.clicked = False

    def mouseMoveEvent(self, qevent):
        # make sure that the mouse is not colliding with the format combo box
        # else the window movement will by laggy as the combo box clic event will be also triggerd
        point = (qevent.screenPos().x(), qevent.screenPos().y())
        x1 = self.formatComboBox.x()
        y1 = self.formatComboBox.y()
        x2 = x1 + self.formatComboBox.width()
        y2 = y1 + self.formatComboBox.height()

        if not (x1 < point[0] and point[0] < x2 and y1 < point[1] and point[1] < y2):
            if self.clicked:
                dx = self.old_pos.x() - qevent.screenPos().x()
                dy = self.old_pos.y() - qevent.screenPos().y()
                self.move(self.pos().x() - dx, self.pos().y() - dy)

                self.eventSignal.emit(event.Event("info", "moving the window"))

        self.old_pos = qevent.screenPos()
        return QWidget.mouseMoveEvent(self, qevent)

    def applyQss(self, filePath):
        with open(filePath, "r") as f:
            self.setStyleSheet(f.read())

        # QMetaObject.connectSlotsByName(self)
