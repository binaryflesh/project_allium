import unittest
from transaction import *
from block import long_to_bytes

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
		# Check if the putput from the function is the same as the concatenation of the two
		self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
