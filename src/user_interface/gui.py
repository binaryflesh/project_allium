import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QPushButton

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

        #create a QWidget and set it as a central widget
        #we need the QWidget because you cannot set a QLayout directly on QMainWindow
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        #set up a GridLayout
        gridLayout = QGridLayout()
        centralWidget.setLayout(gridLayout)


    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui() 
    sys.exit(app.exec_())
