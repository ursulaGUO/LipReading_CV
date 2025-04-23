# Data 

The data are downloaded from Bernie Sanders' YouTube official account, where I only included videos where only Bernie is talking, and his face is (approximately) in the center. The video resolution is at 480p. 

With the videos, I also downloaded subtitles in txt files.

# Papers

https://ieeexplore.ieee.org/abstract/document/9837012

# Steps
## Preprocessing
In `src/builddata.py`, the file takes in a video and its corresponding `.src` subtitle file, and builds mini video data and a csv file that contains the lookup table for all the mini videos and their corresponding texual sentences. 

Run `make clean` to clear the old data in the output directory (remember to specify the output directory in the `Makefile`)
Run `make build` to start the video cutting 
