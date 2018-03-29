# saved as greeting-client.py
import Pyro4
import os
import datetime
import time

#val = input("Brightness level? ").strip()
#value = input("Save? (Y/n)").strip()

#brightness_changer = Pyro4.Proxy("PYRONAME:change.brightness")    # use name server object lookup uri shortcut
#print(brightness_changer.brightnessChanger(val))

#save_last_minute_video = Pyro4.Proxy("PYRONAME:save.lastMinuteVideo")
#print(save_last_minute_video.saveLastMin(value))

def start():
  action = input('(B)rightness? 1-100 Or (Start) Preview and (Stop) Preview. Also (Exit)\n')

  if action.lower() == 'b':
    action2 = 0
    action2 = input('Brightness level? 1-100\n')
    
    if int(action2) > 0 and int(action2) < 101:
      val = action2
      brightness_changer = Pyro4.Proxy("PYRONAME:change.brightness")
      print(val, action2)
      print(brightness_changer.brightnessChanger(val))
      return(start())
    else:
      print('Value not in range 1-100\n')
      return(start())

  if action.lower() == 'start':
    val = 0
    videoControl = Pyro4.Proxy("PYRONAME:control.video")
    print(videoControl.video_control(int(0)))
    return(start())

  if action.lower() == 'stop':
    videoControl = Pyro4.Proxy("PYRONAME:control.video") 
    print(videoControl.video_control(1))   
    return(start())

  if action.lower() == 'exit':   
    exit()

  else:
    print('Entry not valid, try again.. stupid.')
    return(start())

print(start())

exit()
