# saved as greeting-server.py
import Pyro4
screenBrightnessFile = "/home/mint/git/PythonScripting/brightnessFile"

@Pyro4.expose
class changeBrightness(object):
    def brightnessChanger(self, val):
        if val in open(screenBrightnessFile, 'r').read(): #add the check for max brightness here
          logFile = open('/home/mint/git/PythonScripting/running.log', 'a')
          logFile.write('PyroHost attempted to write $val to  $screenBrightnessFile .')
          logFile.close()
          return "100 Brightness already {0}.".format(val)
        else:
          file = open(screenBrightnessFile, 'w')
          file.write = ('{0}.format(val)')
          file.close()
          return "200 Brightness changed to {0}.".format(val)

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(changeBrightness) # register the greeting maker as a Pyro object
ns.register("change.brightness", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
