# imports
import unittest
import os
from blockchain import *

class TestBlock(unittest.TestCase):
	def setUp(self):
		self.bc = Blockchain("testfile")

	def tearDown(self):
		os.remove("testfile")

	def test_constructor(self):
		filename = "testfile"
		self.assertEqual(self.bc.blockfile,filename)
		self.assertTrue(os.path.isfile(filename))
		# Opens the blockchain file and writes '0' to it
		with open(self.bc.blockfile, 'wb') as fileobj:
		    fileobj.write(b'0')
		# Creates another blockchain with the same filename as test_blockchain
		test_blockchain_2 = Blockchain(self.bc.blockfile)
		# Ensures that the file of test_blockchain is not overwritten
		with open(self.bc.blockfile, 'rb') as fileobj:
		    char = fileobj.read(1)
		self.assertEqual(b'0', char)

	def test_get_size_bytes(self):
		# Testing with integer 4, length should be 4
		testint = 4
		testbytes = pack('I', testint)
		testlen = len(testbytes)
		# Compares result of get_size_bytes() to known size
		size_bytes = get_size_bytes(testbytes)
		self.assertEqual(pack('I', testlen), size_bytes)

if __name__ == '__main__':
    unittest.main()