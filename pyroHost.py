# saved as greeting-server.py
import Pyro4
from subprocess import call
import datetime
import shlex
import time

screenBrightnessFile = "/home/osmc/git/PythonScripting/brightnessFile"
screenBacklightFile = "/home/osmc/git/PythonScripting/backlightFile"
runningLogFile = "/home/osmc/git/PythonScripting/running.log"

@Pyro4.expose
class changeBrightness(object):
    def brightnessChanger(self, val):
        if val in open(screenBrightnessFile, 'r').read(): #add the check for max brightness here
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

@Pyro4.expose
class saveLastMinuteVideo(object):
    def saveLastMin(self, value):
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        currentTimeSansThree = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        cTST = datetime.datetime.now() - datetime.timedelta(minutes=3)
        
        return cTST.strftime('%Y-%m-%d_%H.%M.%S')

@Pyro4.expose
class suspendSystem(object):
    def suspendSystemNow(self, value):
        call(shlex.split('xbmc-send --action="PlayerControl(Stop)"'))
        backlightFile = open(screenBacklightFile, 'w')
        backlightFile.write('0')
        backlightFile.close()
        logFile = open(runningLogFile, 'a')                                                                  
        logFile.write('PyroHost suspended the system.\n')             
        logFile.close()

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(changeBrightness) # register the greeting maker as a Pyro object
ns.register("change.brightness", uri)   # register the object with a name in the name server
uri = daemon.register(saveLastMinuteVideo) # register saving the last minute of video object
ns.register("save.lastMinuteVideo", uri)   # registering the object with NS
uri = daemon.register(suspendSystem)
ns.register("system.suspend", uri)
#uri = daemon.register(resumeSystem)
#ns.register("system.resume")

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
