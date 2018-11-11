import os, ecdsa, hashlib

from block import hashSHA, hash_SHA


def generate_private_key():
    """
    Creates a random 32 byte string used as a private key

    :no param:
    :return:    A randomly generated 32 byte string using urandom()
    """
    return os.urandom(32)

def generate_public_key(private_key):
    # Takes private key and puts it through the ellipical curve for public key encryption
    signing_key = ecdsa.SigningKey.from_string(private_key, curve = ecdsa.SECP256k1)
    # Return verifying key, which effectively is the public key
    verifying_key = signing_key.get_verifying_key()

    return verifying_key.to_string()





 
