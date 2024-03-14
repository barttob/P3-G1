# P3-G1

## Requirements

- [Docker](hhttps://www.docker.com/products/docker-desktop/)
- [VcXsrv](https://sourceforge.net/projects/vcxsrv/) - for viewing GUI on windows

## Installation

Build image

    docker build -t optinest .

To run image you have to run **vcxsrv.exe** and then run docker image

    docker run --rm -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix optinest

You can do it in one line in PowerShell

    Start-Process -FilePath 'path\to\file\vcxsrv.exe' ; docker run --rm -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix optinest