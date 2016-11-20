#!/usr/bin/env sh
args=("$@")
export DIR="/home/james/PythonDev/Django"
source $DIR/bin/activate

# test
# $DIR/Weather/manage.py runserver 0.0.0.0:9000 > $DIR/Weather/logs/Weather.log

nohup $DIR/Weather/manage.py runserver 0.0.0.0:9000 > $DIR/Weather/logs/Weather.log 2>&1 &

if [ $1 ] 
then
    tail -f $DIR/Weather/logs/Weather.log 
fi
