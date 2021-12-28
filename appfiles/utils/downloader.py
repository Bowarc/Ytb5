from PyQt5.QtCore import (
    pyqtSignal, QObject
)

import appfiles.utils.event as event
import urllib.request
import yt_dlp
import sys
import os


DEFAULT_OUTPUT_PATH = sys.path[0].replace("\\", "/") + "/UserFiles"


class DownloadFormat:
    def __init__(self, title: str, name: str, ext: str,):
        self.title = title
        self.name = name
        self.ext = ext

    def display(self):
        return f"DownloadFormat object with args [title: {self.title}], [name: {self.name}], [extension: {self.ext}]"


class DownloadArgs:
    def __init__(self, link: str, noPlaylist: bool, path: str, format_: DownloadFormat):
        self.link = link
        self.noPlaylist = noPlaylist
        self.path = path
        self.format = format_

    def display(self):
        return f"DownloadArgs object with args [link: {self.link}], [noPlaylist: {self.noPlaylist}], [path: {self.path}], [format: {self.format.display()}]"

    def isUsable(self):
        usable = True

        if urllib.request.urlopen("https://www.youtube.com/watch?v=2vojalv7gqY").getcode() != 200:
            usable = False
        if not os.path.exists(self.path):
            usable = False

        return usable


class Downloader(QObject):
    eventSignal = pyqtSignal(event.Event)

    def __init__(self, logger, app):
        QObject.__init__(self)

        self.logger = logger

        self.outputPath = DEFAULT_OUTPUT_PATH

        self.app = app

        self.downloadFormats = [
            DownloadFormat(title="Best video and sound quality",
                           name="best", ext="mp4"),
            DownloadFormat(title="Best video quality with no sound",
                           name="bestvideo", ext="mp4"),
            DownloadFormat(title="Best audio quality with no video",
                           name="bestvideo", ext="mp3"),
        ]

        dlArgs = None

    def customYtdlHook(self, d):
        # if d["status"] == "finished":
        #     newEvent = event.Event("info", "downloadEnded")
        #     self.eventSignal.emit(newEvent)

        if d["status"] == "downloading":
            newEvent = event.Event("prcentUpdate", d["_percent_str"].replace('%', '').replace(
                "\x1b[0;94m", "").replace("\x1b[0m", "").replace(" ", ""))
            self.eventSignal.emit(newEvent)

    def downloadHandler(self):
        # link = dlArgs.link
        # newFileName = dlArgs.newFileName
        # noPlaylist = dlArgs.noPlaylist
        dlArgs = self.dlArgs
        if not dlArgs:
            self.eventSignal.emit(event.Event("closeThread", "noDlArgsError"))

            return 1

        if dlArgs.link == "":

            self.eventSignal.emit(event.Event("closeThread", "noLinkError"))

            return 1

        options = {
            "format": dlArgs.format.name,
            "progress_hooks": [self.customYtdlHook],
            "noplaylist": dlArgs.noPlaylist,
            "outtmpl": f"{dlArgs.path}/%(title)s-%(id)s.%(ext)s",
            "quiet": True,
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
        self.dlArgs = None

    def download(self, options, link):
        with yt_dlp.YoutubeDL(options) as ytdl:
            ytdl.download([link])

    def test_signal(self):
        self.eventSignal.emit(event.Event("info", "this is a test signal"))


options = {
    "format": dlArgs.format.name,
    "progress_hooks": [self.customYtdlHook],
    "noplaylist": dlArgs.noPlaylist,
    "outtmpl": f"{dlArgs.path}/%(title)s-%(id)s.%(ext)s",
    "quiet": True,
}
