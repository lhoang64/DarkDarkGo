kill -9 $(lsof -t -i:8080 -sTCP:LISTEN)
kill -9 $(lsof -t -i:8081 -sTCP:LISTEN)
kill -9 $(lsof -t -i:8082 -sTCP:LISTEN)
service nginx stop