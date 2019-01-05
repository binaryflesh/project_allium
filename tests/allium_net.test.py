import unittest
import sys
import os
import json
sys.path.append(sys.path[0] + "/../src/peer_to_peer")
import time
from allium_net import make_server
from allium_net import get_peer_tracker
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

    def test_ItReturnsTheJSONFile(self):
        """This test checks that the function 'get_peer_tracker'
        returns the contents of a JSON file
        """

        test = open("test.json", "w")

        test_content_dict = {
          "add"   : "user",
          "get"   : "peer",
          "clear" : "everything"
        }

        test.write(json.dumps(test_content_dict))

        test.close()

        self.assertEqual(test_content_dict, get_peer_tracker('test.json'))

        os.remove('test.json')

if __name__ == '__main__':
    unittest.main()
