from PyQt5.QtCore import pyqtSlot, QObject, QThread
from PyQt5.QtWidgets import QFileDialog


import appfiles.utils.downloader as downloader
import appfiles.utils.assets as assets

import appfiles.utils.event as event
import appfiles.uis.ui as ui

import time


class App(QObject):
    def __init__(self, logger):
        QObject.__init__(self)

        self.logger = logger

        self.downloader = downloader.Downloader(self.logger, self)
        self.downloader.eventSignal.connect(self.downloaderEvents)
        self.downloader.test_signal()
        self.downloaderThread = self.createThread("downloader")

        self.assets = assets.Assets()

        self.ui = ui.Ytb5(self.assets, self.logger, self.downloader)
        self.ui.eventSignal.connect(self.uiEvents)

    def run(self):
        self.ui.show()

    def quit(self):
        self.logger.info("closing the app")
        self.ui.close()

        if self.downloaderThread.isRunning():
            self.logger.critical(
                "Closing but the downloader thread is still running")

    @pyqtSlot(event.Event)
    def downloaderEvents(self, event):
        handled = False
        if event.type == "closeThread":
            self.closeThread("downloader")
            if event.msg != "downloadEnd":
                if "customError" in str(event.msg):
                    pass
                    self.logger.info("Closing the downloader thread")
                else:
                    self.logger.critical(f"Closing downloader thread due to a error: <{event.msg}>")
            handled = True
        if event.type == "prcentUpdate":
            value = int(float(event.msg))
            self.ui.progress.setValue(value)
            handled = True

        if event.type == "info":
            if event.msg == "downloadStart":
                self.ui.progress.setVisible(True)
                handled = True
            if event.msg == "downloadEnd":
                self.ui.progress.setVisible(False)
                self.ui.progress.setValue(0)
                self.ui.log(ui.consoleMessage(text="The download has finished",
                                              color=ui.UI_CONSOLE_COLORS["green"], fontSize=15))
                handled = True
        if not handled:
            self.logger.warning(f"Downloader event not handled: {event.display()}")

    @pyqtSlot(event.Event)
    def uiEvents(self, event):
        handled = False
        if event.type == "info":
            if event.msg == "moving the window":

                self.logger.debug("Moving the window")
                self.ui.log(ui.consoleMessage(text="Moving the window!",
                                              color=ui.UI_CONSOLE_COLORS["green"], fontSize=5))
                handled = True
        if event.type == "trigger":
            if event.msg == "downloadButton":
                self.downloadHandle()
                handled = True
            if event.msg == "selectOutputPath":
                self.selectOutputPath()
                handled = True
            if event.msg == "quit":
                self.quit()
                handled = True
        if not handled:
            self.logger.warning(f"Ui event not handled: {event.display()}")
            # print(event.display())

    def downloadHandle(self):
        link = self.ui.linkLineEdit.text()
        format_ = self.ui.getDownloadFormat()
        outputPath = self.downloader.outputPath
        if link == "":
            msg = f"LinkError: Please input a link."
            self.logger.error(msg)
            self.ui.log(ui.consoleMessage(text=msg,
                                          color=ui.UI_CONSOLE_COLORS["red"], fontSize=10))
            return 1
        dlArgs = downloader.DownloadArgs(
            link=link,
            noPlaylist=True,
            path=outputPath,
            format_=format_,
        )
        self.logger.debug(f"Initializing a download.\nOptions: {dlArgs.display()}")
        self.ui.log(ui.consoleMessage(text="Initializing a download. . ",
                                      color=ui.UI_CONSOLE_COLORS["green"], fontSize=14))
        self.ui.log(ui.consoleMessage(text=f"Link: {dlArgs.link}",
                                      color=ui.UI_CONSOLE_COLORS["green"], fontSize=10))
        self.ui.log(ui.consoleMessage(text=f"NoPlaylist: {dlArgs.noPlaylist}",
                                      color=ui.UI_CONSOLE_COLORS["green"], fontSize=10))
        self.ui.log(ui.consoleMessage(text=f"Path: {dlArgs.path}",
                                      color=ui.UI_CONSOLE_COLORS["green"], fontSize=10))
        self.ui.log(ui.consoleMessage(text=f"Format: DownloadFormat object with args:",
                                      color=ui.UI_CONSOLE_COLORS["green"], fontSize=10))

        self.ui.log(ui.consoleMessage(text=f"       Title: {dlArgs.format.title}",
                                      color=ui.UI_CONSOLE_COLORS["green"], fontSize=7))
        self.ui.log(ui.consoleMessage(text=f"       Name: {dlArgs.format.name}",
                                      color=ui.UI_CONSOLE_COLORS["green"], fontSize=7))
        self.ui.log(ui.consoleMessage(text=f"       Extension: {dlArgs.format.ext}",
                                      color=ui.UI_CONSOLE_COLORS["green"], fontSize=7))

        self.ui.log(ui.consoleMessage(text=f"Please look at the button for more informations abt the download status",
                                      color=ui.UI_CONSOLE_COLORS["lightblue"], fontSize=13))

        if dlArgs.isUsable():
            self.downloader.dlArgs = dlArgs
            self.startThread("downloader")
        else:
            self.ui.log(ui.consoleMessage(text=f"[ERROR]: Given dl args are not usable",
                                          color=ui.UI_CONSOLE_COLORS["red"], fontSize=13))
            self.logger.error("Given dl args are not usable")

    def selectOutputPath(self):
        path = str(QFileDialog.getExistingDirectory(
            self.ui, "Select Directory"))
        if not path == "":
            self.logger.debug("ok '{0}'".format(path))
            # UiVars.OutPutFile_Path = path
            self.ui.log(ui.consoleMessage(text="New path loaded",
                                          color=ui.UI_CONSOLE_COLORS["green"], fontSize=12))
            self.ui.log(ui.consoleMessage(text=f"{path}",
                                          color=ui.UI_CONSOLE_COLORS["green"], fontSize=12))
            self.ui.outputPathFormater(path, self.ui.outputPathDisplayLabel)
            self.downloader.outputPath = path

        else:
            self.logger.warning("pas ok '{0}'".format(path))

            self.ui.log(ui.consoleMessage(text=f"Path can't be loaded: '{path}'",
                                          color=ui.UI_CONSOLE_COLORS["red"], fontSize=12))
            self.ui.log(ui.consoleMessage(text=f"Default path will be used'{path}'",
                                          color=ui.UI_CONSOLE_COLORS["red"], fontSize=12))

    def createThread(self, thread):
        if thread == "downloader":

            downloaderThread = QThread()
            self.downloader.moveToThread(downloaderThread)
            downloaderThread.started.connect(self.downloader.downloadHandler)
            return downloaderThread
        else:
            self.logger.critical(f"Given thread name isn't handled: {thread}.")
            return None

    def startThread(self, thread):
        if thread == "downloader":
            self.downloaderThread.start()
            if self.downloaderThread.isRunning():
                self.logger.info("Download thread started")
            else:
                self.logger.error(
                    "Thread error: downloader thread failed to start")
        else:
            self.logger.critical(f"Given thread name isn't handled: {thread}.")

    def closeThread(self, thread):
        if thread == "downloader":
            t1 = time.time()
            if self.downloaderThread.isRunning():
                while self.downloaderThread.isRunning():
                    self.downloaderThread.quit()
                    self.downloaderThread.wait()
                    time.sleep(0.2)
                    if time.time() - t1 > 2:
                        self.downloaderThread.terminate()
                        self.logger.info("Terminating the downloader thread")
                    if time.time()-t1 > 5:
                        self.logger.critical(f"Stuck in {thread} thread stopping method")
                self.logger.info(f"Downloader thread has been stopped")
            else:
                pass
                # self.logger.info(f"Downloader thread has been stopped")
        else:
            self.logger.critical(f"Given thread name isn't handled: {thread}.")
