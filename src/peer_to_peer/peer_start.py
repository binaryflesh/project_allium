import logging
import socket
import time
import sys
import json
import requests
import threading
import getopt
FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger()
lock = threading.Lock()


def check_connectivity():
    """
    Checks to see if the machine has an internet connection.
    Also returns machine's hostname ip address

    :return: string ip address
    """
    while True:
        try:
            sock = socket.create_connection(
                ('www.google.com', 80)
            )
            HOST = sock.getsockname()[0]
            sock.close()
            return HOST
        except OSError:
            logger.error("No internet connection.")
            time.sleep(3)
            continue


def connect_to_peers(peers, connections):
    """
    Given a list of peers, attempts to connect to each one.

    :param peers: a list of dictionaries with keys 'ip' and 'port'
    :param connections: a list of sockets
    """
    for p in peers:
        if not p['ip'] == HOST:
            try:
                logger.debug("Attempting connection to {}:{}...".format(
                    p['ip'], p['port']))
                sock = socket.create_connection(
                    (p['ip'], p['port'])
                )
                with lock:
                    connections.append(sock)
                logger.debug("Successfuly connected to {}:{}.".format(
                    p['ip'], p['port']))
            except ConnectionRefusedError:
                logger.debug("Failed to connect to {}:{}.".format(
                    p['ip'], p['port']))


def accept_connections(server, connections, MAX_CONNS):
    """
    Accepts incoming connections.
    Will continue to accept connections until reaching a maximum count.

    :param server: socket object that is bound to a host and port
    :param connections: list of sockets this node is connected to
    :param MAX_CONNS: maximum number of connections
    """
    while len(connections) < MAX_CONNS:
        conn, addr = server.accept()
        with lock:
            connections.append(conn)
        logger.debug("{} has connected.".format(addr))


if __name__ == '__main__':
    """
    Stage 1: Check for internet connection
    """
    logger.debug("Checking internet connection... ")
    online = False  # <--- online variable can be used for GUI
    try:
        HOST = check_connectivity()  # <--- gets the machine's hostname address

    except KeyboardInterrupt:  # <--- Ctrl + C will end the while loop
        logger.debug("Terminating main thread due to keyboard interrupt.")
        sys.exit()

    online = True  # <--- if it reaches this point, you have internets

    """
    Stage 2: Connect to peers
    """

    """
    - set system variables
    """

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:p:c:", [
                                   "help", "tracker=", "port=", "max_conns="])
    except getopt.GetoptError as err:
        logger.critical(err)
        sys.exit(1)
    port = 9001
    MAX_CONNS = 1
    for o, a in opts:
        if o in ("-h", "--help"):
            sys.exit(
                "Provide a tracker file and optional port with max connections")
        elif o in ("-p", "--port"):
            port = int(a)
        elif o in ("-t", "--tracker"):
            tracker_file = (a)
        elif o in ("-c", "--max_conns"):
            MAX_CONNS = int(a)

    """
    - read links from tracker file
    """
    try:
        with open(tracker_file, 'r') as fp:
            links = json.load(fp)
    except FileNotFoundError as err:
        logger.critical(err)
        sys.exit(1)
    except NameError:
        logger.critical("Must provide tracker file.")
        sys.exit(1)

    peers = requests.get(url=links['get']).json()

    connections = []

    conn_thread = threading.Thread(
        target=connect_to_peers,
        args=(peers, connections),
        name="Outgoing Connections",
        daemon=True
    )

    conn_thread.start()
    conn_thread.join()

    logger.debug("Number of active peers found: {}.".format(len(connections)))

    with lock:
        if len(connections) >= MAX_CONNS:
            sys.exit()

    """
    Stage 3: Accept connections
    """

    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', port))
    server.listen()

    ac_thread = threading.Thread(
        target=accept_connections,
        args=(server, connections, MAX_CONNS),
        name="Accept Connections",
        daemon=True
    )

    try:
        logging.debug(
            "Listening for connections on {}:{}...".format(HOST, port))
        ac_thread.start()

        requests.get(url=links['add'], params={
            'ip': HOST,
            'port': port
        })

        while True:
            with lock:
                if len(connections) > 0:
                    break
            time.sleep(5)
            peers = requests.get(url=links['get']).json()
            conn_thread = threading.Thread(
                target=connect_to_peers,
                args=(peers, connections),
                name="Outgoing Connections",
                daemon=True
            )
            conn_thread.start()
            conn_thread.join()

        ac_thread.join()
    except KeyboardInterrupt:
        logger.debug("Terminating main thread due to keyboard interrupt.")
        server.close()
        sys.exit()
    finally:
        server.close()
