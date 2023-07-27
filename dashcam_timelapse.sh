#!/bin/bash

# Function to handle errors.
handle_error() {
  echo "Error: $1"
  exit 1
}

# Check if ffmpeg is installed.
command -v ffmpeg >/dev/null 2>&1 || { echo >&2 "ffmpeg is required but it's not installed. Aborting."; exit 1; }

# Video file options and locations.
input_dir="./input"

# Output file options and locations. create with timestamp
timestamp=$(date +%Y%m%d%H%M%S)
output_dir="$(pwd)/output_${timestamp}"
mkdir -p "$output_dir"
output_file_name="timelapse.mp4"
video_extension="mp4"

# How much to speed up the clips.
speedup="0.05"

# How much to trim off each sped-up clip.
trim_amount="00.12"

# Check if input directory exists.
if [ ! -d "${input_dir}" ]; then
  handle_error "Input directory does not exist."
fi

# Create directories for processed and cropped files.
mkdir -p "${output_dir}/cropped"

# Define the absolute path to the cropped directory.
cropped_dir="${output_dir}/cropped"

# Loop through all the files, creating sped-up versions of each and then trimming.
for file in "${input_dir}"/*.${video_extension}; do
  base_name=$(basename "${file}")
  video_name="${base_name%.*}"
  speedy_video="${output_dir}/${video_name}-speedy.${video_extension}"
  cropped_video="${cropped_dir}/${video_name}.${video_extension}"

  # Speed up the video.
  ffmpeg -i "${file}" -vf "setpts=${speedup}*PTS" -pix_fmt yuv420p "${speedy_video}" || handle_error "Speeding up video failed"

  # Trim the video.
  ffmpeg -i "${speedy_video}" -ss "${trim_amount}" -pix_fmt yuv420p "${cropped_video}" || handle_error "Trimming video failed"
done

# Change directory to the cropped directory.
cd "${cropped_dir}"

# Create a file listing all the videos in the current directory.
ls *.${video_extension} | sed 's:\ :\ \\:g' | sed 's/^/file /' > "concat.txt" || handle_error "Creating list of files failed"

# Concatenate all the videos using the file listing.
ffmpeg -f concat -safe 0 -i "concat.txt" -c copy -pix_fmt yuv420p "${output_dir}/${output_file_name}" || handle_error "Concatenating videos failed"
