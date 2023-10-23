import os
import time
import subprocess
import sys
from UDPManager import UDPManager
from Logger import Logger
from VideoManager import VideoManager

class UDPServer:
    def __init__(self, port, default_interval=None):
        self.udp_manager = UDPManager(port=port)
        self.logger = Logger("server")
        self.video_manager = VideoManager()
        self.video_manager.convert_all_videos_to_ts()
        self.packet_size = 1468  # 1472 (1500 - 20 for IP header - 8 for UDP header) - 4 for packet number
        self.registered_clients = set()

        # Check if interval is set from command line
        self.interval_set_from_cli = default_interval is not None
        self.packet_interval = default_interval if self.interval_set_from_cli else 0.02  # default value

    def register_client(self, client_address):
        """Register a new client."""
        self.registered_clients.add(client_address)

    def start(self):
        self.logger.info("UDPServer started on adress: " + self.udp_manager.get_ip() + ":" + str(self.udp_manager.port))

        self.logger.info("Listening for registration, will start streaming in 30 seconds")
        self.udp_manager.set_timeout(1)
        start_time = time.time()
        while time.time() - start_time < 30:  # listening for registration for 30 seconds
            data, client_address = self.udp_manager.receive()
            if data and data.decode("utf-8") == "REGISTER":
                # log registration
                self.logger.info(f"Received registration from {client_address}")
                self.register_client(client_address)
        self.udp_manager.set_timeout(1)

        while True:
            video_files = self.video_manager.get_converted_video_files()
            for video_path in video_files:
                # Calculate optimal interval if not set from CLI
                if not self.interval_set_from_cli:
                    self.packet_interval = self.calculate_optimal_interval(video_path)

                self.stream_video(video_path)
                time.sleep(2)  # Sleep between sending different video files

    def add_client(self, client_address):
        """Add a client to the set of clients."""
        self.clients.add(client_address)
        self.logger.info(f"Added client: {client_address}")

    def remove_client(self, client_address):
        """Remove a client from the set of clients."""
        if client_address in self.clients:
            self.clients.remove(client_address)
            self.logger.info(f"Removed client: {client_address}")

    def stream_video(self, video_path):
        # create video_name removing path and extension
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        # create video duration
        video_duration = self.video_manager.get_video_duration(video_path)
        video_duration_floor = int(video_duration) + 1
        # Log that we are streaming video_name
        self.logger.info(f"Streaming {video_name} [{video_duration_floor // 60}:{video_duration_floor % 60} minutes]")
        with open(video_path, 'rb') as video_file:
            packet_num = 0
            while chunk := video_file.read(self.packet_size):
                data = packet_num.to_bytes(4, byteorder='big') + chunk
                for client in self.registered_clients:
                    self.udp_manager.send(data, client)
                time.sleep(self.packet_interval)
                packet_num += 1

    def calculate_optimal_interval(self, video_path):
        # Getting the video duration in seconds using FFmpeg
        command = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        try:
            duration = float(result.stdout.strip())
        except ValueError:
            print(f"Error converting ffmpeg output to float: {result.stdout}")
            duration = 0  # Or set a default duration or handle the error as needed.

        
        # Calculate total number of packets
        video_size = os.path.getsize(video_path)
        total_packets = video_size // self.packet_size

        # Optimal interval calculation
        optimal_interval = duration / total_packets
        return optimal_interval


if __name__ == "__main__":
    interval = None
    if len(sys.argv) > 1:
        interval = float(sys.argv[1])

    server = UDPServer(port=8521, default_interval=interval)
    server.start()