import os
import subprocess

class VideoManager:
    def __init__(self, video_folder='./videos'):
        self.video_folder = video_folder
        self.converted_folder = './converted'  # Move converted folder to the root directory
        self.ensure_converted_folder_exists()
        self.video_files = [f for f in os.listdir(self.video_folder) if os.path.isfile(os.path.join(self.video_folder, f))]

    def get_video_duration(self, video_path):
        """Retrieve the duration of the video in seconds using ffmpeg."""
        cmd = ["ffmpeg", "-i", video_path, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
        try:
            output = subprocess.check_output(cmd)
            return float(output)
        except Exception as e:
            self.logger.error(f"Error getting duration for video {video_path}. Error: {str(e)}")
            exit(1)

    def get_converted_video_files(self):
        """Return a list of paths to all converted videos in the converted folder."""
        video_files = [os.path.join(self.converted_folder, f) for f in os.listdir(self.converted_folder) if f.endswith('.ts')]
        return video_files  

    def ensure_converted_folder_exists(self):
        """Ensure the converted videos folder exists."""
        if not os.path.exists(self.converted_folder):
            os.makedirs(self.converted_folder)

    def get_video_duration(self, video_path):
        """Get the duration of a video."""
        cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(result.stdout)

    def convert_all_videos_to_ts(self):
        """Converts all videos in the video_folder to .ts format."""
        for video_file in self.video_files:
            # Base name without extension
            base_name = os.path.splitext(video_file)[0]

            # If the video is already in .ts format, simply move it to the converted folder.
            if video_file.endswith('.ts'):
                shutil.move(os.path.join(self.video_folder, video_file),
                            os.path.join(self.converted_folder, video_file))
                continue
        
            # Check if a .ts version of the video already exists in the converted folder.
            if os.path.exists(os.path.join(self.converted_folder, base_name + '.ts')):
                continue  # Skip conversion if .ts version already exists

            # Conversion process for non .ts videos
            input_path = os.path.join(self.video_folder, video_file)
            output_path = os.path.join(self.converted_folder, base_name + '.ts')
            cmd = ["ffmpeg", "-i", input_path, "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", output_path]
            subprocess.run(cmd)


    def convert_video_to_ts(self, video_name):
        """Convert a single video to .ts format using ffmpeg."""
        input_path = os.path.join(self.video_folder, video_name)
        output_path = os.path.join(self.converted_folder, video_name + '.ts')
        
        if not os.path.exists(output_path):
            cmd = [
                'ffmpeg', 
                '-i', input_path, 
                '-c', 'copy', 
                '-bsf:v', 'h264_mp4toannexb', 
                '-f', 'mpegts', 
                output_path
            ]
            subprocess.run(cmd)

    def get_next_video(self):
        """Get the path of the next video in the converted folder to be streamed."""
        for filename in os.listdir(self.converted_folder):
            if filename.endswith('.ts'):
                return os.path.join(self.converted_folder, filename)
        return None