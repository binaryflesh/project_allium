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

    def test_generate_pk_hash(self):
        # Use generated private key to generate a public key
        key = generate_private_key()
        public_key = generate_public_key(key)
        # Generate pk hash from public key
        pk_hash = generate_pk_hash(public_key)
        # Checks if pk hash is a bite string
        self.assertIsInstance(pk_hash, bytes)

    def test_key_set_to_json_format(self):
        #test encoding and decoding at the same time
        #generate key set 
        key_set = generate_key_set()
        encoded_set = key_set_to_json_format(key_set)   
        self.assertNotEqual(key_set, key_set_to_json_format)
        self.assertEqual(key_set, json_format_to_key_set(encoded_set))

    def test_store_keys(self):
        store_keys()
        #open the file 
        with open('keys.json', 'r') as json_file: 
            key_set = json.load(json_file)
        #check for the existence of keys
        self.assertTrue('public_key' in key_set) 
        self.assertTrue('private_key' in key_set)
        self.assertTrue('pk_hash' in key_set)
        os.remove('keys.json')
        
    def test_load_keys(self):
        store_keys()
        key_set = load_keys()
        self.assertTrue('public_key' in key_set) 
        self.assertTrue('private_key' in key_set)
        self.assertTrue('pk_hash' in key_set)
        os.remove('keys.json')

    def test_startup_keys(self):
        # Tests if startup_keys() works with a keys.json file
        store_keys()
        key_set = startup_keys()
        self.assertTrue('public_key' in key_set) 
        self.assertTrue('private_key' in key_set)
        self.assertTrue('pk_hash' in key_set)
        # Tests if startup_keys() works without a keys.json file
        os.remove('keys.json')
        key_set = startup_keys()
        self.assertTrue('public_key' in key_set) 
        self.assertTrue('private_key' in key_set)
        self.assertTrue('pk_hash' in key_set)
        os.remove('keys.json')

if __name__ == '__main__':
    unittest.main()
