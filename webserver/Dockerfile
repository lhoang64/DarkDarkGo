FROM node:8.8.1

#nginx installation and config
RUN apt-get update &&\
    apt-get -y install Nginx &&\
    apt-get -y install nano &&\
    apt-get -y install lsof &&\
    apt-get install net-tools &&\
COPY nginxconf /etc/nginx/sites-available
RUN rm /etc/nginx/sites-available/default &&\
    rm /etc/nginx/sites-enabled/default &&\
    ln -s /etc/nginx/sites-available/nginxconf /etc/nginx/sites-enabled/nginxconf

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir -p /usr/src/server
ADD . /usr/src/server

WORKDIR /usr/src/server
RUN npm install &&\
    npm install pm2 -g

EXPOSE 80
# For keymetrics, port 43554 should be open
EXPOSE 43554    

ENTRYPOINT ["bash", "start.sh"]
