#!/usr/bin/sh
nohup ./manage.py runserver 0.0.0.0:9000 > ./logs/Weather.log 2>&1 &
