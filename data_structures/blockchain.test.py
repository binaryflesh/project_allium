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
        with open(test_blockchain.blockfile, 'wb') as fileobj:
            fileobj.write(b'0')

        # Creates another blockchain with the same filename as test_blockchain
        test_blockchain_2 = Blockchain(test_blockchain.blockfile)
        # Ensures that the file of test_blockchain is not overwritten
        with open(test_blockchain.blockfile, 'rb') as fileobj:
            char = fileobj.read(1)
        self.assertEqual(b'0', char)
        # Deletes the test file
        os.remove(filename)
        self.assertFalse(os.path.isfile(filename))

if __name__ == '__main__':
    unittest.main()