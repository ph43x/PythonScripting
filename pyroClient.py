# saved as greeting-client.py
import Pyro4

val = input("Brightness level? ").strip()

brightness_changer = Pyro4.Proxy("PYRONAME:change.brightness")    # use name server object lookup uri shortcut
print(brightness_changer.brightnessChanger(val))
