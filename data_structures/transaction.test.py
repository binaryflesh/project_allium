import unittest
from transaction import *

class Test(unittest.TestCase):

	def test_merkle_empty(self):
		actual = get_merkle_root(deque())
		self.assertEqual(None, actual)

	def test_merkle_single(self):
		expected = hash_SHA('allium'.encode())
		actual = get_merkle_root([hash_SHA('allium'.encode())])
		self.assertEqual(expected, actual)

	def test_merkle_even_gt_zero(self):
		s1 = hash_SHA('allium'.encode())
		s2 = hash_SHA('onion'.encode())
		expected = hash_SHA(s1 + s2)
		actual = get_merkle_root(deque([s1, s2]))
		self.assertEqual(expected, actual)

	def test_merkle_odd_gt_one(self):
		s1 = hash_SHA('allium'.encode())
		s2 = hash_SHA('onion'.encode())
		s3 = hash_SHA('lettuce'.encode())

		expected = deque([hash_SHA(s1 + s2), hash_SHA(s3 + s3)])
		p1 = expected.popleft()
		p2 = expected.popleft()
		expected = hash_SHA(p1 + p2)
			
		actual = get_merkle_root(deque([s1, s2, s3]))
		self.assertEqual(expected, actual)
		
if __name__ == '__main__':
    unittest.main()
