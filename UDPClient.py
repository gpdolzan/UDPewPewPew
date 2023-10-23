from Logger import Logger
from UDPManager import UDPManager
import os
import sys
import vlc

class UDPClient:
    def __init__(self, server_ip, server_port, logger):
        self.server_address = (server_ip, server_port)
        self.udp_manager = UDPManager()
        self.logger = Logger("client")

        self.fifo_name = "video_fifo"  # Named pipe
        if not os.path.exists(self.fifo_name):
            os.mkfifo(self.fifo_name)  # Create the named pipe if it doesn't exist

        self.player = vlc.MediaPlayer(self.fifo_name)
        self.player.play()  # Start playing from the named pipe

        # Statistics
        self.prev_packet_number = 0
        self.missed_packets = 0
        self.out_of_order_packets = 0

    def register_with_server(self, server_ip, server_port):
        """Send registration request to the server."""
        # Log
        self.logger.info(f"Sending registration request to {server_ip}:{server_port}")
        self.udp_manager.send(b"REGISTER", (server_ip, server_port))

    def start_receiving(self):
        try:
            while True:
                data, addr = self.udp_manager.receive()  # Using UDPManager to receive data
                if not data:
                    break

                # Extract packet number (first 4 bytes) and video data (rest of the packet)
                packet_number = int.from_bytes(data[:4], byteorder='big')
                video_data = data[4:]

                # Check for missed or out-of-order packets
                if packet_number != self.prev_packet_number + 1:
                    if packet_number <= self.prev_packet_number:
                        self.out_of_order_packets += 1
                        self.logger.warning(f"Received out-of-order packet. Expected: {self.prev_packet_number + 1}, Got: {packet_number}")
                    else:
                        missed = packet_number - self.prev_packet_number - 1
                        self.missed_packets += missed
                        self.logger.warning(f"Missed {missed} packets. Jumped from {self.prev_packet_number} to {packet_number}")

                self.prev_packet_number = packet_number

                with open(self.fifo_name, "wb") as fifo:
                    fifo.write(video_data)

        except Exception as e:
            self.logger.warning(f"Error: {e}. Ending client.")
            self.print_statistics()

        finally:
            self.cleanup()

    def print_statistics(self):
        self.logger.info(f"Missed Packets: {self.missed_packets}")
        self.logger.info(f"Out-of-Order Packets: {self.out_of_order_packets}")

    def cleanup(self):
        self.player.stop()
        os.remove(self.fifo_name)  # Remove the named pipe
        self.udp_manager.close()  # Close the UDP socket using UDPManager

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: client.py <SERVER_IP> <SERVER_PORT>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    logger = Logger("client")

    client = UDPClient(server_ip, server_port, logger)
    client.register_with_server(server_ip, server_port)
    client.start_receiving()
