import os.path
from struct import pack
class Blockchain:
    
    def __init__(self,filename):
        """
        Constructor that takes in a blockchain to create a copy of it
        in the class data member blockfile

        :param filename: local copy of the blockchain that will
                        be used to create this copy of the blockchain
        :no return:
        """
        self.blockfile = filename
        # If the file does not already exist, create the file and close it
        if not (os.path.isfile(filename)):
            with open(filename, 'wb') as f: pass

def get_size_bytes(byte_string):
    """
    Determines the integer size of a byte string and returns it in byte form

    :param1 byte_string: A string of bytes
    :returns: An integer in byte form
    """
    return pack('I', len(byte_string))

def extract(filename, index, num_bytes, offset=0):
  """
  Opens file at filename, moves file pointer to correct position by using
  adding index and offset, reads num_bytes bytes and returns them.
  :param1 filename: String, path to a file containing bytes
  :param2 index: Integer, representing where bytes should begin to read from
  :param3 num_bytes: Integer, number of bytes to read in
  :param4 offset: Integer, default 0. Number to adjust index by if file is offset  
  :returns: Bytestring, representing bytes from index+offspring to index+offspring+num_bytes in filename
  """
  # Opens file for reading bytes
  with open(filename, 'rb') as file:
      # Moves file pointer to correct position at index + offset
      file.seek(index + offset, 0)
      # Reads num_bytes after file pointer
      return file.read(num_bytes)