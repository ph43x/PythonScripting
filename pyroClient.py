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
  action = input('(Res)ume System, (Sus)pend System, (B)rightness, (Prev)iew Controls, (Rec)ording Controls, (Pic)ture, or (Exit)\n')

  if action.lower() == 'sus':
    action2 = input('Suspend System?\n')

    if action2.lower() == 'y':
      suspendSystem = Pyro4.Proxy("PYRONAME:system.suspend")
      print(suspendSystem.suspend_system_now(1))
      return(start())
    else:
      print('Not Suspending System\n')
      return(start())

  if action.lower() == 'res':
    action2 = input('Resume System?\n')

    if action2.lower() == 'y':
      resumeSystem = Pyro4.Proxy("PYRONAME:system.resume")
      print(resumeSystem.resume_system_now(0))
      return(start())
    else:
      print('Not Resuming System\n')
      return(start())

  if action.lower() == 'b':
    action2 = input('Camera Brightness? 1-100\n')
    
    if int(action2) > 0 and int(action2) < 101:
      val = action2
      videoControl = Pyro4.Proxy("PYRONAME:control.video")
      print(videoControl.video_control(5,int(val)))
      return(start())
    else:
      print('Value not in range 1-100\n')
      return(start())

  if action.lower() == 'prev':
    action2 = input('(Start) or (Stop) Preview?\n')
    
    if action2.lower() == 'start':
      videoControl = Pyro4.Proxy("PYRONAME:control.video")
      print(videoControl.video_control(int(0),int(0)))
      return(start())

    if action2.lower() == 'stop':
      videoControl = Pyro4.Proxy("PYRONAME:control.video") 
      print(videoControl.video_control(int(1),int(0)))   
      return(start())
    
    else:
      print('Try again...\n')
      return(start())

  if action.lower() == 'rec':
    action2 = input('(Start) or (Stop) Recording?\n')

    if action2.lower() == 'start':                        
      videoControl = Pyro4.Proxy("PYRONAME:control.video")
      print(videoControl.video_control(int(2),int(0)))  
      return(start())                                   
                                                        
    if action2.lower() == 'stop':                       
      videoControl = Pyro4.Proxy("PYRONAME:control.video")
      print(videoControl.video_control(int(3),int(0)))
      return(start())

    else:
      print('Try again...\n')
      return(start())

  if action.lower() == 'exit':   
    exit()

  if action.lower() == 'pic':
    videoControl = Pyro4.Proxy("PYRONAME:control.video")
    print(videoControl.video_control(4,0))
    return(start())

  else:
    print('Entry not valid, try again.. stupid.')
    return(start())

print(start())

exit()
