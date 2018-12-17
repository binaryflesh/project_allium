# imports
import unittest
import sys
sys.path.append(sys.path[0] + "/../src/data_structures")
from block import *
import time
from struct import unpack

class TestBlock(unittest.TestCase):

    def test_Hash_SHA(self):
        data = "SIG Blockchain"
        actual = hash_SHA(data.encode())
        self.assertIsInstance(actual, bytes)

    def test_int_to_bytes(self):
        """
        Tests out values for the int_to_bytes function. Tests out max values as well
        """
        byte1 = int_to_bytes(1)
        #if we unpack the bytes as a unsigned integer, we should get the same value
        self.assertEqual(unpack('I', byte1)[0], 1)
        #test out 0
        byte0 = int_to_bytes(0)
        self.assertEqual(unpack('I', byte0)[0], 0)
        #test out max signed 32 bit int
        byte_max_32 = int_to_bytes(2**31 -1)
        self.assertEqual(unpack('I', byte_max_32)[0], 2**31 -1)
        #test out max unsigned 32 bit int
        byte_max_u32 = int_to_bytes(2**32 -1)
        self.assertEqual(unpack('I', byte_max_u32)[0], 2**32 -1)

    def test_short_to_bytes(self):
        """
        Tests out values for the short_to_bytes function. Tests out max values as well
        """
        byte1 = short_to_bytes(1)
        #if we unpack the bytes as a unsigned integer, we should get the same value
        self.assertEqual(unpack('H', byte1)[0], 1)
        #test out 0
        byte0 = short_to_bytes(0)
        self.assertEqual(unpack('H', byte0)[0], 0)
        #test out max unsigned 32 bit int
        byte_max_short = short_to_bytes(2**8 -1)
        self.assertEqual(unpack('H', byte_max_short)[0], 2**8 -1)

    def test_long_to_bytes(self):
        """
        Tests out values for the long_to_bytes function. Tests out max values as well
        """
        byte1 = long_to_bytes(1)
        #if we unpack the bytes as a unsigned integer, we should get the same value
        self.assertEqual(unpack('L', byte1)[0], 1)
        #test out 0
        byte0 = long_to_bytes(0)
        self.assertEqual(unpack('L', byte0)[0], 0)
        #test out max unsigned 32 bit int
        byte_max_long = long_to_bytes(2**32 -1)
        self.assertEqual(unpack('L', byte_max_long)[0], 2**32 -1)

    # Tests time_now() by printing the current time, converting it
    # to an int manually, and comparing it to the output of time_now
    def test_time_now(self):
        curr_time = time.time()
        int_time = int(curr_time)
        self.assertEqual(int_time, time_now())

    # Converts a known value to a bytestring and manually converts to string
    # Compares to output of less_than_target with known greater value
    def test_less_than_target(self):
        target = 30
        test_bs = bytes([20])
        self.assertTrue(less_than_target(test_bs, target))

    # Converts a known value to a byte string, manually converts it back into an
    # integer, compares this integer to the output of bytes_to_int()
    def test_bytes_to_int(self):
        convert = 20
        byte_s = pack('I', convert)
        self.assertEqual(convert, bytes_to_int(byte_s))

    # Converts a known value to a byte string, manually converts it back into an
    # integer, compares this integer to the output of bytes_to_int()
    def test_bytes_to_short(self):
        convert = 30
        byte_s = pack('H', convert)
        self.assertEqual(convert, bytes_to_short(byte_s))

    # Converts a known value to a byte string, manually converts it back into an
    # integer, compares this integer to the output of bytes_to_int()
    def test_bytes_to_long(self):
        convert = 40
        byte_s = pack('L', convert)
        self.assertEqual(convert, bytes_to_long(byte_s))

    # Gets the log of a given whole number of base 10 and converts it into bytes
    # Uses short_to_bytes function for byte conversion
    def test_log_target_bytes(self):
        convert = 10000             #10^4
        byte_form = log_target_bytes(convert)
        self.assertEqual(convert, pow(10,int.from_bytes(byte_form,byteorder = 'little')))

    # Generates a block with predetermined values, checks the length of the output, expecting 74
    def test_mine(self):
        # Creates 2 arbitrary 32 byte strings
        prev_hash = hash_SHA("0".encode())
        self.assertEqual(32, len(prev_hash))
        data = hash_SHA("0".encode())
        self.assertEqual(32, len(data))
        #Creates a block header by mining with these strings and a target of 10^200
        bytestring = mine(prev_hash, data, 10**77)
        self.assertEqual(74, len(bytestring))   #NOTE: This fails on Linux Mint
        #Tests if result block header is less than target
        self.assertTrue(less_than_target(hash_SHA(bytestring), 10**77))

    # Generates a block based on an incredibly large target, so the nonce will be zero
    # Compares the result of splice_nonce converted to an integer to zero
    def test_slice_nonce(self):
        # Creates an arbitrary 32 byte string and creates a block with it
        prev_hash = hash_SHA("0".encode())
        data = hash_SHA("BeepBeepLettuce".encode())
        header = mine(prev_hash, data, 10**200)
        # The nonce of mine() should be always zero, due to large target, output of slice_nonce() is zero
        self.assertEqual(0, bytes_to_long(slice_nonce(header)))

    # Generates a block based on a specific data and tests the results of
    # splice_data to the defined data
    def test_slice_data(self):
        # Creates an arbitrary 32 byte string and creates a block with it
        prev_hash = hash_SHA("0123456789ABCDEF".encode())
        data = hash_SHA("BeepBeepLettuce".encode())
        header = mine(prev_hash, data, 10**100)
        sliced_data = slice_data(header)
        # Tests the length of the data byte string, expecting 32
        self.assertEqual(32, len(sliced_data))
        # Tests the result of splice_data with the inputted data
        self.assertEqual(data, sliced_data)

    def test_slice_prev_hash(self):
        # Creates an arbitrary 32 byte string and creates a block with it
        prev_hash = hash_SHA("0123456789ABCDEF".encode())
        data = hash_SHA("BeepBeepLettuce".encode())
        header = mine(prev_hash, data, 10**200)
        sliced_prev_hash = slice_prev_hash(header)
        # Tests the length of the data byte string, expecting 32
        self.assertEqual(32, len(sliced_prev_hash))
        # Tests the result of splice_data with the inputted data
        self.assertEqual(prev_hash, sliced_prev_hash)

    def test_slice_timestamp(self):
        # Creates an arbitrary 32 byte string and creates a block with it
        prev_hash = hash_SHA("0123456789ABCDEF".encode())
        data = hash_SHA("BeepBeepLettuce".encode())
        header = mine(prev_hash, data, 10**200)
        sliced_timestamp = slice_timestamp(header)
        # Tests the length of the data byte string, expecting 32
        self.assertEqual(4, len(sliced_timestamp))

    def test_slice_target(self):
        # Creates an arbitrary 32 byte string and creates a block with it
        prev_hash = hash_SHA("0123456789ABCDEF".encode())
        data = hash_SHA("BeepBeepLettuce".encode())
        target = 10**200
        header = mine(prev_hash, data, target)
        sliced_target = slice_target(header)
        # Tests the length of the data byte string, expecting 32
        self.assertEqual(2, len(sliced_target))
        self.assertEqual(log_target_bytes(target), sliced_target)

    def test_parse_block(self):
       # Creates an arbitrary 32 byte string and creates a block with it
       prev_hash = hash_SHA("0123456789ABCDEF".encode())
       data = hash_SHA("0123456789ABCDEF".encode())
       target = 10**200
       header = mine(prev_hash, data, target)
       parsed_block = parse_block(header)
       # Tests if the values that are in the dictionary are the same as the inputted values
       self.assertEqual(prev_hash, parsed_block["prev_hash"])
       self.assertEqual(data, parsed_block["data"])
       self.assertEqual(log_target_bytes(target), parsed_block["target"])
       # Tests if the values in the dictionary are equal to the ones found by the related slice functions
       self.assertEqual(slice_nonce(header), parsed_block["nonce"])
       self.assertEqual(slice_timestamp(header), parsed_block["timestamp"])
       self.assertEqual(hash_SHA(header), parsed_block["block_hash"])
      
    @unittest.skip(" ")
    # This test ensures that a block with a timestamp less than the timestamp of its previous block, will not be added to the blockchain
    def test_01_is_valid_block(self):
        target = 10**72     # Target for which all block hashes must be under
        data = hash_SHA("1".encode())   # valid block data to be used for block construction
        prev_hash = hash_SHA("0".encode())  # This previous hash is invalid, though the timestamp of the block will be checked first
        #Creates an invalid block, this is invalid due to having a timestamp less than the candidate block
        invalid_candidate_block = mine(prev_hash, hash_SHA("INVALID".encode()), target)

        #Creates a valid previous block
        prev_block = mine(hash_SHA("0".encode()), data, target)

        # Confirms that block with timestamp lesser than prev_block is invalid
        self.assertFalse(is_valid_block(invalid_candidate_block, prev_block))

    @unittest.skip(" ")
    # This test ensures that a block with an invalid previous hash will not be added to the blockchain
    def test_02_is_valid_block(self):
        target = 10**72     # Target for which all block hashes must be under
        data = hash_SHA("1".encode())   # valid block data to be used for block construction

        #This previous hash would be invalid if used to create a new block, as it does not match hash_SHA(prev_block)
        invalid_prev_hash = hash_SHA("BEEPBEEPLETTUCE".encode())

        #Creates a valid previous block
        prev_block = mine(hash_SHA("0".encode()), data, target)

        time.sleep(1) # Ensures prev_block and candidate block will not have identical timestamps
        #Creates an invalid block with invalid prev_hash that does not match hash_SHA(prev_block)
        invalid_candidate_block = mine(invalid_prev_hash, hash_SHA("INVALID".encode()), target)

        # Confirms that block with prev_hash not equal to hash of prev_block is invalid
        self.assertFalse(is_valid_block(invalid_candidate_block, prev_block))

    @unittest.skip(" ")
    # This test ensures that a block with an invalid block hash, a block hash that is greater than its target, is not added to the blockchain
    def test_03_is_valid_block(self):
        previous_target = 10**75     # Target for which all block hashes must be under
        candidate_target = 1        # A low target like this will create a block with an invalid hash
        data = hash_SHA("1".encode())   # valid block data to be used for block construction

        #Creates a valid previous block
        prev_block = mine(hash_SHA("0".encode()), data, previous_target)
        prev_hash = hash_SHA(prev_block)

        time.sleep(1) # Ensures prev_block and candidate block will not have identical timestamps
        #Creates an invalid block with block hash less than its target
        #NOTE: This cannot be done with mine() function, as it checks for this
        nonce = 0
        timestamp = time_now()
        # Concatonates the previous hash, data, timestamp, exponent of target, and nonce into a byte string
        invalid_candidate_block = prev_hash + data + int_to_bytes(timestamp) + log_target_bytes(candidate_target) + long_to_bytes(nonce)

        # Confirms that block where block hash is lesser than target is invalid block
        self.assertFalse(is_valid_block(invalid_candidate_block, prev_block))

    @unittest.skip(" ")
    # This tests shows that a valid block, a block that meets none of the above three failure states, will be added to the blockchain
    def test_04_is_valid_block(self):
        target = 10**72     # Target for which all block hashes must be under
        data = hash_SHA("1".encode())   # valid block data to be used for block construction
        #Creates a valid previous block
        prev_block = mine(hash_SHA("0".encode()), data, target)
        prev_hash = hash_SHA(prev_block)

        time.sleep(1)   # Ensures prev_block and candidate block will not have identical timestamps
        #Creates a valid block
        candidate_block = mine(prev_hash, data, target)

        #Tests if block is a valid block, it should be
        self.assertTrue(is_valid_block(candidate_block, prev_block))

if __name__ == '__main__':
    unittest.main()
