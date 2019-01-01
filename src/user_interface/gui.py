import sys
sys.path.append(sys.path[0] + "/../")
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QPushButton, QAction, QLabel, QHBoxLayout, QFrame
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

        #set up fonts to be used
        self.bigFont = QFont("Arial", 16,QFont.Bold)
        self.normalFont = QFont("Arial", 12)

        # Sets the background image of the page to qbetdark.png
        self.setBackgroundImage()
        # Initializes the file bar
        self.initFileBar()
        # Initializes the mine button
        self.initMineButton()
        # Initializes the transaction button
        self.initTxButton()

        #set up a GridLayout
        gridLayout = QGridLayout()
        #gridlayout.addWidget(widget, startRow, endRow, startCol, endCol)
        # Places the Mine Button in the top left corner of the screen
        gridLayout.addWidget(self.mineButton, 0, 0)
        # Places the Transaction Button in the top left corner of the screen
        gridLayout.addWidget(self.txButton, 0, 2)

        #create a QWidget and set it as a central widget
        #we need the QWidget because you cannot set a QLayout directly on QMainWindow
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(gridLayout)

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

    def initMineButton(self):
        # Creates a mine button, sets its text, font and style
        self.mineButton = QPushButton("Mine", self)
        self.mineButton.setFont(self.bigFont)
        self.mineButton.setStyleSheet("""
                            QWidget{
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200)
                            }""")
        #self.mineButton.clicked.connect("""MINE FUNCTION""")
        # Sets fixed size for mine button
        self.mineButton.setFixedWidth(200)
        self.mineButton.setFixedHeight(50)

    def initTxButton(self):
        # Creates a transaction button, sets its text, font and style
        self.txButton = QPushButton("Transaction", self)
        self.txButton.setFont(self.bigFont)
        self.txButton.setStyleSheet("""
                            QWidget{
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200)
                            }""")
        #self.txButton.clicked.connect("""OPEN TX WINDOW""")
        # Sets fixed size for transaction button
        self.txButton.setFixedWidth(200)
        self.txButton.setFixedHeight(50)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui() 
    sys.exit(app.exec_())
