from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap


class Window(QWidget):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.title = 'Png Parser'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        label = QLabel(self)
        pixmap = QPixmap(self.name)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()