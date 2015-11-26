#! /bin/sh
export SDEV_HOME=/home/james.morris/PythonDev/Django/Weather
export LEGO_HOME=/home/pi/rpi/Weather
export CAMERA_HOME=/home/pi/lcd

cd $SDEV_HOME

export DBF1=$SDEV_HOME/Weather.db
export DBF2=$DBF1.sav

mv $DBF1 $DBF2

scp pi@CamPi.local:$LEGO_HOME/Weather.db $SDEV_HOME/Weather.db
# scp pi@192.168.1.105:LEGO_HOME/Weather.db $SDEV_HOME/Weather.db
if ! [ -a $DBF1 ]
  then
    mv $DBF2 $DBF1
fi

python $SDEV_HOME/temperature/GenerateD3Data.py > /dev/null 2>&1
