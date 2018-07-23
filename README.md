# PCB Template Matching 📸

## Intro 🔬
This is a CLI tool built using Python bindings for OpenCV to explore template matching. It is intended to take an image or 
video of a pcb, along with a config file of known landmarks that exist on the board. This config file is referred to agaisnt
a pre-filled library of images of these landmarks, and then looked for in the image/video.

## Usage 💻

Some samples:

`python3 main.py -p ridago_gnd -t 0.66 -m image`

`python3 main.py -p rigado -t 0.7 -m video`

`python3 main.py -p ledboard_hole -t 0.66 -m image`

## Todo 🗒

- Make useful data out of actual landmark positions versus expected positions
