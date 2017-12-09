# Dockerfile for Dark Dark Go crawlers.
# 12/5/17
# matthewjones@bennington.edu
FROM ubuntu:16.04

MAINTAINER Matt Jones <"matthewjones@bennington.edu">

COPY ./crawler /app/crawler
COPY ./chunk_reader /app/crawler/chunk_reader

WORKDIR /app/crawler

RUN apt-get update -y
RUN apt-get install -y \
    python3 \
    python3-pip \
    tor

RUN mkdir /data

RUN pip3 install -r dependencies.txt

CMD ["/app/crawler/crawler_script.sh"]

