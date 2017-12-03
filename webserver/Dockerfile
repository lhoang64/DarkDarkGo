FROM node:8.8.1

#nginx installation and config
RUN apt-get update
RUN apt-get -y install Nginx
RUN apt-get -y install nano
RUN apt-get -y install lsof
RUN apt-get install net-tools
COPY nginxconf /etc/nginx/sites-available
RUN rm /etc/nginx/sites-available/default
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/nginxconf /etc/nginx/sites-enabled/nginxconf

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir -p /usr/src/server
ADD . /usr/src/server

WORKDIR /usr/src/server
RUN npm install
RUN npm install pm2 -g

EXPOSE 80

# For keymetrics
EXPOSE 43554

ENTRYPOINT ["bash", "start.sh"]

