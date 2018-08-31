#!/usr/bin/python3
import Pyro4
from subprocess import call
import datetime
import shlex
import time
import picamera
import os

screenBrightnessFile = "/home/osmc/git/PythonScripting/brightnessFile"
screenBacklightFile = "/home/osmc/git/PythonScripting/backlightFile"
runningLogFile = "/home/osmc/git/PythonScripting/running.log"
camera = picamera.PiCamera()
videoTemp = '/home/osmc/camera/temp/'
videoSaved = '/home/osmc/camera/video/'
picSaved = '/home/osmc/camera/pic/'
currentVolume = 0
adjustingVolume = 0
i = 0

#Camera settings with default values
camera.sharpness = 0
#camera.contrast = 0
camera.contrast = 50
#camera.brightness = 50
camera.brightness = 75
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
#camera.vflip = False
camera.vflip = True
camera.crop = (0.0, 0.0, 1.0, 1.0)

#=========================
# Files required to set permissions
#=========================

call(shlex.split('sudo chmod 777 ' + screenBacklightFile))
call(shlex.split('sudo chmod 777 ' + screenBrightnessFile))
call(shlex.split('sudo chmod 777 ' + runningLogFile))
#call(shlex.split('python3 -m Pyro4.naming &'))

#=========================
# PiCamera Video functions
#=========================

@Pyro4.expose
class saveLastMinuteVideo(object):
    def saveLastMin(self, value):
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        currentTimeSansThree = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        cTST = datetime.datetime.now() - datetime.timedelta(minutes=3)
        return cTST.strftime('%Y-%m-%d_%H.%M.%S')

#===============================
# Actions for videoControl class
# 0-start 1-stop camera preview
# 2-start 3-stop camera recording
# 4-Take picture from camera
# 5-Change cameras brightness
# 6-Save last minute of video
#===============================

