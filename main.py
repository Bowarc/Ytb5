__Author__ = "Bowarc\nDiscord: Bowarc#4159"

from PyQt5.QtWidgets import QApplication

import appfiles.uis.ui as ui

import appfiles.utils.app as app
import appfiles.utils.logger as logger

import os

if __name__ == "__main__":
    # This creates the Main Event Handler for a PyQt Application
    qapp = QApplication([])
    l = logger.logger(level=0, logFile="RapportDeBugs.txt")

    # raise Exception("salut", "a tosu")
    app = app.App(l)

    app.run()

    qapp.exec()
