#!/bin/bash

#kill $(ps -ef | grep pyroHost | grep -v grep | awk '{print $2}')
for pid in $( ps -ef | egrep 'Pyro4.naming|pyroHost|interpreterForArduino' | grep -v grep | awk '{print $2}' );
  do sudo kill $pid;
done

sleep 1
sudo chmod 777 /dev/ttyUSB*
sleep 1
python3 -m Pyro4.naming &
sleep 1
python3 /home/osmc/git/PythonScripting/pyroHost.py &
sleep 1
python3 /home/osmc/git/RPi3Carputer/interpreterForArduino.py &
sleep 1
echo "System Ready"
exit
