# Dockerfile for Dark Dark Go crawlers.
# 12/5/17
# matthewjones@bennington.edu
FROM ubuntu:16.04

MAINTAINER Matt Jones <"matthewjones@bennington.edu">

RUN apt-get update -y
RUN apt-get install -y \
    python3 \
    python3-pip \
    tor \
    nano

RUN mkdir /data

COPY ./crawler /app/crawler
COPY ./crawler/123 /data
COPY ./chunk_reader /app/crawler/chunk_reader

WORKDIR /app/crawler

RUN pip3 install -r dependencies.txt
RUN pip3 install requests[socks]

EXPOSE 5000
EXPOSE 9150

CMD ["/app/crawler/crawler_script.sh"]

