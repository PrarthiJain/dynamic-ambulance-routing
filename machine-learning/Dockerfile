#From python:3.8.14-alpine3.15
FROM ubuntu:latest

COPY object-detection /root/object-detection/
WORKDIR /root/object-detection

RUN apt update -y && apt install python3 pip -y
RUN    python3 -m pip install --upgrade pip && \
       pip3 install -r requirements.txt

RUN pip3 install tensorflow azure-storage-blob

RUN apt install ffmpeg libsm6 libxext6  -y
CMD ["python3", "yolo.py"]
