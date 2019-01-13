import sys
sys.path.append(sys.path[0] + "/../")
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QPushButton, QAction, QLabel, QHBoxLayout, QFrame, QDialog, QLineEdit, QComboBox
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
        # Initializes the wallet label
        self.initWalletFrame()
        # Initializes the IP label
        self.initIPFrame()
        # Initializes the transaction dialog
        self.initTxDialog()

        #set up a GridLayout
        gridLayout = QGridLayout()
        #gridlayout.addWidget(widget, startRow, startCol, #rows, #cols)
        # Places the Mine Button in the top left corner of the screen
        gridLayout.addWidget(self.mineButton, 0, 0)
        # Places the Transaction Button in the top left corner of the screen
        gridLayout.addWidget(self.txButton, 0, 2)
        # Places Wallet label between mine and transaction button
        gridLayout.addWidget(self.walletFrame, 0, 1)
        # Places the IP label below the mine label
        gridLayout.addWidget(self.IPFrame, 1, 0)

        #create a QWidget and set it as a central widget
        #we need the QWidget because you cannot set a QLayout directly on QMainWindow
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(gridLayout)

#===MAIN DIALOG=======================================================
#=====================================================================
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
                                color: rgb(200, 200, 200);
                                selection-background-color: rgb(130, 130, 130);
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
                                color: rgb(200, 200, 200);
                                selection-background-color: rgb(130, 130, 130);
                            }""")
        self.txButton.clicked.connect(self.showTxDialog)
        # Sets fixed size for transaction button
        self.txButton.setFixedWidth(200)
        self.txButton.setFixedHeight(50)

    def initWalletFrame(self):
        self.walletContent = QLabel('₩ 0.00', self)
        self.walletContent.setAlignment(QtCore.Qt.AlignCenter)
        self.walletContent.setFont(self.bigFont)
        walletLayout = QHBoxLayout()
        walletLayout.addWidget(self.walletContent)
        self.walletFrame = QFrame(self)
        #Set up the style of the main Label
        self.walletFrame.setStyleSheet("""
                          QFrame {
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200);
                                border-radius: 12px;
                                padding: 6px
                        }""")
        self.walletFrame.setLayout(walletLayout)

    def initIPFrame(self):
        self.IPAddress = QLabel("Offline", self)
        self.IPAddress.setAlignment(QtCore.Qt.AlignCenter)
        self.IPAddress.setFont(self.bigFont)
        IPLayout = QHBoxLayout()
        IPLayout.addWidget(self.IPAddress)
        self.IPFrame = QFrame(self)
        #Set up the style of the main Label
        self.IPFrame.setStyleSheet("""
                          QFrame {
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200);
                                border-radius: 12px;
                                padding: 6px
                        }""")
        self.IPFrame.setLayout(IPLayout)
        self.IPFrame.setFixedWidth(200)
        self.IPFrame.setFixedHeight(60)

#===TRANSACTION DIALOG================================================
#=====================================================================
    def initTxDialog(self):
        self.txDialog = QDialog()
        self.txDialog.setWindowTitle("Transaction")
        self.txDialog.setFixedSize(735, 170)
        # Creates a QImage Object with the image file
        oImage = QImage(sys.path[0] + "/qbertdark.png")
        # Creates a palette, sets the brush to a brush with the original image
        palette = QPalette()
        palette.setBrush(10, QBrush(oImage))
        # Sets window palette to this palette
        self.txDialog.setPalette(palette)

        # Initializes all elements on this dialog
        self.initTxInputs()
        self.initTxContactList()
        self.initTxSummary()
        self.initTxOKButton()
        self.initTxCancelButton()

    def initTxInputs(self):
        # Initializes input lines and titles
        recTitle = QLabel("Send To:", self.txDialog)
        recTitle.setFont(self.normalFont)
        valTitle = QLabel("Value:", self.txDialog)
        valTitle.setFont(self.normalFont)
        self.recInput = QLineEdit(self.txDialog)
        self.recInput.setStyleSheet("""
                        QLineEdit {
                                color: rgb(200, 200, 200);
                                border: 1px solid gray;
                                border-radius: 5px;
                                padding: 0 8px;
                                background: rgb(17, 17, 17);
                                selection-background-color: rgb(130, 130, 130);
                        }""")
        self.recInput.resize(1000, 30)
        self.valInput = QLineEdit(self.txDialog)
        self.valInput.setStyleSheet("""
                        QLineEdit {
                                color: rgb(200, 200, 200);
                                border: 1px solid gray;
                                border-radius: 5px;
                                padding: 0 8px;
                                background: rgb(17, 17, 17);
                                selection-background-color: rgb(130, 130, 130);
                        }""")
        # Set up a GridLayout 
        txGridLayout = QGridLayout()
        txGridLayout.addWidget(recTitle, 0 , 0)
        txGridLayout.addWidget(self.recInput, 0 , 1)
        txGridLayout.addWidget(valTitle, 1, 0)
        txGridLayout.addWidget(self.valInput, 1 , 1)

        # Sets the grid layout to a frame
        self.txInputFrame = QFrame(self.txDialog)
        self.txInputFrame.setLayout(txGridLayout)
        self.txInputFrame.setStyleSheet("""
                          QFrame {
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200);
                                border-radius: 12px;
                                padding: 6px
                        }""")
        # Places the frame on the dialog
        self.txInputFrame.move(15, 15)
        self.txInputFrame.resize(350, 100)

    def initTxContactList(self):
        # Creates a drop down box
        self.txContactList = QComboBox(self.txDialog)
        # Centers the text in the combo box
        self.txContactList.setEditable(True)
        self.ledit = self.txContactList.lineEdit()
        self.ledit.setAlignment(QtCore.Qt.AlignCenter)
        # Sets the editable portion of the combo box to read only
        self.ledit.setReadOnly(True)
        self.txContactList.addItem("Example")
        self.txContactList.setStyleSheet("""
                            QComboBox {
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200);
                                padding: 6px;
                                border: 1px solid gray;
                                border-radius: 5px;
                                selection-background-color: rgb(130, 130, 130);
                                    }
                            QComboBox QAbstractItemView {
                                background-color: rgb(17, 17, 17);
                                color: rgb(200, 200, 200);
                                selection-background-color: rgb(30, 30, 30);
                                    }""")

        # Creates a Title Label
        contactTitle = QLabel("Contact List", self.txDialog)
        contactTitle.setFont(self.normalFont)
        contactTitle.setAlignment(QtCore.Qt.AlignCenter)

        # Set up a GridLayout 
        contactGridLayout = QGridLayout()
        contactGridLayout.addWidget(contactTitle, 0, 0)
        contactGridLayout.addWidget(self.txContactList, 1, 0)

        # Sets the grid layout to a frame
        self.contactFrame = QFrame(self.txDialog)
        self.contactFrame.setLayout(contactGridLayout)
        self.contactFrame.setStyleSheet("""
                          QFrame {
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200);
                                border-radius: 12px;
                                padding: 6px
                        }""")
        # Places the frame on the dialog
        self.contactFrame.move(380, 15)
        self.contactFrame.resize(200, 100)

    def initTxSummary(self):
        # Creates labels containing current wallet value, transaction value, and resulting value
        self.walletValLabel = QLabel("0.00", self.txDialog)
        self.txValLabel = QLabel("0.00", self.txDialog)
        self.resultValLabel = QLabel("0.00", self.txDialog)
        # Creates labels containing a dash and dividing line
        dashLabel = QLabel("-", self.txDialog)
        lineLabel = QLabel("____________________", self.txDialog)

        # Creates a grid layout and adds the labels to it
        summGridLayout = QGridLayout()
        summGridLayout.addWidget(self.walletValLabel, 0, 1)
        summGridLayout.addWidget(dashLabel, 1, 0)
        summGridLayout.addWidget(self.txValLabel, 1, 1)
        summGridLayout.addWidget(lineLabel, 2, 0, 1, 2)
        summGridLayout.addWidget(self.resultValLabel, 3, 1)

        # Sets the grid layout to a frame
        self.summFrame = QFrame(self.txDialog)
        self.summFrame.setLayout(summGridLayout)
        self.summFrame.setStyleSheet("""
                          QFrame {
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200);
                                border-radius: 12px;
                        }""")

        # Places the frame on the dialog
        self.summFrame.move(595, 15)
        self.summFrame.resize(125, 100)

    def initTxOKButton(self):
        # Initialize OK Button, and set style
        self.txOKButton = QPushButton("OK", self.txDialog)
        self.txOKButton.setFont(self.normalFont)
        self.txOKButton.setStyleSheet("""
                            QWidget{
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200);
                                selection-background-color: rgb(130, 130, 130);
                            }""")

        # Connects button to function
        #self.txOKButton.clicked.connect("""START TRANSACTION FUNCTION""")

        # Correctly sizes and moves button. Starts disabled.
        self.txOKButton.resize(100, 30)
        self.txOKButton.move(15, 128)
        self.txOKButton.setEnabled(False)

    def initTxCancelButton(self):
        # Initialize Cancel Button, and set style
        self.txCancelButton = QPushButton("Cancel", self.txDialog)
        self.txCancelButton.setFont(self.normalFont)
        self.txCancelButton.setStyleSheet("""
                            QWidget{
                                background-color: rgb(20, 20, 20);
                                color: rgb(200, 200, 200);
                                selection-background-color: rgb(130, 130, 130);
                            }""")

        # Connects button to close window
        self.txCancelButton.clicked.connect(self.txDialog.reject)

        # Correctly sizes and moves button.
        self.txCancelButton.resize(100, 30)
        self.txCancelButton.move(130, 128)

    def resetTxDialog(self):
        # This should reset all text boxes, buttons, and labels in this window
        self.recInput.setText("")
        self.valInput.setText("")
        self.txOKButton.setEnabled(False)

    def showTxDialog(self):
        self.resetTxDialog()
        self.txDialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui() 
    sys.exit(app.exec_())

