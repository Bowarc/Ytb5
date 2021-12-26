__Author__ = "Bowarc\nDiscord: Bowarc#4159"

from PyQt5.QtWidgets import QApplication

import appfiles.uis.ui as ui

import appfiles.utils.app as app
import appfiles.utils.logger as logger

import win32gui
import win32con
import os


def close_console():
    # input("Press enter to hide this console and start the app.")
    user_input = input("Do you want to close the console ?\n[USER]>")
    if user_input.lower().startswith("y") or user_input.lower().startswith("o"):
        the_program_to_hide = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)


with open("RapportDeBugs.txt", "w") as f:
    f.write("")

if __name__ == "__main__":
    # This creates the Main Event Handler for a PyQt Application
    qapp = QApplication([])

    l = logger.logger(level=0)

    app = app.App(l)
    try:
        # close_console()
        app.run()
    except Exception as e:
        import traceback
        import sys
        print(traceback.format_exc())

        with open("RapportDeBugs.txt", "w") as f:
            f.write(traceback.format_exc())
        sys.exit()
    qapp.exec()
