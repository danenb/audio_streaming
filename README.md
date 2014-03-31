audio_streaming
===============

Configures a Raspberry Pi to download mp3 media from a web server using a wifi dongle.



Features:
---------

* The unit becomes a wireless hotspot when it is unable to connect to a wireless network. Credentials for wireless networks can be uploaded to unit by connecting to hotspot with alternate device and browsing the address http://192.168.42.1

* The default hotspot is WPA encrypted, and has an SSID of "prototype" and WPA key of "prototype123"

* Media server URL can be set while in hotspot mode by browsing http://192.168.42.1/server

* Media plays, pauses, and resumes with momentary pull-down of GPIO pin 11 (board numbering)



Installation:
-------------

* Recommended on a fresh installation of Raspbian (http://www.raspberrypi.org/downloads)

* Ensure a steady internet connection
 
* Connect personal computer to raspberry pi through serial cable

* On host computer (USB side) run "USB-to-Serial Wifi Uitility.py" script from this repository (Requires python installation and PySerial module https://www.python.org/download/releases/2.7/ , https://pypi.python.org/pypi/pyserial)
  - Alternatively, access the Raspberry Pi command line directly through a telnet client such as Putty (see http://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable for tutorial on serial setup)
  - After logging into the raspberry pi through the command line, enter "sudo nano /etc/network/interfaces"
  - Edit the file to the following:

auto lo


iface lo inet loopback

iface eth0 inet dhcp


allow-hotplug wlan0

auto wlan0

iface wlan0 inet dhcp

  wpa-ssid "your network ssid"
  
  wpa-psk "your network passphrase"
  
  
  
  - Save the file by pressing ctrl+x, follow the prompts to save to current file
  - Reboot with "sudo reboot"

* Using SSH or serial connection into raspberry pi command line, run the following: 

  - "git clone https://github.com/danenb/audio_streaming"

  - Navigate to folder using "cd audio_streaming"

  - Execute install script by running "sudo bash ./install"

  - Confirm installation and allow up to 30 minutes to download and configure all dependencies (network internet connection must remain intact)

  - Customize hotspot SSID and WPA key using "sudo nano /etc/hostapd/hostapd.conf" (Defaults are ssid:prototype, key:prototype123)

  - Edit media server path: "sudo nano server" (can be hosted locally from a computer on the network, or from a remote website. Default is "http://thetinkerer.net/cgi-bin/)
  
  - Place "file_list.py" and "purge_files.py" from this repository into the media server directory set above. (The server must have python installed and configured to parse scripts with the ".py" extension)
  
  - Reboot the raspberry pi by entering "sudo reboot" in the command line.

* Upload or copy mp3 files into the media server directory

* The raspberry pi will check for and download mp3 files from the server every 5 minutes. The files will automatically be removed from the server after each successive download.

* If the raspberry pi is unable to connect to a network, it will initiate its own hotspot. To input new wifi credentials, connect to the hotspot from a wifi-capable device (SSID: prototype, key: prototype123), browse the address http://192.168.42.1, input new wifi credentials and press connect.

* If the hotspot appears on a device's network list but the device will not connect, restart (briefly unplug) the raspberry pi and allow up to two minutes for it to reboot before again connecting to the hotspot.
