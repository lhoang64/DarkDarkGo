FROM ubuntu:latest
MAINTAINER Hoanh An <hoanhan@bennington.edu>

# Add the PostgreSQL PGP key to verify their Debian packages.
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Add PostgreSQL's repository. It contains the most recent stable release of PostgreSQL, ``9.3``.
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Install python dependencies
RUN apt-get update && apt-get install -y \
	curl \
	python-dev \
	python-setuptools \
	python-pip \
	postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3 \
	--no-install-recommends && \
	rm -rf /var/lib/apt/lists/* && \
	apt-get clean


# Install dependencies
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install -I flask==0.12.0
RUN pip install psycopg2

USER postgres

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `docker` owned by the ``docker`` role.
RUN    /etc/init.d/postgresql start &&\
    createdb -O postgres mgmt_db

#    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf


# Add working directory
ADD . /src
WORKDIR /src

EXPOSE 5000

# Note: PostgresQL run on port 5432

ENV FLASK_APP=device_manager_server.py

CMD ./start.sh