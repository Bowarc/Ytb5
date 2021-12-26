from PyQt5.QtCore import pyqtSlot, QObject


import appfiles.utils.downloader as downloader
import appfiles.utils.assets as assets

import appfiles.utils.event as event
import appfiles.uis.ui as ui


class App(QObject):
    def __init__(self, logger):
        QObject.__init__(self)

        self.logger = logger

        self.downloader = downloader.Downloader(self.logger)
        self.downloader.eventSignal.connect(self.downloaderEvents)
        self.downloader.test_signal()

        self.assets = assets.Assets()

        self.ui = ui.Ytb5(self.assets, self.logger)
        self.ui.eventSignal.connect(self.uiEvents)

    def run(self):
        self.ui.show()

    @pyqtSlot(event.Event)
    def downloaderEvents(self, event):
        handled = False
        if not handled:
            print(event.display())

    @pyqtSlot(event.Event)
    def uiEvents(self, event):
        handled = False
        if event.type == "info":
            if event.msg == "moving the window":
                self.logger.debug("Moving the window")
                handled = True
        if not handled:
            print(event.display())
