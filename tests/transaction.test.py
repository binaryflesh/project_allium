import unittest
import sys
sys.path.append(sys.path[0] + '/../src/data_structures')
from transaction import *
from block import int_to_bytes, short_to_bytes, long_to_bytes, hash_SHA
from keys import generate_key_set
from collections import deque

class Test(unittest.TestCase):

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
		unsigned_tx = prev_hash + prev_tx_locking_script + new_tx_output
		# creates made up unsigned transaction hash
		unsigned_tx_hash = hash_SHA(unsigned_tx)
		# getting a private and public key
		key_dict = generate_key_set()
		priv_key = key_dict["private_key"]
		pub_key = key_dict["public_key"]
		# creating a verification key
		verifying_key = ecdsa.VerifyingKey.from_string(pub_key, ecdsa.SECP256k1)
		# creating a signed transaction using the sign transaction function
		signed_tx = sign_transaction(unsigned_tx, priv_key)
		# Verifying the verification key works
		self.assertTrue(verifying_key.verify(signed_tx, unsigned_tx_hash))

	@DeprecationWarning
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

	@DeprecationWarning
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

	def test_parse_output(self):
		value = 50000000
		recipient = hash_SHA('recipient'.encode())
		# Create output and parse
		parsed_output = parse_output(create_output(value, recipient))
		self.assertEqual(parsed_output["value"], value)
		self.assertEqual(parsed_output["recipient"], recipient)

	def test_cat_input_fields(self):
		prev_hash = hash_SHA('previous'.encode())
		output_index = 128 
		prev_recipient = hash_SHA('recipient'.encode())

		actualResults = cat_input_fields(prev_hash, output_index, prev_recipient)
		expectedResults = prev_hash + short_to_bytes(output_index) + prev_recipient 
		self.assertEqual(actualResults, expectedResults)

	def test_cat_tx_fields_single(self):
		# Version number
		version = 1
		# Arbitrary 32 byte previous transaction hash
		prev_tx_hash = hash_SHA('0'.encode())
		# Arbritrary 32 byte previous recipient
		prev_recipient = hash_SHA('1'.encode())
		# Arbritrary 32 byte recipient
		recipient = hash_SHA('2'.encode())
		# Value of 100 for output
		value = 100
		# Input generated from above elements, with output_index of 0
		input1 = cat_input_fields(prev_tx_hash, 0, prev_recipient)
		# Output genereated from above elements
		output1 = create_output(value, recipient)
		# Input list
		inputs = [input1]
		# Output list
		outputs = [output1]

		# Manually generates expected output from above elements
		expected = int_to_bytes(version)
		expected += short_to_bytes(len(inputs))
		expected += input1
		expected += short_to_bytes(len(outputs))
		expected += output1

		# Actual output generated from cat_tx_fields
		actual = cat_tx_fields(version, inputs, outputs)
		self.assertEqual(expected, actual)

	def test_cat_tx_fields_double(self):
		# Version number
		version = 1
		# Arbitrary 32 byte previous transaction hash
		prev_tx_hash = hash_SHA('0'.encode())
		# Arbritrary 32 byte previous recipient
		prev_recipient = hash_SHA('1'.encode())
		# Arbritrary 32 byte recipient
		recipient = hash_SHA('2'.encode())
		# Value of 100 for output
		value1 = 100
		value2 = 300
		# Inputs generated from above elements, with output_index of 0, 1
		input1 = cat_input_fields(prev_tx_hash, 0, prev_recipient)
		input2 = cat_input_fields(prev_tx_hash, 1, prev_recipient)
		# Output genereated from above elements
		output1 = create_output(value1, recipient)
		output2 = create_output(value2, recipient)
		# Input list
		inputs = [input1, input2]
		# Output list
		outputs = [output1, output2]

		# Manually generates expected output from above elements
		expected = int_to_bytes(version)
		expected += short_to_bytes(len(inputs))
		expected += input1
		expected += input2
		expected += short_to_bytes(len(outputs))
		expected += output1
		expected += output2

		# Actual output generated from cat_tx_fields
		actual = cat_tx_fields(version, inputs, outputs)
		self.assertEqual(expected, actual)

	def test_create_tx_single(self):
		# Version number
		version = 1
		# Arbitrary 32 byte previous transaction hash
		prev_tx_hash = hash_SHA('0'.encode())
		# Arbritrary 32 byte previous recipient
		prev_recipient = hash_SHA('1'.encode())
		# Arbritrary 32 byte recipient
		recipient = hash_SHA('2'.encode())
		# Value of 100 for output
		value = 100
		# Input generated from above elements, with output_index of 0
		input1 = cat_input_fields(prev_tx_hash, 0, prev_recipient)
		# Output genereated from above elements
		output1 = create_output(value, recipient)
		# Input list
		unsigned_inputs = [input1]
		# Output list
		outputs = [output1]
		key_set1 = generate_key_set()
		
		private_key = key_set1["private_key"]
		public_key = key_set1["public_key"]
		unsigned_tx = cat_tx_fields(version, unsigned_inputs, outputs)
		signature = sign_transaction(unsigned_tx, private_key)
		signed_input = cat_input_fields(prev_tx_hash, 0, signature + public_key)
		signed_inputs = [signed_input]
		
		# creating a verification key
		verifying_key = ecdsa.VerifyingKey.from_string(public_key, ecdsa.SECP256k1)
		
		actual = create_tx(version, unsigned_inputs, outputs, private_key)

		#Checks if version number is correct
		self.assertEqual(actual[0:4], int_to_bytes(version))

		#Checks input info
		#Checks if number of inputs is correct
		self.assertEqual(actual[4:6], short_to_bytes(1))
		#Checks if previous transaction hash is correct of input1
		self.assertEqual(actual[6:38], prev_tx_hash)
		#Checks if output index of input1 is correct
		self.assertEqual(actual[38:40], short_to_bytes(0))
		#Checks if signature of input1 is valid
		self.assertTrue(verifying_key.verify(actual[40:104], hash_SHA(unsigned_tx)))
		
		#Checks ouptut info
		#Checks if the number of outputs is correct
		self.assertEqual(actual[6 + len(signed_input):6 + len(signed_input) + 2], short_to_bytes(1))
		#Checks if output1 is correct
		self.assertEqual(actual[6 + len(signed_input) + 2:6 + len(signed_input) + 2 + len(output1)], output1)
		
if __name__ == '__main__':
	unittest.main()
