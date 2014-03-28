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

* In terminal, run "git clone https://github.com/danenb/audio_streaming"

* Navigate to folder using "cd audio_streaming"

* Execute install script by running "sudo bash ./install"

* Confirm installation and allow up to 30 minutes to download and configure all dependencies

* Customize hotspot SSID and WPA key using "sudo nano /etc/hostapd/hostapd.conf"
