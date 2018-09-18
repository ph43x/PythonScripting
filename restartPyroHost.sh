#!/bin/bash

#kill $(ps -ef | grep pyroHost | grep -v grep | awk '{print $2}')

#May want to try disabling this next line, or the sudo part of it for kodi to be able to run it?
for pid in $( ps -ef | egrep 'pyroNaming|pyroHost|interpreterForArduino' | grep -v grep | awk '{print $2}' );
  do sudo kill $pid;
done

sleep 1
sudo chmod 777 /dev/ttyUSB*
sleep 1
python3 /home/osmc/git/PythonScripting/pyroNaming.py & > /dev/null 2>&1
sleep 1
python3 /home/osmc/git/PythonScripting/pyroHost.py & > /dev/null 2>&1
sleep 1
python3 /home/osmc/git/RPi3Carputer/interpreterForArduino.py & > /dev/null 2>&1
sleep 1
echo "System Ready"
exit
