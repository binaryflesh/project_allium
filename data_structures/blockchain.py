import os.path
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
            # fileobj = open(filename, "wb")
            # fileobj.close()
            with open(filename, 'wb') as f: pass
