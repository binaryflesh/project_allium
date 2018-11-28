import os, ecdsa, hashlib, json, binascii

from block import hash_SHA


def generate_private_key():
    """
    Creates a random 32 byte string used as a private key

    :no param:
    :return:    A randomly generated 32 byte string using urandom()
    """
    return os.urandom(32)

def generate_public_key(private_key):
    """
    Takes private key and puts it through the ellipical curve for public key encryption
    
    :param: private key is the randomly generated 32 byte string 
    :return:  verifying key, which effectively is the public key  
    """
    signing_key = ecdsa.SigningKey.from_string(private_key, curve = ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    return verifying_key.to_string()

def generate_pk_hash(public_key):
    """
    Takes public key
    
    :param: public key
    :return:  ripemd160 object  
    """
    sha_public_key = hashlib.sha256(public_key)
    ripemd160_obj = hashlib.new('ripemd160')
    ripemd160_obj.update(sha_public_key.digest())
    return ripemd160_obj.digest()

def generate_key_set():
    """
    Generates all 3 keys and stores them in a dictionary
    
    :no param:
    :return: dictionary containing all 3 keys  
    """
    key_set = {}
    key_set["private_key"] = generate_private_key()
    key_set["public_key"] = generate_public_key(key_set["private_key"])
    key_set["pk_hash"] = generate_pk_hash(key_set["public_key"])
    return key_set 

def key_set_to_json_format(key_set):
    """
    Given a key_set, it returns a equivalent set, one that can be stored in a json file


    :param: key_set: A dictionary with a private_key, pubic_key, pk_hash. All three values should just be bytes
    :return: key_set: same as the key_set passed in, except the byte values have been turning into strings
    """
    encoded_set = {}
    encoded_set["private_key"] = binascii.hexlify(key_set["private_key"]).decode()
    encoded_set["public_key"] = binascii.hexlify(key_set["public_key"]).decode()
    encoded_set["pk_hash"] = binascii.hexlify(key_set["pk_hash"]).decode()
    return encoded_set 

def json_format_to_key_set(key_set):
    """
    Given a key straight from a json file, converts it to a normal key_set
    
    :param: key_set: A dictionary with a private_key, pubic_key, pk_hash. All three values should just be byteshex decimal representation of bytes
    :return: key_set with all values converted into bytes
    """
    decoded_set = {}
    decoded_set["private_key"] = binascii.unhexlify(key_set["private_key"].encode())
    decoded_set["public_key"] = binascii.unhexlify(key_set["public_key"].encode())
    decoded_set["pk_hash"] = binascii.unhexlify(key_set["pk_hash"].encode())
    return decoded_set     

def store_keys():
    """
    This is a one-time use function. Generates keys and then stores it on a local file keys.json 

    :no param:
    :return: no return value, but a keys.json file is created/written to
    """
    key_set = generate_key_set() #get the keys
    #encode the key_set
    encoded_keys = key_set_to_json_format(key_set)
    with open('keys.json', 'w+') as output_file:
             json.dump(encoded_keys, output_file)
            
def load_keys():
    """
    Loads keys from a json file.

    :returns: a set of keys
    """
    with open("keys.json", "r") as read_file:
        keys = json.load(read_file)
    return keys
