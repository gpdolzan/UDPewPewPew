import net
import threading

# CONSTANTS
MAIN_PORT = 8521
LOCAL_IP = None
HOSTNAME = None
MAIN_SOCKET = None
REGISTERED_USERS = []

def get_starting_info():
    """
    Get the local IP address, hostname, and socket.
    """
    global LOCAL_IP, HOSTNAME, MAIN_SOCKET
    LOCAL_IP = net.get_local_ip()
    HOSTNAME = net.get_hostname()
    MAIN_SOCKET = net.bind_socket(LOCAL_IP, MAIN_PORT)
    if MAIN_SOCKET is None:
        print("Error: Could not bind socket.")
        return False
    return True

def main_server_loop():
    """
    Main server loop.
    Basically listens for possible users to register.
    If the user wants to register, then add them to the list of registered users.
    After that create 2 threads:
        1. Thread to listen for messages from the user
        2. Thread to send messages to the user
    """
    global MAIN_SOCKET
    while True:
        message, address = net.listen_for_message(MAIN_SOCKET)
        if message is None and address is None:
            continue
        elif message == b"register":
            if address not in REGISTERED_USERS:
                REGISTERED_USERS.append(address)
                # Create 2 threads
                # 1. Thread to listen for messages from the user
                # 2. Thread to send messages to the user
                listen_thread = threading.Thread(target=listen_for_user_messages, args=(address,))
                listen_thread.start()
                send_thread = threading.Thread(target=send_messages_to_user, args=(address,))
                send_thread.start()
    return True

def listen_for_user_messages(address):
    """
    Bind a new socket to the specified address of the user.
    Then choose port after the main port, verify that it is open, and bind it.
    """
    
    while True:
        message, address = net.listen_for_message(MAIN_SOCKET)
        
    return True

# main
if __name__ == "__main__":
    if not get_starting_info():
        exit(1)
    main_server_loop()

    