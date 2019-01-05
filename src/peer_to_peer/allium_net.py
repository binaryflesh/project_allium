import socket
import json
import os
from pprint import pprint

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

def make_server(port):
    """
    Return a new socket using the given address family, socket type and protocol number.
    The address family should be AF_INET (the default), AF_INET6 or AF_UNIX.
    The socket type should be SOCK_STREAM (the default), SOCK_DGRAM or perhaps
    one of the other SOCK_ constants. The protocol number is usually zero and may be
    omitted in that case.

    :param port: The int will represent the desired port number (default is 9001)
    :returns: A socket that represents the server
    """
    server = socket.socket()
    server.bind(('', port))
    return server

def get_peer_tracker(tracker_links) :
    """
    Returns available peers who want to connect to the Allium network

    :param tracker_links: Provides the link list of available peers
    :returns: contents of json.reload
    """

    with open(tracker_links) as data_file:
        data = json.load(data_file)

    return data
