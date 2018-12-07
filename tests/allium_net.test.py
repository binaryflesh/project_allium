import unittest
import sys
sys.path.append(sys.path[0] + "/../src/peer_to_peer")
from networks import *
import time
from allium_net import *
import socket


class Test(unittest.TestCase):
    port = 9001

    def setUp(self):
        self.server = make_server(self.port)

    def tearDown(self):
        self.server.close()


    def test_ItCreatesAServer(self):
        """This test checks that a socket instance is createdIP"""
        self.assertIsInstance(self.server,socket.socket)

    def test_ItReturnsTheExpectedIPAddress(self):
        """This test checks that a server created returns an expecgted IP address """
        ip = "0.0.0.0"
        self.assertEqual(ip, self.server.getsockname()[0])

    def test_ItReturnsTheExpectedPortAddress(self):
        """This test checks that a server created returns an expectged port """
        self.assertEqual(self.port, self.server.getsockname()[1])

if __name__ == '__main__':
    unittest.main()
