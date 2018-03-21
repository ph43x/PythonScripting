# saved as greeting-server.py
import Pyro4
from subprocess import call

screenBrightnessFile = "/home/osmc/git/PythonScripting/brightnessFile"
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
          #call(['echo "' + str(val) + '" > ' + str(screenBrightnessFile)])
          logFile = open(runningLogFile, 'a')
          logFile.write('PyroHost wrote ' + str(val) + ' to ' + str(screenBrightnessFile) + '.\n')
          logFile.close()
          return "200 Brightness changed to {0}.".format(val)

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(changeBrightness) # register the greeting maker as a Pyro object
ns.register("change.brightness", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
