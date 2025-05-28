FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# --- Install base dependencies ---
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && apt-get update

# --- Install required packages ---
RUN apt-get install -y \
    python3 python3-pip python3-gi python3-gst-1.0 \
    libgirepository1.0-dev \
    gir1.2-gst-rtsp-server-1.0 \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio \
    libcairo2-dev pkg-config python3-dev build-essential \
    ninja-build \
    iputils-ping \
    && apt-get clean

# --- Install newer version of meson via pip ---
RUN pip3 install --no-cache-dir meson>=0.63.3

# --- Set working directory ---
WORKDIR /app

# --- Copy app files ---
COPY requirements.txt .
COPY multi_rtsp_server.py .
COPY web_viewer.py .

# --- Install Python dependencies ---
RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "multi_rtsp_server.py"]

# # --- Create startup scripts ---
# RUN echo '#!/bin/bash\n\
# # Add host.docker.internal to /etc/hosts if it doesn'\''t exist\n\
# if ! grep -q "host.docker.internal" /etc/hosts; then\n\
#     echo "Adding host.docker.internal to /etc/hosts"\n\
#     echo "host.docker.internal host.docker.internal" >> /etc/hosts\n\
# fi\n\
# \n\
# case "$1" in\n\
#   "rtsp")\n\
#     python3 multi_rtsp_server.py "${@:2}"\n\
#     ;;\n\
#   "viewer")\n\
#     python3 web_viewer.py\n\
#     ;;\n\
#   "both")\n\
#     python3 multi_rtsp_server.py "${@:2}" &\n\
#     python3 web_viewer.py &\n\
#     wait\n\
#     ;;\n\
#   *)\n\
#     echo "Usage: $0 {rtsp|viewer|both} [rtsp_args...]"\n\
#     echo "  rtsp    - Run only the RTSP server"\n\
#     echo "  viewer  - Run only the web viewer"\n\
#     echo "  both    - Run both services"\n\
#     exit 1\n\
#     ;;\n\
# esac' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# # --- Expose ports ---
# EXPOSE 8554 5000

# # --- Entrypoint ---
# ENTRYPOINT ["/app/entrypoint.sh"]
