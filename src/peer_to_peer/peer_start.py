import socket, time, sys

def check_connectivity():
    """
    Checks to see if the machine has an internet connection.
    Also returns machine's hostname ip address

    :return: string ip address
    """
    print("Checking internet connection... ", end="", flush=True)
    while True:
        try:
            sock = socket.create_connection(
                ('www.google.com', 80)
            )
            HOST = sock.getsockname()[0]
            sock.close()
            print("confirmed.")
            return HOST
        except OSError:
            print("failed")
            print("Error: no internet connection.")
            time.sleep(3)
            continue

if __name__ == '__main__':

    """
    Stage 1: Check for internet connection
    """
    online = False # <--- online variable can be used for GUI
    try:
        HOST = check_connectivity() # <--- gets the machine's hostname address

    except KeyboardInterrupt: # <--- Ctrl + C will end the while loop
        print("\nTerminating main thread.")
        sys.exit()

    online = True # <--- if it reaches this point, you have internets
