__Author__ = "Bowarc\nDiscord: Bowarc#4159"

from PyQt5.QtWidgets import QApplication

import appfiles.uis.ui as ui

import appfiles.utils.app as app
import appfiles.utils.logger as logger

import os

if __name__ == "__main__":
    qapp = QApplication([])

    l = logger.logger(level=0, logFile="Ytb5.log")

    app = app.App(l)

    app.run()

    qapp.exec()
