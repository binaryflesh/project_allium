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

	def test_extract(self):
		# Generates byte strings
		bytes_1 = bytes("VADER: The Force is with you, Young Skywalker. But your not a Jedi yet. (BREATHING CONTINUES)", 'utf-8')
		bytes_2 = bytes("Your destiny... lies with me, Skywalker. Obi-Wan knew is to be true.", 'utf-8')
		bytes_3 = bytes("There is no escape. Don't make me destroy you. Luke. You do not yet realize... your importance. You've only become to... discover your power.", 'utf-8')
		bytes_4 = bytes("Join me... and I will complete your training. With our combined strength... we can end this... destructive conflict... and bring order... to the galaxy.", 'utf-8')
		# Writes byte strings to file
		with open(self.bc.blockfile, 'w+b') as file:			
			file.write(bytes_1)
			file.write(bytes_2)
			file.write(bytes_3)
			file.write(bytes_4)
		# Goal is to pick out third byte string
		expected = bytes("There is no escape. Don't make me destroy you. Luke. You do not yet realize... your importance. You've only become to... discover your power.", 'utf-8')
		# Index of first actual character from bytes_3, minus character name
		index = len(bytes_1) + len(bytes_2) - 7
		# Number of bytes to read is equal to length of bytes_3
		num_bytes = len(bytes_3)
		# 7 Byte offset, due to 7 unecessary bytes at beginning of file
		offset = 7
		# Attempts to extract bytes_3 from written file
		actual = extract(self.bc.blockfile, index, num_bytes, offset)
		# Tests manually written bytestring, and extracted bytestring
		self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()