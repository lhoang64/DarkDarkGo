pm2 start /usr/src/server/server.js -i 0 &
sleep 5 &
service nginx restart