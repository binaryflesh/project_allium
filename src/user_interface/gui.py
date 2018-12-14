import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

class Gui(QMainWindow):

    def __init__(self):
        super().__init__() 
        self.title = ' Allium Wallet'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 280
        self.initUI() 
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui() 
    sys.exit(app.exec_())
