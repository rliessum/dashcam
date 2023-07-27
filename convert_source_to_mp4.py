import os
import subprocess
import shutil
import datetime

def check_command(command):
    try:
        subprocess.run(["which", command], check=True)
    except subprocess.CalledProcessError:
        raise Exception(f"{command} is required but it's not installed.")

# Check if ffmpeg and ffprobe are installed.
check_command("ffmpeg")
check_command("ffprobe")

# Video file options and locations.
input_dir = "./input"
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)
video_extension = "avi"

# Check if input directory exists.
if not os.path.isdir(input_dir):
    raise Exception("Input directory does not exist.")

# Loop through all the AVI files in the input directory.
for file_name in os.listdir(input_dir):
    if file_name.endswith(video_extension):
        file_path = os.path.join(input_dir, file_name)
        base_name = os.path.basename(file_path)
        video_name, _ = os.path.splitext(base_name)

        # Check if the file is non-interleaved.
        ffprobe_output = subprocess.run(["ffprobe", "-i", file_path], text=True, capture_output=True, check=True).stderr
        if "non-interleaved AVI" in ffprobe_output:
            print(f"The video {base_name} is non-interleaved. Converting to MP4...")
            # Temporarily convert the video to MP4.
            temp_file = os.path.join(output_dir, f"{video_name}_temp.mp4")
            subprocess.run(["ffmpeg", "-i", file_path, "-pix_fmt", "yuv420p", temp_file], check=True)
            # Use the MP4 video as the input for the next steps.
            file_path = temp_file
        else:
            print(f"The video {base_name} is interleaved.")

        # Convert the pixel format and strip the audio.
        output_file = os.path.join(output_dir, f"{video_name}_no_audio.mp4")
        subprocess.run(["ffmpeg", "-i", file_path, "-pix_fmt", "yuv420p", "-an", output_file], check=True)

        # If a temporary MP4 video was created, delete it.
        if os.path.exists(temp_file):
            os.remove(temp_file)
