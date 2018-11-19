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