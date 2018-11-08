#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QGridLayout, QFrame, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore
import socket

class Gui(QMainWindow):
    '''Create a window and display the title of the project in the center'''

    def __init__(self, port = 9001):
        super().__init__()
        self.title = ''
        self.left = 100
        self.top = 100
        self.width = 700
        self.height = 280
        self.port = port
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #set up fonts to be used
        self.bigFont = QFont("Times", 18,QFont.Bold)
        self.normalFont = QFont("Time", 12)

        #create a QWidget and set it as a central widget
        #we need the QWidget becasue you cannot set a QLayout directly on QMainWindow
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        #set up a GridLayout
        gridLayout = QGridLayout()

        label = QLabel('SIG Blockchain Project', self)
        #Set up the style of the main Label
        label.setStyleSheet("""
                          QWidget {
                                border: 2px solid black;
                                border-radius:13px;
                                padding: 6px;
                                background-color: rgb(255, 255, 255);
                        }""")
        label.setFont(self.bigFont)
        gridLayout.addWidget(label, 0, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        #set up various gui components

        gridLayout.addWidget(self.createIPFrame(), 0, 1)

        gridLayout.addWidget(self.createStatusFrame(), 1, 1)

        gridLayout.addWidget(self.createPeersFrame(), 2, 1)

        centralWidget.setLayout(gridLayout)

        # Set window background color
        self.setStyleSheet("QMainWindow {background: 'black';}");

        self.show()

    def createIPFrame(self):
        IPFrame = QFrame(self)
        IPFrame.setObjectName("IPFrame")
        IPFrame.setStyleSheet("""
                            QWidget#IPFrame{
                                border: 2px solid black;
                                border-radius: 15px;
                                padding: 3px;
                                background-color: rgb(255, 255, 255);
                        }""")
        IPLayout = QHBoxLayout()
        lblIp = QLabel("IP:Port ", IPFrame)
        lblIp.setFont(self.normalFont)
        IPLayout.addWidget(lblIp)
        self.IPLabel = QLabel(concat_ip_port(self.port), IPFrame)
        self.IPLabel.setFont(self.normalFont)
        IPLayout.addWidget(self.IPLabel)
        IPFrame.setLayout(IPLayout)
        return IPFrame

    def createStatusFrame(self):
        StatusFrame = QFrame(self)
        StatusFrame.setObjectName("StatusFrame")
        StatusFrame.setStyleSheet("""
                            QWidget#StatusFrame{
                                border: 2px solid black;
                                border-radius: 15px;
                                padding: 3px;
                                background-color: rgb(255, 255, 255);
                        }
        """)
        StatusLayout = QHBoxLayout()
        lblStatus = QLabel("Status: ", StatusFrame)
        lblStatus.setFont(self.normalFont)
        self.StatusLabel = QLabel("Offline", StatusFrame)
        self.StatusLabel.setFont(self.normalFont)
        StatusLayout.addWidget(lblStatus)
        StatusLayout.addWidget(self.StatusLabel)
        StatusFrame.setLayout(StatusLayout)
        return StatusFrame

    def createPeersFrame(self):
        PeersFrame = QFrame(self)
        PeersFrame.setObjectName("PeersFrame")
        PeersFrame.setStyleSheet("""
                            QWidget#PeersFrame{
                                border: 2px solid black;
                                border-radius: 15px;
                                padding: 3px;
                                background-color: rgb(255, 255, 255);
                        }
        """)
        PeersLayout = QHBoxLayout()
        lblPeers = QLabel("Peers: ", PeersFrame)
        lblPeers.setFont(self.normalFont)
        self.PeersLabel = QLabel("0", PeersFrame)
        self.PeersLabel.setFont(self.normalFont)
        PeersLayout.addWidget(lblPeers)
        PeersLayout.addWidget(self.PeersLabel)
        PeersFrame.setLayout(PeersLayout)
        return PeersFrame

def get_ip() :

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.google.com', 80))

    ip = s.getsockname()[0]


    s.close()

    return ip

def concat_ip_port(port) :
    return str(get_ip()) + ":" + str(port)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    port = 9001
    ex = Gui(port)
    sys.exit(app.exec_())
