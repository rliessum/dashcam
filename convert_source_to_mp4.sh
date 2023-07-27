#!/bin/bash

handle_error() {
  echo "Error: $1"
  exit 1
}

# Check if ffmpeg and ffprobe are installed.
command -v ffmpeg >/dev/null 2>&1 || { echo >&2 "ffmpeg is required but it's not installed. Aborting."; exit 1; }
command -v ffprobe >/dev/null 2>&1 || { echo >&2 "ffprobe is required but it's not installed. Aborting."; exit 1; }

# Input and output directories.
input_dir="./input"
output_dir="./output"

# Check if input directory exists.
if [ ! -d "${input_dir}" ]; then
  handle_error "Input directory does not exist."
fi

# Create output directory if it doesn't exist.
mkdir -p "${output_dir}"

# Loop through all the AVI files in the input directory.
for input_file in "${input_dir}"/*.avi; do
  base_name=$(basename "${input_file}")
  video_name="${base_name%.*}"

  # Check if the file is non-interleaved.
  if ffprobe -i "${input_file}" 2>&1 | grep -q "non-interleaved AVI"; then
    echo "The video ${base_name} is non-interleaved. Converting to MP4..."
    # Temporarily convert the video to MP4.
    temp_file="${output_dir}/${video_name}_temp.mp4"
    ffmpeg -i "${input_file}" -pix_fmt yuv420p "${temp_file}" || handle_error "Converting video to MP4 failed"
    # Use the MP4 video as the input for the next steps.
    input_file="${temp_file}"
  else
    echo "The video ${base_name} is interleaved."
  fi

  # Convert the pixel format and strip the audio.
  output_file="${output_dir}/${video_name}_no_audio.mp4"
  ffmpeg -i "${input_file}" -pix_fmt yuv420p -an "${output_file}" || handle_error "Converting pixel format and stripping audio failed"

  # If a temporary MP4 video was created, delete it.
  if [[ -e "${temp_file}" ]]; then
    rm "${temp_file}"
  fi
done
