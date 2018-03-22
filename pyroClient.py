# saved as greeting-client.py
import Pyro4

#val = input("Brightness level? ").strip()
value = input("Save? (Y/n)").strip()

#brightness_changer = Pyro4.Proxy("PYRONAME:change.brightness")    # use name server object lookup uri shortcut
#print(brightness_changer.brightnessChanger(val))

save_last_minute_video = Pyro4.Proxy("PYRONAME:save.lastMinuteVideo")
print(save_last_minute_video.saveLastMin(value))
