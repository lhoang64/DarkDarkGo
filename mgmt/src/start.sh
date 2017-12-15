#!/usr/bin/env bash

/etc/init.d/postgresql start
sleep 5
cd database
./import.sh
cd ..
sleep 2
/usr/local/bin/flask run --host=0.0.0.0 &
sleep 5
python watchdog.py 2>&1