#From python:3.8.14-alpine3.15
#FROM ubuntu:latest
FROM --platform=linux/amd64 praru15/machinelearning_base:latest

COPY object-detection /root/object-detection/
WORKDIR /root/object-detection
RUN    python3 -m pip install --upgrade pip && \
       pip3 install -r requirements.txt

