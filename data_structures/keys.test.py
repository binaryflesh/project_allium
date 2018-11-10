import unittest
from keys import*

class Test(unittest.TestCase):

    def setUp(self): pass

    def tearDown(self): pass

    def test_generate_private_key(self):
        # calls for function
        key = generate_private_key()
        # checks if the size of the generated key is of length 32 bytes
        self.assertEqual(32,len(key))


if __name__ == '__main__':
    unittest.main()
