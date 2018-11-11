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
        self.assertIsInstance(key, bytes)

    def test_generate_public_key(self):
        key = generate_private_key()
        public_key = generate_public_key(key)
        self.assertIsInstance(public_key, bytes)
        signing_key = ecdsa.SigningKey.from_string(key, curve = ecdsa.SECP256k1)
        some_random_hash_string = hash_SHA("some_random_string".encode())
        # Creating a signature that can only be created by the private key holder
        signature = signing_key.sign(some_random_hash_string)
        # Using the public key to varifying the signature
        verifying_key = ecdsa.VerifyingKey.from_string(public_key, ecdsa.SECP256k1)
        # Return if validity is true
        self.assertTrue(verifying_key.verify(signature, some_random_hash_string))



if __name__ == '__main__':
    unittest.main()
