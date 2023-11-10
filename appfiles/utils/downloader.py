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
        return f"DownloadArgs object with args\n[link: {self.link}]\n[noPlaylist: {self.noPlaylist}]\n[path: {self.path}]\n[format: {self.format.display()}]"

    def isUsable(self):
        usable = True
        try:

            code = urllib.request.urlopen(self.link).getcode()
            if code != 200:
                usable = False
            else:
                usable = True
        except Exception as e:
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
                           name="bestaudio", ext="mp3"),
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
            "outtmpl": f"{dlArgs.path}/%(title)s.%(ext)s",
            "quiet": True,
            "noprogress": True,
            'ignoreerrors': True,
            'continue_dl': True,
        }
        try:
            self.eventSignal.emit(event.Event("info", "downloadStart"))
            self.download(options, dlArgs.link)
            self.eventSignal.emit(event.Event("info", "downloadEnd"))
        except Exception as e:
            self.eventSignal.emit(event.Event("closeThread", e))
            self.logger.error(str(e))
            return 1
        self.eventSignal.emit(event.Event("closeThread", "downloadEnd"))
        self.dlArgs = None

    def download(self, options, link):
        with yt_dlp.YoutubeDL(options) as ytdl:
            ytdl.download([link])
