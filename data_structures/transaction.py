from block import hash_SHA
import ecdsa
from collections import deque


def get_merkle_root(hashed_tx_list):
    if len(hashed_tx_list) < 1:
        return None
    else:
        return _get_merkle_root(hashed_tx_list)

def _get_merkle_root(merkle_list):
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
