# Bubbaloop: Turn Your iPhone into a Security Camera System

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

- Docker installed on your system
- Python 3.x
- Git
- iPhone (for using your phone as a camera) or access to public RTSP streams

## Setting Up the RTSP Stream

You have two options for setting up your RTSP stream:

### Option 1: Using Your iPhone

1. Download and install `IP Camera Lite` from the App Store
2. Launch the app and enable the IP Camera server (toggle at the bottom)
3. To get your credentials:
   - Tap the top-right dropdown menu
   - Select "Settings"
   - Note down your username and password
4. The app will display your RTSP stream URL

### Option 2: Using Public RTSP Streams

If you can't use your iPhone or want to test with public streams:
1. Visit [rtsp.stream](https://www.rtsp.stream/admin/teststream)
2. Select a test stream from their collection

To verify your RTSP stream is working:
```bash
vlc rtsp://YOUR_RTSP_LINK
```

## Installation

1. Clone the repository and initialize submodules:
```bash
git submodule update --init --recursive
```

## Configuration

Generate the camera configuration file using our Python script. You have two options:

### Single Camera Setup (Recommended for Beginners)
```bash
python generate_camera_config.py \
  --rtsp_streams rtsp://rtspstream:4j_U0tJ6fGtiaKREnuVnH@zephyr.rtsp.stream/movie \
  --output_path ./bubbaloop/src/cu29/pipelines/streaming.ron
```

```bash
python generate_camera_config.py \
  --rtsp_streams rtsp://admin:admin@10.185.38.90:8554/live \
  --output_path ./bubbaloop/src/cu29/pipelines/streaming.ron
```

### Multiple Camera Setup (Up to 4 Cameras)
```bash
python generate_camera_config.py \
  --output_path ./bubbaloop/src/cu29/pipelines/streaming.ron \
  --rtsp_streams rtsp://STREAM1_URL rtsp://STREAM2_URL
```

## Running Bubbaloop

1. Build the Docker image:
```bash
sudo docker build -t bubbaloop_base .
```

2. Run the Docker container:
```bash
sudo docker run --network host --rm -it -p 3000:3000 bubbaloop_base
```

3. Get the container ID:
```bash
sudo docker ps
```

4. In a new terminal, access the container:
```bash
sudo docker exec -it $(sudo docker ps -q) /bin/bash
```

5. Start the pipeline:
```bash
just start-pipeline steaming 0.0.0.0 3000
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

## Troubleshooting

- If you can't access the RTSP stream, verify that:
  - Your iPhone and computer are on the same network (if using iPhone)
  - The RTSP URL is correct
  - The stream credentials are valid
  - Your firewall isn't blocking the connection

- If the Docker container fails to start:
  - Ensure port 3000 isn't being used by another application
  - Check if Docker has sufficient permissions

For additional help or to report issues, please visit our GitHub repository.
