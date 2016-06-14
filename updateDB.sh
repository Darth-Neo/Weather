#! /bin/sh
export SDEV_HOME=/home/james.morris/PythonDev/Django/Weather
export 
export WEATHER_HOME=/home/pi/rpi

cd $SDEV_HOME

export DBF1=$SDEV_HOME/Weather.db
export DBF2=$DBF1.sav

mv $DBF1 $DBF2

scp pi@WeatherPi.local:rpi/Weather.db $SDEV_HOME/Weather.db
if ! [ -a $DBF1 ]
  then
    mv $DBF2 $DBF1
fi

python $SDEV_HOME/temperature/GenerateD3Data.py > /dev/null 2>&1
