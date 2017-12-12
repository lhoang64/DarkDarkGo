FROM node:8.8.1

#nginx installation and config
RUN apt-get update &&\
    apt-get -y install Nginx
COPY nginxconf /etc/nginx/sites-available
RUN rm /etc/nginx/sites-available/default &&\
    rm /etc/nginx/sites-enabled/default &&\
    ln -s /etc/nginx/sites-available/nginxconf /etc/nginx/sites-enabled/nginxconf

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir -p /usr/src/search
ADD . /usr/src/search

WORKDIR /usr/src/search
RUN npm install &&\
    npm run build
    
EXPOSE 80

ENTRYPOINT ["service", "nginx", "start"]