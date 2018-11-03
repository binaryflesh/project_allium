# imports
import unittest
from blockchain import *

class TestBlock(unittest.TestCase):
    def test_constructor(self):
        #file that is going into the blockchain
        filename = "file"
        #creating an object of the Blockchain class
        test_blockchain = Blockchain(filename)
        self.assertEqual(test_blockchain.blockfile,filename)
        

if __name__ == '__main__':
    unittest.main()