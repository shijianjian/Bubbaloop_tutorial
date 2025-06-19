# Bubbaloop 101: Turn Your iPhone into a Security Camera System

Bubbaloop is a powerful tool that allows you to transform your iPhone into a security camera using RTSP streams. This tutorial will guide you through the setup and usage process.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setting Up the RTSP Stream](#setting-up-the-rtsp-stream)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Bubbaloop](#running-bubbaloop)
- [Viewing the Camera Feed](#viewing-the-camera-feed)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.x
- CMake
- GStreamer
- Rust
- Rerun-sdk
- iPhone (for using your phone as a camera) or access to public RTSP streams


For Mac users, installing cmake and GStreamer are mandatory:
```bash
brew reinstall gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly
```
For linux users:
```bash
cp install_linux.sh ./bubbaloop/scripts
cd bubbaloop
./scripts/install_linux.sh
```

## Setting Up the RTSP Stream

You have two options for setting up your RTSP stream:

### Option 1: Using Your iPhone

1. Download and install `IP Camera Lite` from the App Store
2. Launch the app and enable the IP Camera server (toggle at the bottom)
3. To get your credentials:
   - Tap the top-right dropdown menu
   - Select "Settings"
   - Note down your username and password
4. The app will display your RTSP stream URL (you may verify the RTSP stream on a webpage).

### Option 2: Using Public RTSP Streams

If you can't use your iPhone or want to test with public streams:
1. Visit [rtsp.stream](https://www.rtsp.stream/admin/teststream)
2. Select a test stream from their collection

To verify your RTSP stream is working:
```bash
gst-launch-1.0 rtspsrc location=rtsp://admin:admin@10.240.40.255:8554/live ! decodebin ! fakesink
```

Or for a visualization, you may try with VLC or FFPLay:
```bash
vlc rtsp://YOUR_RTSP_LINK
```
or using ffplay
```bash
ffplay rtsp://YOUR_RTSP_LINK
```

## Installation

1. Clone the repository and initialize submodules:
```bash
git submodule update --init --recursive
```

2. Copying the `Cargo.lock` for a better reproducibility.
```bash
cp Cargo.lock ./bubbaloop
```

## Configuration

Generate the camera configuration file using our Python script. You have two options:

### Single Camera Setup (Recommended for Beginners)

For a public stream:
```bash
python generate_camera_config.py \
  --rtsp_streams rtsp://rtspstream:4j_U0tJ6fGtiaKREnuVnH@zephyr.rtsp.stream/movie \
  --output_path ./bubbaloop/src/cu29/pipelines/streaming.ron
```

For your iPhone feed:
```bash
python generate_camera_config.py \
  --rtsp_streams rtsp://admin:admin@10.240.40.255:8554/live \
  --output_path ./bubbaloop/src/cu29/pipelines/cameras_1.ron
```

### Multiple Camera Setup (Up to 4 Cameras)
```bash
python generate_camera_config.py \
  --output_path ./bubbaloop/src/cu29/pipelines/cameras_1.ron \
  --rtsp_streams rtsp://STREAM1_URL rtsp://STREAM2_URL
```

## Running Bubbaloop

Get into the bubbaloop folder:
```bash
cd bubbaloop
```

1. In a new terminal, access the container:
```bash
just serve
```

2. Start the pipeline:
```bash
just start-pipeline cameras 0.0.0.0 3000
```

## Viewing the Camera Feed

1. Navigate to the bubbaloop directory:
```bash
cd bubbaloop
```

2. Start the client viewer:
```bash
python examples/python-streaming/client.py --host 0.0.0.0 --port 3000
```

![](https://kornia.gitbook.io/~gitbook/image?url=https%3A%2F%2Fgithub.com%2Fkornia%2Fdata%2Fblob%2Fmain%2Fbubbaloop%2Fbubbaloop_inference.png%3Fraw%3Dtrue&width=768&dpr=2&quality=100&sign=191d02ea&sv=2)

## Troubleshooting

- If you can't access the RTSP stream, verify that:
  - Your iPhone and computer are on the same network (if using iPhone)
  - The RTSP URL is correct
  - The stream credentials are valid
  - Your firewall isn't blocking the connection

For additional help or to report issues, please visit our GitHub repository.
