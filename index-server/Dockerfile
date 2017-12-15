FROM ubuntu:latest
MAINTAINER Nayeem Aquib <nayeemaquib@bennington.edu>

RUN apt-get clean && apt-get update && apt-get install -y \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nano\
	--no-install-recommends && \
	rm -rf /var/lib/apt/lists/* && \
	apt-get clean

RUN pip3 install --upgrade pip

RUN mkdir -p /usr/src/index-server

ADD . /usr/src/index-server
WORKDIR /usr/src/index-server

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=index-server/idx_server.py

CMD ./start.sh
