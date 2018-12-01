import socket

def get_ip():
    """
    Gets the ip address of the program's machine

    :returns: ip address in string form
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.google.com', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def make_server(port=9001):
    """Return a new socket using the given address family, socket type and protocol number. 
       The address family should be AF_INET (the default), AF_INET6 or AF_UNIX. 
       The socket type should be SOCK_STREAM (the default), SOCK_DGRAM or perhaps 
       one of the other SOCK_ constants. The protocol number is usually zero and may be 
       omitted in that case.
       The port number will be assigned to 9001 if not specified."""
    server = socket.socket()
    server.bind(('', port))

    return server
