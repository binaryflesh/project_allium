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
        # Use generated private key to generate a public key
        key = generate_private_key()
        public_key = generate_public_key(key)
        # Checking the right data type
        self.assertIsInstance(public_key, bytes)
        # Generate random string so we can sign it using private key
        signing_key = ecdsa.SigningKey.from_string(key, curve = ecdsa.SECP256k1)
        some_random_hash_string = hash_SHA("some_random_string".encode())
        # Creating a signature that can only be created by the private key holder
        signature = signing_key.sign(some_random_hash_string)
        # Using the public key to varifying the signature
        verifying_key = ecdsa.VerifyingKey.from_string(public_key, ecdsa.SECP256k1)
        # Return if validity is true
        self.assertTrue(verifying_key.verify(signature, some_random_hash_string))

    def test_verify_wrong_public_key(self):
        # Use generated private key to generate a public key
        key = generate_private_key()
        public_key = generate_public_key(key)
        # Generate second public/private key
        key_2 = generate_private_key()
        public_key_2 = generate_public_key(key_2)
        # Checking the right data type
        self.assertIsInstance(public_key, bytes)
        self.assertIsInstance(public_key_2, bytes)
        # Generate random string so we can sign it using private key
        signing_key = ecdsa.SigningKey.from_string(key, curve = ecdsa.SECP256k1)
        some_random_hash_string = hash_SHA("some_random_string".encode())
        # Creating a signature that can only be created by the private key holder
        signature = signing_key.sign(some_random_hash_string)
        # Using the second public key to verifying the signature
        verifying_key = ecdsa.VerifyingKey.from_string(public_key_2, ecdsa.SECP256k1)
        # Return if verify raises BadSiginatureError
        with self.assertRaises(ecdsa.BadSignatureError):
            verifying_key.verify(signature, some_random_hash_string)



if __name__ == '__main__':
    unittest.main()
