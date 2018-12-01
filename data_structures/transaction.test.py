import unittest
from transaction import *
from block import long_to_bytes
from keys import generate_key_set

class Test(unittest.TestCase):

	# Case 1: empty collection
	def test_merkle_empty(self):
		actual = get_merkle_root(deque())
		# should return None
		self.assertEqual(None, actual)

	# Case 2: singleton
	def test_merkle_single(self):
		expected = hash_SHA('allium'.encode())
		actual = get_merkle_root([hash_SHA('allium'.encode())])
		# should trigger base case of recursive helper only
		self.assertEqual(expected, actual)

	# Case 3: even number (x > 0) number of elements
	def test_merkle_even_gt_zero(self):
		s1 = hash_SHA('allium'.encode())
		s2 = hash_SHA('onion'.encode())
		expected = hash_SHA(s1 + s2)
		actual = get_merkle_root(deque([s1, s2]))
		# should pair up elements and hash them
		self.assertEqual(expected, actual)

	# Case 4: odd number (x > 1) number of elements
	def test_merkle_odd_gt_one(self):
		s1 = hash_SHA('allium'.encode())
		s2 = hash_SHA('onion'.encode())
		s3 = hash_SHA('lettuce'.encode())

		# should create a copy of last element and
		# append it to the deque, creating an even
		# length collection to hash
		expected = deque([hash_SHA(s1 + s2), hash_SHA(s3 + s3)])
		p1 = expected.popleft()
		p2 = expected.popleft()
		expected = hash_SHA(p1 + p2)
			
		# now should pair up elements and hash them
		actual = get_merkle_root(deque([s1, s2, s3]))
		self.assertEqual(expected, actual)
		
	# test create_output
	def test_create_output(self):
		value = 50000000
		recipient= hash_SHA('recipient'.encode())
		# Put value and recipient into create_output function
		actual = create_output(value, recipient)
		expected = long_to_bytes(value) + recipient
		# Check if the output from the function is the same as the concatenation of the two
		self.assertEqual(expected, actual)

	def test_sign_transaction(self):
		# manually created components of unsigned transaction hash
		prev_hash = hash_SHA('previous'.encode())
		prev_tx_locking_script = create_output(30000000,hash_SHA('recipient'.encode()))
		new_tx_output = hash_SHA('new_output'.encode())
		# concatenating above components
		p1 = prev_hash + prev_tx_locking_script + new_tx_output
		# creates made up unsigned transaction hash
		unsigned_tx_hash = hash_SHA(p1)
		# getting a private and public key
		key_dict = generate_key_set()
		priv_key = key_dict["private_key"]
		pub_key = key_dict["public_key"]
		# creating a verification key
		verifying_key = ecdsa.VerifyingKey.from_string(pub_key, ecdsa.SECP256k1)
		# creating a signed transaction using the sign transaction function
		signed_tx = sign_transaction(priv_key,prev_hash,prev_tx_locking_script,new_tx_output)
		# Verifying the verification key works
		self.assertTrue(verifying_key.verify(signed_tx, unsigned_tx_hash))

	def test_create_input(self):
		# Create key set
		key_dict = generate_key_set()
		priv_key = key_dict["private_key"]
		public_key = key_dict["public_key"]
		# Create transaction signature
		previous_tx_hash = hash_SHA('previous'.encode())
		prev_tx_locking_script = create_output(30000000, hash_SHA('recipient'.encode()))
		new_tx_output = hash_SHA('new_output'.encode())
		signature = sign_transaction(priv_key, previous_tx_hash, prev_tx_locking_script, new_tx_output)
		# Create index value
		index = 2
		# Concatenate values together
		unlocking_script = signature + public_key
		index_short = short_to_bytes(index)
		expected = previous_tx_hash + index_short + unlocking_script
		# Run same values through function
		actual = create_input(previous_tx_hash, index, signature, public_key)
		# Check if function equals the concatenation of the values
		self.assertEqual(expected, actual)

	def test_parse_input(self):
		# Create key set
		key_dict = generate_key_set()
		priv_key = key_dict["private_key"]
		public_key = key_dict["public_key"]
		# Create transaction signature
		previous_tx_hash = hash_SHA('previous'.encode())
		prev_tx_locking_script = create_output(30000000, hash_SHA('recipient'.encode()))
		new_tx_output = hash_SHA('new_output'.encode())
		signature = sign_transaction(priv_key, previous_tx_hash, prev_tx_locking_script, new_tx_output)
		# Create index value
		index = 2
		# Create input and parse
		parsed_input = parse_input(create_input(previous_tx_hash, index, signature, public_key))

		self.assertEqual(parsed_input["previous_tx_hash"], previous_tx_hash)
		self.assertEqual(parsed_input["index"], index)
		self.assertEqual(parsed_input["signature"], signature)
		self.assertEqual(parsed_input["public_key"], public_key)

if __name__ == '__main__':
    unittest.main()
