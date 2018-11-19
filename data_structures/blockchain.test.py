# imports
import unittest
import os
from blockchain import *
from block import mine, hash_SHA, bytes_to_int

class TestBlock(unittest.TestCase):
	def setUp(self):
		self.bc = Blockchain("testfile.db")

	def tearDown(self):
		os.remove("testfile.db")
	
	def test_constructor(self):
		filename = "testfile.db"
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
	
	def test_extract(self):
		# Generates byte strings
		bytes_1 = bytes("VADER: The Force is with you, Young Skywalker. But your not a Jedi yet. (BREATHING CONTINUES)", 'utf-8')
		bytes_2 = bytes("Your destiny... lies with me, Skywalker. Obi-Wan knew is to be true.", 'utf-8')
		bytes_3 = bytes("There is no escape. Don't make me destroy you. Luke. You do not yet realize... your importance. You've only become to... discover your power.", 'utf-8')
		bytes_4 = bytes("Join me... and I will complete your training. With our combined strength... we can end this... destructive conflict... and bring order... to the galaxy.", 'utf-8')
		# Writes byte strings to file
		with open(self.bc.blockfile, 'ab') as file:			
			file.write(bytes_1)
			file.write(bytes_2)
			file.write(bytes_3)
			file.write(bytes_4)
		# Goal is to pick out third byte string
		expected = bytes("There is no escape. Don't make me destroy you. Luke. You do not yet realize... your importance. You've only become to... discover your power.", 'utf-8')
		# Index of first actual character from bytes_3, minus character name
		index = len(bytes_1) + len(bytes_2)
		# Number of bytes to read is equal to length of bytes_3
		num_bytes = len(bytes_3)
		# Attempts to extract bytes_3 from written file
		actual = extract(self.bc.blockfile, index, num_bytes)
		# Tests manually written bytestring, and extracted bytestring
		self.assertEqual(expected, actual)

	def test_add_block1(self):
		target = 10**72     
		data = hash_SHA("Testing block".encode())   
		prev_hash = hash_SHA("0123456789ABCDEF".encode())
		
		#Create a block using .mine()
		block = mine(prev_hash, data, target)
		# Creates expected with preceding magic_bytes and size values and block
		expected = magic_bytes + get_size_bytes(block) + block
		#Get size of block
		size = bytes_to_int(get_size_bytes(expected))
		# Add block to blockchain
		self.bc.add_block(block)
		# Extracts block from blockchain
		actual = extract(self.bc.blockfile, 0, size)
		# Confirms that extracted block is identical to actual block
		self.assertEqual(expected, actual)

	def test_add_block2(self):
		target = 10**72     
		
		# Creates 4 blocks and add to file
		b1 = mine(hash_SHA("Root".encode()), "Block1".encode(), target)
		self.bc.add_block(b1)
		b2 = mine(hash_SHA("Block1".encode()), "Block2".encode(), target)
		self.bc.add_block(b2)
		b3 = mine(hash_SHA("Block2".encode()), "Block3".encode(), target)
		self.bc.add_block(b3)
		b4 = mine(hash_SHA("Block3".encode()), "Block4".encode(), target)
		self.bc.add_block(b4)
		# Creates expected with preceding magic_bytes and size values
		# Split into multiple lines for readability
		expected = magic_bytes + get_size_bytes(b1) + b1
		expected = expected + magic_bytes + get_size_bytes(b2) + b2
		expected = expected + magic_bytes + get_size_bytes(b3) + b3
		expected = expected + magic_bytes + get_size_bytes(b4) + b4
		#Get size of block
		size = bytes_to_int(get_size_bytes(expected))
		# Extracts blocks from blockchain
		actual = extract(self.bc.blockfile, 0, size)
		# Confirms that extracted blocks is identical to actual blocks
		self.assertEqual(expected, actual)

if __name__ == '__main__':
	unittest.main()