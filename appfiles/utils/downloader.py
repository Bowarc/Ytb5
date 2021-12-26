from PyQt5.QtCore import (
    pyqtSignal, QObject
)

import appfiles.utils.event as event

import sys


class DownloadFormat:
    def __init__(self, title: str, message: str, name: str):
        self.title = title
        self.message = message
        self.name = name


class DownloadArgs:
    def __init__(self, link: str, noPlaylist: bool, path: str, format_: DownloadFormat):
        self.link = link
        self.noPlaylist = noPlaylist
        self.path = path
        self.format = format_


class Downloader(QObject):
    eventSignal = pyqtSignal(event.Event)

    def __init__(self, logger):
        QObject.__init__(self)

        self.logger = logger

    def customYtdlHook(self, d):
        # if d["status"] == "finished":
        #     newEvent = event.Event("info", "downloadEnded")
        #     self.eventSignal.emit(newEvent)

        if d["status"] == "downloading":
            newEvent = event.Event("prcentUpdate", d["_percent_str"].replace('%', '').replace(
                "\x1b[0;94m", "").replace("\x1b[0m", "").replace(" ", ""))
            self.eventSignal.emit(newEvent)

    def downloadHandler(self, dlArgs):
        # link = dlArgs.link
        # newFileName = dlArgs.newFileName
        # noPlaylist = dlArgs.noPlaylist

        if dlArgs.link == "":

            self.eventSignal.emit(event.Event("closeThread", "noLinkError"))

            return 1

        options = {
            "format": dlArgs.format.name,
            "progress_hooks": [self.customYtdlHook],
            "noplaylist": dlArgs.noPlaylist,
            "outtmpl": f"{dlArgs.path}/%(title)s-%(id)s.%(ext)s",
            'quiet': True,
        }
        try:
            self.eventSignal.emit(event.Event("info", "downloadStart"))
            self.download(options, dlArgs.link)
            self.eventSignal.emit(event.Event("info", "downloadEnd"))
        except Exception as e:
            self.eventSignal.emit(event.Event("closeThread", e))
            print(e)
            return 1
        self.eventSignal.emit(event.Event("closeThread", "downloadEnd"))

    def download(self, options, link):
        with yt_dlp.YoutubeDl(options) as ytdl:
            ytdl.download([link])

    def test_signal(self):
        self.eventSignal.emit(event.Event("info", "this is a test signal"))
