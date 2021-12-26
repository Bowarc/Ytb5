import enum


class Event:
    def __init__(self, type_: str, msg: str):
        self.type = type_

        self.msg = msg

    def display(self):
        return f"Type: {self.type}, Msg: {self.msg}"
