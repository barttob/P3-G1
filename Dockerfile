FROM ubuntu:jammy

ENV DISPLAY=:0
ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install -y \
    python3 python3-pip python3-pynest2d python3-pyqt5 \
    xcb x11-apps python3-pyqt5.qtwebkit \
    wget unzip gdebi xvfb

RUN pip install matplotlib pyqt5 svg.path ezdxf pygcode svg-to-gcode


COPY ODAFileConverter_QT5_lnxX64_8.3dll_25.1.deb /app/tmp/

RUN gdebi -n /app/tmp/ODAFileConverter_QT5_lnxX64_8.3dll_25.1.deb

RUN ln -s /usr/lib/x86_64-linux-gnu/libxcb-util.so.1 /usr/lib/x86_64-linux-gnu/libxcb-util.so.0

WORKDIR /app

COPY . /app

CMD ["python3", "main.py"]
