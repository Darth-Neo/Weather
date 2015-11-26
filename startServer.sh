#!/usr/bin/sh
nohup ./manage.py runserver 0.0.0.0:9000 > ./log.txt 2>&1 &
tail -f ./log.txt
