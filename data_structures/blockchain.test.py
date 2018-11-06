# imports
import unittest
import os
from blockchain import *

class TestBlock(unittest.TestCase):
    def test_constructor(self):
        #file that is going into the blockchain
        filename = "testfile"
        #creating an object of the Blockchain class
        test_blockchain = Blockchain(filename)
        self.assertEqual(test_blockchain.blockfile,filename)
        self.assertTrue(os.path.isfile(filename))
        # Opens the blockchain file and writes '0' to it
        fileobj = open(test_blockchain.blockfile, "wb")
        fileobj.write(b'0')
        fileobj.close()
        # Creates another blockchain with the same filename as test_blockchain
        test_blockchain_2 = Blockchain(test_blockchain.blockfile)
        # Ensures that the file of test_blockchain is not overwritten
        fileobj = open(test_blockchain.blockfile, "rb")
        char = fileobj.read(1)
        fileobj.close()
        self.assertEqual(b'0', char)
        # Deletes the test file
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()