# Dashcam Time-lapse

This script combines separate recordings from a cheap Chinese dashcam into a single, streamlined time-lapse video. Initially, it takes .mp4 files and processes them into a time-lapse sequence. The need to convert the source files from .avi to .mp4 arose due to ffmpeg's limitations in optimally processing .avi files.

The foundational structure for this script was inspired by Jeff Geerling's [gist](https://gist.github.com/geerlingguy/d515b8e85242b1787a4bbdc21c037495), and was adapted to cater to my specific needs.

**Suboptimal Source Files:** If you have any issues with the concatenation process due to the suboptimal source files (as was the case with my .avi files from my dashcam), you can use the `convert_source_to_mp4.sh` script. This script will convert all .avi files in the `./input/` directory to .mp4 files.

**Optimal Source Files:** If your source files are already in a format that is usable with ffmpeg, the `dashcam_timelapse.sh` script will suffice. 

You can fine-tune the speedup and trim settings directly within the script. By default, it reads from the `./input/` directory and writes to the dynamically named `./output_{timestamp}/` directory.
