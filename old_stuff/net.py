import socket

# CONSTANTS
UDP_PACKET_BYTES = 1472
TIMEOUT = 5

def get_local_ip():
    """
    Get the local IP address of the machine.
    """
    # The following code will get the local IP address of the machine
    # that has a connection to the outside world (like the internet).
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # The IP address isn't really used here. It's just a known IP that will cause the OS 
        # to select the appropriate network interface to route the traffic.
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_hostname():
    """
    Get the hostname of the machine.
    """
    try:
        return socket.gethostname()
    except Exception as e:
        print(f"Error: {e}")
        return None

def bind_socket(ip, port):
    """
    Bind a socket UDP socket to the specified IP address and port.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((ip, port))
        return s
    except Exception as e:
        print(f"Error: {e}")
        return None

def listen_for_message(socket, timeout=TIMEOUT, size=UDP_PACKET_BYTES):
    """
    Listen for a message on the specified socket.
    """
    try:
        socket.settimeout(timeout)
        message, address = socket.recvfrom(size)
        return message, address
    except Exception as e:
        print(f"Error: {e}")
        return None, None