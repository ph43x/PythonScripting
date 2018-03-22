# PythonScripting
--- Required Packages
sudo apt-get install python3 python3-pip Pyro4 gcc python3-dev build-essentials
mkdir ~/bin
cd ~/bin
wget https://pypi.python.org/packages/e2/58/6e1b775606da6439fa3fd1550e7f714ac62aa75e162eed29dbec684ecb3e/RPi.GPIO-0.6.3.tar.gz
tar -xvf RPi.GPIO-0.6.3.tar.gz
cd RPi.GPIO-0.6.3
sudo python3 setup.py install



--- Tidbits of information
Pyro4 does not handle relative paths very well. 
ex. "~/git/directory/file.txt" will throw an error, but "/home/user/git/directory/file.txt" will not.


