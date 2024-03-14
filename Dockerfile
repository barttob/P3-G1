FROM ubuntu:jammy

ENV DISPLAY=:0
ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install -y \
    python3 python3-pip python3-pynest2d python3-pyqt5 \
    xcb x11-apps python3-pyqt5.qtwebkit

RUN pip install matplotlib pyqt5 svg.path ezdxf 

WORKDIR /app

COPY . /app

CMD ["python3", "main.py"]
