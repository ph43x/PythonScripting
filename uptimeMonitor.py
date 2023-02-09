#!/usr/bin/python3

import os
from datetime import datetime

def executeCmd(host):
  full_command = f'ping -c 1 {host}  >> result.out'
  results = os.system(full_command)
  return str(datetime.now())

def start():
  targetList = open('pingTargets.list', 'r', encoding="utf-8")
  fileOutput = open('result.out', 'a', encoding="utf-8")
  fileOutput.write(str(datetime.now()))
  fileOutput.write('\n')

  with open('pingTargets.list') as f:
    host = f.read().splitlines()

  for line in host:
    executeCmd(line)
  targetList.close()
  fileOutput.close()
  cleanup = os.system("sed -i 's/^PING.*//;s/^rtt.*//;s/^64.*//;/^$/d;' result.out")

start()
