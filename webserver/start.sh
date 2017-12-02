NODE_PORT=8080 node /usr/src/server/server.js &
NODE_PORT=8081 node /usr/src/server/server.js &
NODE_PORT=8082 node /usr/src/server/server.js &
service nginx restart