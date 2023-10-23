import socket

class UDPManager:
    def __init__(self, port=0):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = self.get_ip()
        self.hostname = self.get_hostname()
        self.port = port
        self.udp.bind((self.ip, self.port))
        self.udp.settimeout(1)

    def print_info(self):
        print(f"IP Address: {self.ip}")  # Fix here
        print(f"Hostname: {self.hostname}")
        print(f"Port: {self.port}")

    def set_timeout(self, timeout):
        self.udp.settimeout(timeout)

    def get_hostname(self):
        try:
            return socket.gethostname()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_ip(self):
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            temp_sock.connect(("8.8.8.8", 80))
            ip = temp_sock.getsockname()[0]
            temp_sock.close()  # Close the temporary socket
            return ip
        except Exception as e:
            print(f"Error: {e}")
            temp_sock.close()  # Close the temporary socket even on failure
            return '0.0.0.0'  # default to listening on all available interfaces


    def send(self, message, address):
        self.udp.sendto(message, address)

    def receive(self):
        try:
            message, address = self.udp.recvfrom(1468)
            return message, address
        except socket.timeout:
            return None, None

    def close(self):
        self.udp.close()