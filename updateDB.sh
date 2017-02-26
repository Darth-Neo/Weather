#!/usr/bin/sh
export SDEV_HOME=/home/james/PythonDev/Weather/Weather
export WEATHER_HOME=/home/pi/rpi

cd $SDEV_HOME

export DBF1=$SDEV_HOME/Weather.db
export DBF2=$DBF1.sav

mv $DBF1 $DBF2

scp pi@WeatherPi.local:$WEATHER_HOME/Weather.db $SDEV_HOME/Weather.db

if ! [ -a $DBF1 ]
  then
    mv $DBF2 $DBF1
fi

python $SDEV_HOME/temperature/GenerateD3Data.py > /dev/null 2>&1
