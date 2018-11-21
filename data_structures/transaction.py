from block import hash_SHA, long_to_bytes
import ecdsa
from collections import deque


def get_merkle_root(hashed_tx_list):
    """
    Calls the recursive helper function if the length
    of the hashed tx list is greater than 0.

    :param hashed_tx_list: a collections.deque object
    containining SHA-256 hashed byte strings
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
    Convert the value to a long and concatenate it with the recepiant

    :param value: value of transaction
    :param recipient: recipient of transaction
    :return: concatenation of the value converted to a long and the recipient 
    """
    return long_to_bytes(value) + recipient
