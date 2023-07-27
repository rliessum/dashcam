import os
import subprocess
import shutil
import datetime

# Video file options and locations.
input_dir = "./input"

# Output file options and locations. create with timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
output_dir = os.path.join(os.getcwd(), f"output_{timestamp}")
os.makedirs(output_dir, exist_ok=True)
output_file_name = "timelapse.mp4"
video_extension = "mp4"

# How much to speed up the clips.
speedup = "0.05"

# How much to trim off each sped-up clip.
trim_amount = "00.12"

# Check if input directory exists.
if not os.path.isdir(input_dir):
    raise Exception("Input directory does not exist.")

# Create directories for processed and cropped files.
cropped_dir = os.path.join(output_dir, "cropped")
os.makedirs(cropped_dir, exist_ok=True)

# Loop through all the files, creating sped-up versions of each and then trimming.
for file_name in os.listdir(input_dir):
    if file_name.endswith(video_extension):
        file_path = os.path.join(input_dir, file_name)
        base_name = os.path.basename(file_path)
        video_name, _ = os.path.splitext(base_name)
        speedy_video = os.path.join(output_dir, f"{video_name}-speedy.{video_extension}")
        cropped_video = os.path.join(cropped_dir, f"{video_name}.{video_extension}")

        # Speed up the video.
        subprocess.run(["ffmpeg", "-i", file_path, "-vf", f"setpts={speedup}*PTS", "-pix_fmt", "yuv420p", speedy_video], check=True)

        # Trim the video.
        subprocess.run(["ffmpeg", "-i", speedy_video, "-ss", trim_amount, "-pix_fmt", "yuv420p", cropped_video], check=True)

# Change directory to the cropped directory.
os.chdir(cropped_dir)

# Create a file listing all the videos in the current directory.
with open("concat.txt", "w") as f:
    for file_name in os.listdir():
        if file_name.endswith(video_extension):
            f.write(f"file '{file_name}'\n")

# Concatenate all the videos using the file listing.
subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", "-pix_fmt", "yuv420p", os.path.join(output_dir, output_file_name)], check=True)
