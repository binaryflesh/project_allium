import sys
sys.path.append(sys.path[0] + "/../")
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QPushButton, QAction
from PyQt5.QtGui import QFont, QImage, QPalette, QBrush, QPixmap
from PyQt5 import QtCore

class Gui(QMainWindow):

    def __init__(self):
        super().__init__() 
        self.title = ' Allium Wallet'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 400
        self.initUI() 
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        #create a QWidget and set it as a central widget
        #we need the QWidget because you cannot set a QLayout directly on QMainWindow
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        #set up a GridLayout
        gridLayout = QGridLayout()
        centralWidget.setLayout(gridLayout)
        #Sets the background image of the page to qbetdark.png
        self.setBackgroundImage()
        self.initFileBar()

    def setBackgroundImage(self):
        # Creates a QImage Object with the image file
        oImage = QImage(sys.path[0] + "/qbertdark.png")
        # Scales the image to the size of the window
        sImage = oImage.scaled(QtCore.QSize(self.width, self.height))
        # Creates a palette, sets the brush to a brush with the scaled image
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        # Sets window palette to this palette
        self.setPalette(palette)

    def initFileBar(self):
    	# Creates a menubar
        self.mainMenu = self.menuBar()
        # Sets the background of filebar to grey and text to white
        self.mainMenu.setStyleSheet("""
                            QWidget{
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200)
                            }""")
        # FILE TAB ========================================================
        self.fileMenu = self.mainMenu.addMenu('File')

        # VIEW TAB ========================================================
        self.viewMenu = self.mainMenu.addMenu('View')

        # TOOLS TAB =======================================================
        self.toolsMenu = self.mainMenu.addMenu('Settings')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui() 
    sys.exit(app.exec_())