@Pyro4.expose
class videoControl(object):
  def video_control(self, action, val): #add a 3rd var for naming the camera setting to update global variables
    fileName = os.path.join(videoTemp, datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264'))
    global recordingStatus
    recordingStatus = 0


    if action == '':
      return "100 No action specified 0-6"

    if action == 0:
      #Do i have to return the start_preview() function for it to display
      camera.start_preview()
      return "200 Preview Started"
    
    if action == 1:
      camera.stop_preview()
      return "200 Preview Stopped"
    
    if action == 2:
      if recordingStatus == 0:
        camera.start_recording(fileName)
        recordingStatus = 1
        return("200 Recording Started " + str(recordingStatus))
      else:
        return "100 Recording Running"
    
    if action == 3:
      if recordingStatus == 1:
        camera.stop_recording()
        recordingStatus = 0
        return("200 Recording Stopped " + str(recordingStatus))
      else:
        return("100 Recording Not Running " + str(recordingStatus))

    if action == 4:
      picFileName = os.path.join(picSaved, datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg'))
      camera.capture(picFileName)
      return("200 Picture Taken")

    if action == 5:
      camera.brightness = int(val)
      return("200 Camera Brightness " + str(val))

    if action == 6:
      if recordingStatus == 1:
        camera.stop_recording()
        recordingStatus = 0
        call(shlex.split('for file in $(find ~/camera/temp/ -type f -mmin -2 -name *h264 -print);do mv $file ~/camera/saved;done'))
        camera.start_recording(fileName)
        recordingStatus = 1
        return("200 Last Two Minutes Saved")
      if recordingStatus == 0:
        call(shlex.split('for file in $(find ~/camera/temp/ -type f -mmin -2 -name *h264 -print);do mv $file ~/camera/saved;done'))
        return("200 Last Two Minutes Saved")
      else:
        return("100 Something went wrong")

    if action == 7:
      global i
      temp = i
      i = val
      
      return("i = " + str(val) + ". temp = " + str(temp))

    else:
      return("100 Action Unknown" + str(action))


#=========================
# System suspend functions
#=========================

@Pyro4.expose
class suspendSystem(object):
    def suspend_system_now(self, value):
        call(shlex.split('xbmc-send --action="PlayerControl(Stop)"'))
        backlightFile = open(screenBacklightFile, 'w')
        backlightFile.write('0')
        backlightFile.close()
        logFile = open(runningLogFile, 'a') 
        logFile.write('PyroHost suspended the system.\n') 
        logFile.close()
        return "200 Suspended System"

@Pyro4.expose
class resumeSystem(object):
    def resume_system_now(self, value):
        backlightFile = open(screenBacklightFile, 'w')
        backlightFile.write('1')
        backlightFile.close()
        logFile = open(runningLogFile, 'a')                                                                  
        logFile.write('PyroHost resumed the system.\n')             
        logFile.close()
        if currentVolume > 75:
          loweredVolume = int(currentVolume) - 50
          adjustingVolume = int(currentVolume)
        if currentVolume != adjustingVolume:
          

        #I may have to break out of the function to insert the variable loweredVolume
        call(shlex.split('xbmc-send --action="SetVolume(percent[$loweredVolume])"'))
        call(shlex.split('xbmc-send --action="PlayerControl(Play)"'))
        while int(loweredVolume) < int(currentVolume):
          loweredVolume = loweredVolume + 5
          if loweredVolume > 100:
            loweredVolume = 100
          call(shlex.split('xbmc-send --action="SetVolume(percent[$loweredVolume])"'))
          sleep(0.5)
          if currentVolume != adjustingVolume:
            loweredVolume = currentVolume
            break
        return "200 Suspended Resumed"

@Pyro4.expose
class screenBrightness(object):
  def brightnessChanger(self, val):
    if int(val) > 0 and int(val) < 255:
      if val in open(screenBrightnessFile, 'r').read():
        logFile = open(runningLogFile, 'a')
        logFile.write('PyroHost attempted to write ' + str(val) + ' to ' + str(screenBrightnessFile) + '.\n')
        logFile.close()
        return "100 Brightness already {0}.".format(val) 
      else: 
        screenFile = open(screenBrightnessFile, 'w') 
        screenFile.write(val) 
        screenFile.close() 
        logFile = open(runningLogFile, 'a') 
        logFile.write('PyroHost wrote ' + str(val) + ' to ' + str(screenBrightnessFile) + '.\n') 
        logFile.close() 
        return "200 Brightness changed to {0}.".format(val) 
    else:                                                                                                    
      return "100 Not a valid value 0-255"

@Pyro4.expose
class screenBacklight(object):
  def backlightChanger(self, val):
    if int(val) == 1 or int(val) == 0:
      sbl = open(screenBacklightFile, 'w')
      sbl.write(val)
      sbl.close()
      return "200 Backlight changed to {0}.".format(val)
    else:
      return "100 Backlight value out of range 0-1"

@Pyro4.expose
class volumeControl(object):
  def adjustVolume(self, volChange): # Accepts -100..100 % change to current volume or mute if 0
    prevVol = currentVolume
    if int(volChange) == 0:
      currentVolume = 0
    if currentVolume > 100:
      currentVolume = 100
    else:
      currentVolume = int(currentVolume) + int(volChange)
    call(shlex.split('xbmc-send --action="SetVolume(percent[$currentVolume])"'))
    return "200 Volume Set From {0} to {1}.".format(prevVol, currentVolume)



daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(screenBrightness) # register the greeting maker as a Pyro object
ns.register("screen.brightness", uri)   # register the object with a name in the name server
uri = daemon.register(screenBacklight)
ns.register("screen.backlight", uri)
uri = daemon.register(saveLastMinuteVideo) # register saving the last minute of video object
ns.register("save.lastMinuteVideo", uri)   # registering the object with NS
uri = daemon.register(suspendSystem)
ns.register("system.suspend", uri)
uri = daemon.register(resumeSystem)
ns.register("system.resume", uri)
uri = daemon.register(videoControl)
ns.register("control.video", uri)
uri = daemon.register(volumeControl)
ns.register("control.volume", uri)


print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
