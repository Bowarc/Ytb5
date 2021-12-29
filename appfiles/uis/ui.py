from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

import appfiles.utils.event as event

UI_CONSOLE_COLORS = {
    "red": (255, 100, 100),
    "green": (100, 255, 100),
    "lightblue": (50, 150, 200)
}

TITLE = "Welcome on Ytb5"


class consoleMessage:
    def __init__(self, text: str, color: (int, int, int), fontSize: int):
        self.text = text
        self.color = color
        self.fontSize = fontSize


class Ytb5(QWidget):
    eventSignal = pyqtSignal(event.Event)

    def __init__(self, assets, logger, downloader):
        QWidget.__init__(self)
        self.setWindowFlags(
            Qt.Widget | QtCore.Qt.FramelessWindowHint)
        self.resize(670, 370)

        self.clicked = False

        self.logger = logger

        self.downloader = downloader

        self.setupUi()
        self.applyQss(assets.getQss(f"main.qss"))
        QtGui.QFontDatabase.addApplicationFont(
            assets.getFont("SAOUI-Regular.otf"))

    def setupUi(self):

        self.setWindowTitle("Window")
        self.setObjectName("Window")

        defaultItemW = 50
        defaultItemH = 20
        defaultDistanceBetweenSameRowItems = 20
        defaultDistanceBetweenItemRows = 15
        defaultItem2X = 100

        titleLabelX = 20
        titleLabelY = 20
        titleLabelW = 300
        titleLabelH = 50

        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setGeometry(QtCore.QRect(
            titleLabelX, titleLabelY, titleLabelW, titleLabelH))
        self.titleLabel.setObjectName("titleLabel")

        quitButtonX = 600
        quitButtonY = 0
        quitButtonW = self.get_size()[0] - quitButtonX
        quitButtonH = 30
        self.quitButton = QtWidgets.QPushButton("Quit", self)
        self.quitButton.setGeometry(QtCore.QRect(
            quitButtonX, quitButtonY, quitButtonW, quitButtonH))
        self.quitButton.clicked.connect(
            lambda: self.eventSignal.emit(event.Event("trigger", "quit")))
        self.quitButton.setObjectName("quitButton")

        formatComboBoxX = defaultItem2X
        formatComboBoxY = 90
        formatComboBoxW = 200
        formatComboBoxH = 30
        self.formatComboBox = QtWidgets.QComboBox(self)
        self.formatComboBox.setGeometry(QtCore.QRect(
            formatComboBoxX, formatComboBoxY, formatComboBoxW, formatComboBoxH))
        for f in self.downloader.downloadFormats:
            self.formatComboBox.addItem(f.title, Qt.AlignCenter)
        for i in range(self.formatComboBox.count()):
            self.formatComboBox.setItemData(
                i, Qt.AlignCenter, Qt.TextAlignmentRole)

        self.formatComboBox.setObjectName("formatComboBox")

        formatLabelW = 45
        formatLabelH = defaultItemH
        formatLabelX = formatComboBoxX - formatLabelW - \
            defaultDistanceBetweenSameRowItems
        # difference between the height of the label and the height of the combo box
        formatLabelY = formatComboBoxY - \
            ((formatLabelH - formatComboBoxH) / 2)

        self.formatLabel = QtWidgets.QLabel("Format:", self)
        self.formatLabel.setGeometry(QtCore.QRect(
            formatLabelX, formatLabelY, formatLabelW, formatLabelH))
        self.formatLabel.setObjectName("formatLabel")

        outputPathDisplayLabelX = defaultItem2X
        outputPathDisplayLabelY = formatComboBoxY + \
            formatComboBoxH + defaultDistanceBetweenItemRows
        outputPathDisplayLabelW = 200
        outputPathDisplayLabelH = defaultItemH

        self.outputPathDisplayLabel = QtWidgets.QLabel(self)
        self.outputPathDisplayLabel.setGeometry(
            QtCore.QRect(outputPathDisplayLabelX, outputPathDisplayLabelY, outputPathDisplayLabelW, outputPathDisplayLabelH))
        self.outputPathDisplayLabel.setObjectName("outputPathDisplayLabel")

        outputPathLabelW = 70
        outputPathLabelH = defaultItemH
        outputPathLabelX = outputPathDisplayLabelX - \
            outputPathLabelW - defaultDistanceBetweenSameRowItems
        outputPathLabelY = outputPathDisplayLabelY
        self.outputPathLabel = QtWidgets.QLabel("Output path: ", self)
        self.outputPathLabel.setGeometry(QtCore.QRect(
            outputPathLabelX, outputPathLabelY, outputPathLabelW, outputPathLabelH))
        self.outputPathLabel.setObjectName("outputPathLabel")

        selectOutputPathButtonX = outputPathDisplayLabelX + \
            outputPathDisplayLabelW + defaultDistanceBetweenSameRowItems
        selectOutputPathButtonY = outputPathDisplayLabelY
        selectOutputPathButtonW = 90
        selectOutputPathButtonH = defaultItemH
        self.selectOutputPathButton = QtWidgets.QPushButton(
            "Select path",  self)
        self.selectOutputPathButton.setGeometry(
            QtCore.QRect(selectOutputPathButtonX, selectOutputPathButtonY, selectOutputPathButtonW, selectOutputPathButtonH))
        self.selectOutputPathButton.clicked.connect(
            lambda: self.eventSignal.emit(event.Event("trigger", "selectOutputPath")))
        self.selectOutputPathButton.setObjectName("selectOutputPathButton")

        linkLineEditX = defaultItem2X
        linkLineEditY = outputPathDisplayLabelY + \
            selectOutputPathButtonH + defaultDistanceBetweenItemRows
        linkLineEditW = 200
        linkLineEditH = defaultItemH

        self.linkLineEdit = QtWidgets.QLineEdit(self)
        self.linkLineEdit.setGeometry(QtCore.QRect(
            linkLineEditX, linkLineEditY, linkLineEditW, linkLineEditH))
        self.linkLineEdit.setObjectName("linkLineEdit")

        linkLabelW = 30
        linkLabelH = defaultItemH
        linkLabelX = linkLineEditX - linkLabelW - defaultDistanceBetweenSameRowItems
        linkLabelY = linkLineEditY
        self.linkLabel = QtWidgets.QLabel("Link:", self)
        self.linkLabel.setGeometry(QtCore.QRect(
            linkLabelX, linkLabelY, linkLabelW, linkLabelH))
        self.linkLabel.setObjectName("linkLabel")

        self.consoleTextEdit = QtWidgets.QTextEdit(self)
        self.consoleTextEdit.setGeometry(QtCore.QRect(-2, 201, 381, 171))
        self.consoleTextEdit.setReadOnly(True)
        # self.consoleTextEdit.setCursor(Qt.ArrowCursor)
        self.consoleTextEdit.viewport().setCursor(Qt.ArrowCursor)
        self.consoleTextEdit.setObjectName("consoleTextEdit")

        self.log(consoleMessage(text="Console connected.",
                                color=UI_CONSOLE_COLORS["green"], fontSize=20))

        downloadButtonX = 460
        downloadButtonY = 200
        downloadButtonW = 111
        downloadButtonH = 61

        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setGeometry(QtCore.QRect(
            downloadButtonX, downloadButtonY, downloadButtonW, downloadButtonH))
        self.progress.setMaximum(100)
        # self.progress.setValue(50)

        self.downloadButton = QtWidgets.QPushButton("Download", self)
        self.downloadButton.setGeometry(QtCore.QRect(
            downloadButtonX, downloadButtonY, downloadButtonW, downloadButtonH))
        self.downloadButton.clicked.connect(
            lambda: self.eventSignal.emit(event.Event("trigger", "downloadButton")))
        self.downloadButton.setObjectName("downloadButton")

        self.outputPathFormater(
            self.downloader.outputPath, self.outputPathDisplayLabel)

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

                if False:  # Send a moving window event
                    self.eventSignal.emit(event.Event(
                        "info", "moving the window"))

        self.old_pos = qevent.screenPos()
        return QWidget.mouseMoveEvent(self, qevent)

    def get_size(self):
        return (self.frameGeometry().width(), self.frameGeometry().height())

    def applyQss(self, filePath):
        with open(filePath, "r") as f:
            self.setStyleSheet(f.read())

    def log(self, msg: consoleMessage):
        console = self.consoleTextEdit
        console.setFontPointSize(msg.fontSize)
        console.setTextColor(QtGui.QColor(
            msg.color[0], msg.color[1], msg.color[2]))
        console.append(f"> {msg.text}")

    def getDownloadFormat(self):
        usedFormat = self.downloader.downloadFormats[0]
        for f in self.downloader.downloadFormats:
            if f.title == self.formatComboBox.currentText():
                usedFormat = f
                break
        return usedFormat

    def outputPathFormater(self, path, targetLabel):
        if not path:
            label.setText("Path not selected")
            return 0

        def generateText(rightSidePathList, leftSidePathList):
            txt = '/'.join(map(str, rightSidePathList)) + \
                "/ .. /" + ('/'.join(map(str, leftSidePathList))) + "/"
            return txt
        dummyLabel = QtWidgets.QLabel(targetLabel)
        dummyLabel.setText("salut")
        # dummyLabel.setVisible(False)
        dummyLabel.deleteLater()
        # self.removeWidget(dummyLabel)
        pathList = path.split("/")

        usablePath = path + "/"

        targetLabel.setText(usablePath)

        rightSidePathList = pathList[:int(len(pathList)/2)]
        leftSidePathList = pathList[int(len(pathList)/2):]

        while targetLabel.fontMetrics().boundingRect(targetLabel.text()).width() > targetLabel.width() - 5:
            if len(rightSidePathList) > 2:

                rightSidePathList.pop(-1)
            else:

                leftSidePathList.pop(0)
            txt = generateText(rightSidePathList, leftSidePathList)
            targetLabel.setText(txt)
        totalPath = generateText(rightSidePathList, leftSidePathList)

        self.logger.debug(f"New formated path: {totalPath}")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        font = QtGui.QFont("SAO UI", 25)
        painter.setFont(font)
        rect = QtCore.QRect(self.titleLabel.x(), self.titleLabel.y(
        ), self.titleLabel.width(), self.titleLabel.height())
        gradient = QtGui.QLinearGradient(rect.topLeft(), rect.topRight())
        gradient.setColorAt(0, QtGui.QColor(20, 200, 200))
        gradient.setColorAt(1, QtGui.QColor(0, 55, 92))
        pen = QtGui.QPen()
        pen.setBrush(gradient)
        painter.setPen(pen)
        painter.drawText(QtCore.QRectF(rect), TITLE,
                         QtGui.QTextOption(QtCore.Qt.AlignCenter))
