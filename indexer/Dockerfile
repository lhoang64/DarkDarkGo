FROM ubuntu:latest
MAINTAINER Dung Le <dungle@bennington.edu>

RUN apt-get update && apt-get install -y \
	curl \
	python-dev \
	python-setuptools \
	python-pip \
	--no-install-recommends && \
	rm -rf /var/lib/apt/lists/* && \
	apt-get clean

RUN pip install --upgrade pip
RUN pip install -I flask==0.12.0

ADD . /usr/src/indexer
WORKDIR /usr/src/indexer

EXPOSE 5000

ENV FLASK_APP=index_builder_server.py

CMD /usr/local/bin/flask run --host=0.0.0.0