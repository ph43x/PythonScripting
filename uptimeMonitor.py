#!/usr/bin/python3

import requests
import re
import subprocess
import os
import logging
from datetime import datetime

def executeCmd(host):
  full_command = f'ping -c 1 {host}'
  results = os.system(full_command)
  return results

fileOutput = open('result.out', 'a', encoding="utf-8")
targetList = open('pingTargets.list', 'r', encoding="utf-8")
with open('pingTargets.list') as f:
  host = f.read().splitlines()

for line in host:
  #resultOutput = executeCmd(line)
  fileOutput.write(str(datetime.now()))
  full_command = f'ping -c 1 {line} >> result.out'
  results = os.system(full_command)
  #print(datetime.now())
  #fileOutput.write(results)
  fileOutput.write('\n')
  #print(line)
  print(results)
  #results = [i for i in results if i.find(" 0% packet loss") > 0]
  #if not resultOutput:
  #  fileOutput.write(datetime.datetime, " FAILURE ", host)
  #else:
  #  fileOutput.write(datetime.datetime, " SUCCESS ", host)
targetList.close()
fileOutput.close()
