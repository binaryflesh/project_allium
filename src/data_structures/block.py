# imports
from hashlib import sha256 as sha
from binascii import hexlify, unhexlify
from time import time
from struct import pack, unpack
import math

def hash_SHA(byte_string):
    """
    Hashes the inputed byte string using SHA256 from the hash Library

    :param byte_string: The byte string that is going to be hashed
    :return: The hash of the inputed byte string
    """

    return sha(byte_string).digest()
    


def int_to_bytes(val):
    """
    Given an integer i, return it in byte form, as an unsigned int 
    Will only work for positive ints. 
    Max value accepted is 2^32 - 1 or 4,294,967,295
    Basically any valid positive 32 bit int will work 
    
    :param val: integer i 
    :return: integer i in byte form as unsigned int.
    """
    return pack('I', val)

def short_to_bytes(val):
    """
    Given an short i, return it in byte form, as an unsigned short 
    Will only work for positive shorts. 
    Max value accepted is 2^8 - 1 or 65535
    Basically any valid positive 8 bit int will work 
    
    :param val: short i 
    :return: short i in byte form as unsigned short.
    """
    return pack('H', val)

def long_to_bytes(val):
    """
    Given an long i, return it in byte form, as an unsigned long 
    Will only work for positive longs. 
    Max value accepted is 2^32 - 1 or 4,294,967,295
    Basically any valid positive 8 bit int will work 
    
    :param val: long i 
    :return: long i in byte form as unsigned long.
    """
    return pack('Q', val)

def time_now():
    """
    This function takes the current time and returns it as an integer

    :returns: an integer, representing the current system time.
    """
    return int(time())

def less_than_target(byte_string, target):
    """
    This function determines which of a byte string holding an integer, or a target integer is lesser.

    :param1 byte_string: a byte string intended to hold an integer
    :param2 targer: an integer, a target to which byte_string is compared  
    :returns: a boolean, true if the byte_string integer is less than target. false otherwise
    """
    return hash_to_int(byte_string) < target

def bytes_to_int(byte_string):
    """
    This function intends to convert a four byte string into an unsigned integer

    :param1 byte_string: a byte string, assumed to be four bytes, holding an integer
    :returns: an unsigned integer, drawn from byte_string
    """
    return unpack('I', byte_string)[0]

def bytes_to_short(byte_string):
    """
    This function intends to convert a four byte string into an unsigned short integer

    :param1 byte_string: a byte string, assumed to be four bytes, holding an integer
    :returns: an unsigned short integer, drawn from byte_string
    """
    return unpack('H', byte_string)[0]

def bytes_to_long(byte_string):
    """
    This function intends to convert a four byte string into an unsigned long integer

    :param1 byte_string: a byte string, assumed to be four bytes, holding an integer
    :returns: an unsigned long integer, drawn from byte_string
    """
    return unpack('Q', byte_string)[0]


def log_target_bytes(base10_number):
    """
    Converts the unsigned log base 10 of the inputed number into bytes

    :param base10_number: A number of base 10
    :return: The log base 10 of the inputed number as bytes
    """
    return short_to_bytes(int(math.log10(base10_number)))

def mine(previous_hash, data, target):
    """
    This function creates blocks using the proof of work algorithm, currently only generates
    block header.
    
    :param1 previous_hash: This is a 32 byte string representing the hash of a previous block
    :param2 data: This is a 32 byte string
    :param3 target: This is a unsigned integer representing the target number which the hash of the new block has to meet
    :returns: A 74 byte string containing the previous block hash, data, time of block creation, target power, and nonce
    in that order
    """
    nonce = 0
    timestamp = time_now()
    # Concatonates the previous hash, data, timestamp, exponent of target, and nonce into a byte string
    block_header = previous_hash + data + int_to_bytes(timestamp) + log_target_bytes(target) + long_to_bytes(nonce)
    block_hash = hash_SHA(block_header)

    while not (less_than_target(block_hash, target)):
        nonce += 1
        timestamp = time_now()
        block_header = previous_hash + data + int_to_bytes(timestamp) + log_target_bytes(target) + long_to_bytes(nonce)
        block_hash = hash_SHA(block_header)
        
    return block_header

def slice_nonce(block_header):
    """
    Takes a concatenated 74 byte string and returns the last 4 bytes

    :param1 block_header: a 74 byte string containing the information of a block
    :returns: a 4 byte byte string containing the nonce of a block
    """
    return block_header[70:78]

def slice_data(block_header):
    """
    Takes a concatenated 74 byte string and returns bytes 32 through 63

    :param1 block_header: a 74 byte string containing the information of a block
    :returns: a 32 byte string containing the block's data
    """ 
    return block_header[32:64]

def slice_prev_hash(block_header):
    """
    Takes a concatenated 74 byte string and returns bytes 0 through 31
    Those bytes represent the hash of the previous block

    :param1 block_header: a 74 byte string containing the information of a block
    :returns: a 32 byte string containing the hash of the previous block
    """ 
    return block_header[0:32]

def slice_timestamp(block_header):
    """
    Takes a concatenated 74 byte string and returns bytes 64 through 67
    Those bytes represent the timestamp of the block (time when the header was created)

    :param1 block_header: a 74 byte string containing the information of a block
    :returns: a 4 byte string containing the timestamp of the block
    """
    return block_header[64:68]

def slice_target(block_header):
    """
    Takes a concatenated 74 byte string and returns bytes 68 through 70
    Those bytes represent the target of the block

    :param1 block_header: a 74 byte string containing the information of a block
    :returns: a 2 byte string containing the target of the block
    """
    return block_header[68:70]

def hash_to_int(_hash):
    return int.from_bytes(_hash, byteorder='big')


def parse_block(block_header):
    """
    Takes a concatenated 74 byte string and runs it through the the previously defined slice functions
    Those functions outputs are added to a dictionary

    :param1 block_header: a 74 byte string containing the information of a block
    :returns: a dictionary containing the previous hash, data, timestamp, target and nonce of the block
    """
    parsed_block = {}
    parsed_block["prev_hash"] = slice_prev_hash(block_header)
    parsed_block["data"] = slice_data(block_header)
    parsed_block["timestamp"] = slice_timestamp(block_header)
    parsed_block["target"] = slice_target(block_header)
    parsed_block["nonce"] = slice_nonce(block_header)
    parsed_block["block_hash"] = hash_SHA(block_header)
    return parsed_block

def is_valid_block(block, prev_block):
    """
    Compares a block and its previous block to determine if block is allowed to be added to blockchain
    Confirms that the timestamp of block is larger than that of prev_block
    Confirms that prev_hash member of block is equal to hash of prev_block
    Confirms that the target of block is greater than the hash of block
    :param1 block: 74 byte string representing a block, output of mine()
    :param block: 74 byte string representing the previous block in the blockchain. output of mine()
    :returns: boolean True if all the above conditions are met, False otherwise
    """
    block_info = parse_block(block)
    prev_block_info = parse_block(prev_block)
    # Ensures that time timestamp of block is greater than the timestamp of prev_block
    if (bytes_to_int(block_info["timestamp"]) <= bytes_to_int(prev_block_info["timestamp"])):
        return False
    # Ensures that the prev_hash element of block matches the hash of prev_block
    if (block_info["prev_hash"] != hash_SHA(prev_block)):
        return False
    # Ensures that the block was mined correctly, and the block hash is less than the target
    if not (less_than_target(hash_SHA(block), 10**(bytes_to_short(block_info["target"])))):
        return False
    return True 
