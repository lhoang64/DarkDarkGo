FROM ubuntu:latest
MAINTAINER Nayeem Aquib <nayeemaquib@bennington.edu>

RUN apt-get update && apt-get install -y \
	curl \
	python-dev \
	python-setuptools \
	python3-pip \
	--no-install-recommends && \
	rm -rf /var/lib/apt/lists/* && \
	apt-get clean

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ADD . /usr/src/index-server
WORKDIR /usr/src/index-server

EXPOSE 8000

ENV FLASK_APP=index_server.py

CMD /usr/local/bin/flask run --host=0.0.0.0
