from block import hash_SHA, long_to_bytes, short_to_bytes, bytes_to_short, bytes_to_long
import ecdsa
from collections import deque


def get_merkle_root(hashed_tx_list):
    """
    Calls the recursive helper function if the length
    of the hashed tx list is greater than 0.

    :param hashed_tx_list: a collections.deque object
    containing SHA-256 hashed byte strings
    :return: a single SHA-256 hashed byte string 
    """
    if len(hashed_tx_list) < 1:
        return None
    else:
        return _get_merkle_root(hashed_tx_list)

def _get_merkle_root(merkle_list):
    """
    Recursive helper function that pairs up
    adjacent elements and hashes them, then repeats
    until a single hash is left.

    :param merkle_list: a collections.deque object
    containing SHA-256 hashed byte strings
    :return: base case is a single hash otherwise
    a deque containing an even length deque
    of hashed byte strings
    """
    if len(merkle_list) == 1:
        return merkle_list.pop()
    else:
        if len(merkle_list) % 2 != 0:
            merkle_list.append(merkle_list[-1])
        sz = len(merkle_list)
        for i in range(int(sz/2)):
            p1 = merkle_list.popleft()
            p2 = merkle_list.popleft()
            merkle_list.append(hash_SHA(p1 + p2))
        return _get_merkle_root(merkle_list)

def create_output(value, recipient):
    """
    Convert the value to a long and concatenate it with the recipient

    :param value: value of transaction
    :param recipient: recipient of transaction
    :return: concatenation of the value converted to a long and the recipient 
    """
    return long_to_bytes(value) + recipient

def sign_transaction(private_key, prev_tx_hash, prev_tx_locking_script, new_tx_output):
    """
    Signs a transaction hash

    :param private_key: users private key
    :param prev_tx_hash: hash to the previous transaction
    :param prev_tx_locking_script: locking script to the previous transaction
    :param new_tx_hash: the hash of the current transaction
    :return: signature of the unsigned transaction hash
    """
    # concatenation of all keys except private key
    concat = prev_tx_hash + prev_tx_locking_script + new_tx_output
    # hashes the concatenated keys
    unsigned_tx_hash = hash_SHA(concat)
    # creates signing key
    signing_key = ecdsa.SigningKey.from_string(private_key,curve=ecdsa.SECP256k1)
    # signs the hashed transaction
    return signing_key.sign(unsigned_tx_hash)


def create_input(previous_tx_hash, index, signature, public_key):
    """
    Creates transation input

    :param previous_tx_hash: hash of the previous transaction
    :param index: Index of output
    :param signature: signature of the transaction hash
    :param public_key: users public key
    :return: concatenation of parameters with the index changed to a short
    """
    unlocking_script = signature + public_key
    index_short = short_to_bytes(index)
    return previous_tx_hash + index_short + unlocking_script

def parse_input(input):
    """
    Parses transaction input into dictionary

    :param input: Transaction input
    :return: dictionary containing transaction input parameters
    """
    # Create empty dictionary
    parsed_input = {}
    # Parse out sections of input into dictionary values
    parsed_input["previous_tx_hash"] = input[0:32]
    parsed_input["index"] = bytes_to_short(input[32:34])
    parsed_input["signature"] = input[34:98]
    parsed_input["public_key"] = input[98:162]
    # Return the dictionary
    return parsed_input

def parse_output(output):
    """
    Parses transaction output into dictionary

    :param output: Transaction output
    :return: dictionary containing transaction output parameters
    """
    # Create empty dictionary
    parsed_output = {}
    # Parse out sections of output into dictionary values
    parsed_output["value"] = bytes_to_long(output[0:8])
    parsed_output["recipient"] = output[8:40]
    # Return the dictionary
    return parsed_output

def cat_input_fields(prev_tx_hash, output_index, prev_recipient):
    """
    converts output_index to short in byte form and concatenates parameters in order

    :params prev_tx_hash, output_index, prev_recipient
    :return: concatentation of prev_tx_has, output_index (in byte form), prev_recipient
    """
    return prev_tx_hash + short_to_bytes(output_index) + prev_recipient