# Key-locator
Locates key if it is already located

## Instalation
1. Clone the repository `git clone https://USERNAME@bitbucket.org/rneventteknik/key-locator.git`
2. Install pycurl `sudo apt-get install python-pycurl`
3. Configure Crowntab to run program at boot `crowntab -e`
4. Add the row to the file that opens `@reboot sudo python /home/pi/code/key-locator/KeyLocator.py >> /home/pi/code/key-locator/key.log 2>&1`
5. Reboot `sudo reboot`