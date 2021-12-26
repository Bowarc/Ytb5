import enum


class Event:
    def __init__(self, type_: str, msg: str):
        self.type = type_

        self.msg = msg
