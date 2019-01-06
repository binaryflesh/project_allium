FROM alpine:latest

WORKDIR /app
COPY . /app
RUN apk update && \
    apk add python3 && \
    apk add curl && \
    apk add --update bash && \
    apk add py-pip && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Error response from daemon: Get https://registry-1.docker.io/v2/: 
# dial tcp: lookup registry-1.docker.io on 192.168.65.1:53: 
# server misbehaving
# docker-machine ssh default
# sudo vi /etc/resolv.conf
# change nameserver to 8.8.8.8

