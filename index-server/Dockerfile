FROM ubuntu:latest
MAINTAINER Nayeem Aquib <nayeemaquib@bennington.edu>

RUN apt-get clean && apt-get update && apt-get install -y \
	python-dev \
	python-setuptools \
	python-pip \
	nano\
	--no-install-recommends && \
	rm -rf /var/lib/apt/lists/* && \
	apt-get clean

RUN pip install --upgrade pip

RUN mkdir -p /usr/src/index-server

ADD . /usr/src/index-server
WORKDIR /usr/src/index-server

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=index-server/idx_server.py

CMD /usr/local/bin/flask run --host=0.0.0.0

