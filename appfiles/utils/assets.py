import os


class Assets:
    def __init__(self):
        self.ressourcePath = "appfiles\\ressources\\"
        pass

    def getImage(self, imageName):
        basePath = os.path.abspath(".")
        relativePath = self.ressourcePath + "imgs\\" + imageName

        return os.path.join(basePath, relativePath)

    def getQss(self, fileName):
        basePath = os.path.abspath(".")
        relativePath = self.ressourcePath + "qss\\" + fileName

        return os.path.join(basePath, relativePath)

    def getFont(self, fileName):
        basePath = os.path.abspath(".")
        relativePath = self.ressourcePath + "fonts\\" + fileName

        return os.path.join(basePath, relativePath)
