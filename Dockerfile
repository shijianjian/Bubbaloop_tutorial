FROM ubuntu:22.04

# Set non-interactive frontend
ENV DEBIAN_FRONTEND=noninteractive

# First, install pkg-config and essential build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    ca-certificates \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    gdb \
    software-properties-common \
    wget \
    nasm \
    libssl-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    libgstreamer-plugins-good1.0-dev \
    gstreamer1.0-plugins-bad \
    libgstreamer-plugins-bad1.0-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PKG_CONFIG=/usr/bin/pkg-config
ENV PKG_CONFIG_PATH="/usr/lib/x86_64-linux-gnu/pkgconfig"
ENV OPENSSL_DIR="/usr"
ENV OPENSSL_LIB_DIR="/usr/lib/x86_64-linux-gnu"
ENV OPENSSL_INCLUDE_DIR="/usr/include"

# Set working directory
WORKDIR /app

# Copy app files
COPY examples examples
COPY scripts scripts
COPY src src
COPY Cargo.toml .
COPY Cross.toml .
COPY README.md .
COPY build.rs .
COPY justfile .
COPY package.json .
COPY package-lock.json .

# Run installation script
RUN /app/scripts/install_linux.sh
# RUN systemctl status bubbaloop
# RUN sudo journalctl -u bubbaloop.service -f

ENTRYPOINT ["just", "serve"]
