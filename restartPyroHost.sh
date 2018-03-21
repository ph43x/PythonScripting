#!/bin/bash

kill $(ps -ef | grep pyroHost | grep -v grep | awk '{print $2}')
sleep 2
python3 pyroHost.py &
sleep 2
python3 pyroClient.py
