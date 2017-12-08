# Dockerfile for Dark Dark Go crawlers.
# 12/5/17
# matthewjones@bennington.edu
FROM ubuntu:16.04

MAINTAINER Matt Jones "matthewjones@bennington.edu"

COPY . /app

WORKDIR /app

RUN apt-get update -y
RUN apt-get install -y \
    python3 \
    python3-pip \
    tor

RUN pip3 install -r dependencies.txt # TODO: I'm not sure this will install
                                     # the sock sub-lib correctly.
RUN tor

ENTRYPOINT ["python3"]
CMD [
"crawl_server.py",
"--port", "5000",
"--threads", "4",
"--user-agent", "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0", # TODO : be honest
"--queue-host", "", # FIXME
"--queue-port", "", # FIXME
"--mgmt-host", "", # FIXME
"--mgmt-port", "", # FIXME
]
