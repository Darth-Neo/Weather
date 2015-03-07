#! /bin/sh
 
cd /home/james.morris/rpi/Weather
mv /home/james.morris/rpi/Weather/Weather.db /home/james.morris/rpi/Weather/Weather.db.sav
scp pi@192.168.1.103:/home/pi/rpi/Weather/Weather.db /home/james.morris/rpi/Weather/Weather.db

