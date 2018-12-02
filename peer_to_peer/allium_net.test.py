import unittest
from networks import *
import time
from allium_net import *
import socket


class Test(unittest.TestCase):
    def setUp(self): pass

    def tearDown(self): pass


    def test_ItCreatesAServer(self):
        """This test checks that a socket instance is createdIP"""
        server = make_server()
        self.assertIsInstance(server,socket.socket)
        server.close()

    def test_ItReturnsTheExpectedIPAddress(self):
        """This test checks that a server created returns an expecgted IP address """
        ip = "0.0.0.0"
        server = make_server()
        self.assertEquals(ip,server.getsockname()[0])
        server.close()

    def test_ItReturnsTheExpectedPortAddress(self):
        """This test checks that a server created returns an expectged port """
        port = 9001
        server = make_server()
        self.assertEqual(port,server.getsockname()[1])
        server.close()

if __name__ == '__main__':
    unittest.main()
