# P3-G1

Nesting 2d and gcode generation application

## Requirements

- [Docker](https://www.docker.com/products/docker-desktop/)
- [VcXsrv](https://sourceforge.net/projects/vcxsrv/) - for viewing GUI on Windows

## Installation

### Step 1: Build the Docker Image

First, you need to build the Docker image. Open a terminal and run the following command:

    docker build -t optinest .

### Step 2: Configure VcXsrv

VcXsrv is an X server for Windows. To use it, you need to download and install it from [here](https://sourceforge.net/projects/vcxsrv/).

After installation, you need to start VcXsrv.

### Step 3: Run the Docker Container

**On Windows**

Once VcXsrv is running, you can start the Docker container with the following command:

    docker run --rm -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix optinest

Alternatively, you can run VcXsrv and start Docker container in one line using PowerShell:

    Start-Process -FilePath 'C:\path\to\vcxsrv.exe' ; docker run -it --rm -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix optinest

Replace `C:\path\to\vcxsrv.exe` with the actual path where `vcxsrv.exe` is located.

**On Linux**

If you are on Linux, you only need to run the Docker container. Use the following command:

    docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix optinest

## Usage

After following the installation steps, the application should be running inside the Docker container.

### Common Issues

- **Docker not detecting DISPLAY environment variable on Windows**: Make sure VcXsrv is running and that you have set the `DISPLAY` variable correctly.
- **Permission issues**: Ensure Docker has access to the necessary directories and that VcXsrv is configured without access control.

### Stopping the Application

To stop the application, you can simply close the Docker container. If you started VcXsrv manually, you can stop it by closing the VcXsrv window.
