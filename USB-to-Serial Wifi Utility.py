# -*- coding: utf-8 -*-
import sys
import serial
import time
import os

#### Parameters ####
##username = 'pi'
##password = 'raspberry'
##hostname = 'raspberrypi'
#### Parameters ####
#clear_all = True



def serial_ports():
    """
    Returns a generator for all available serial ports
    """
    if os.name == 'nt':
        # windows
        for i in range(256):
            try:
                s = serial.Serial(i)
                s.close()
                yield 'COM' + str(i + 1)
            except serial.SerialException:
                pass
    else:
        # unix
        for port in serial.tools.list_ports.comports():
            yield port[0]


def port_check(username, hostname, ports = (list(serial_ports()))):
    'Find the port connected to the raspberry pi'
    global COM

    print ports  #debugging

    for i in range(len(ports)):
        try:
            COM = serial.Serial(port=ports[i],baudrate=115200,timeout=.5)

            COM.write('\n')
            time.sleep(.5)
            output = COM.read(1024)
            print output  #debugging

            if output.find('login:') > 0:
                print 'success on port ', ports[i]  #debugging
                return False
            elif output.find(username+'@'+hostname) > 0:
                print 'logged in on port ', ports[i]
                return True
            else:
                print 'unsuccessful on port', ports[i]  #debugging
        except serial.SerialException:
            print 'An exception occured'
            pass
    return None


def sign_in(username, password, hostname):
    'send login data'
    global COM

    COM.write(username+'\n')
    time.sleep(.2)
    output = COM.read(1024)
    if output.find('Password:') < 0:
        print 'Invalid username'
    COM.write(password+'\n')
    time.sleep(2)
    output = COM.read(1024)
    if output.find(username+'@'+hostname) < 0:
        time.sleep(.5)
        if output.find(username+'@'+hostname) < 0:
            print 'Invalid password'
    print output  #debugging


def check_status(check_string,error,duration=.1,print_output=False):
    global COM
    output = ''
    cycles = int(10*duration)

    for i in range (cycles):
        output = output + COM.read(1024)
        if output.find(check_string) > 0 or print_output==True:
            print output
            return
        time.sleep(.1)
    print '\n\n\nAn error occured while',error,'\n\n\n\n'
    


def create_interfaces(username,hostname,ssid,psk):
    'Write/replace Rpi interfaces file'
    global COM
    ssid = "'"+ssid+"'"
    psk = "'"+psk+"'"

    #Write interface file
    COM.write('cd ~\n')
    COM.write('echo "auto lo" > temp\n')
    COM.write('echo "" >> temp\n')
    check_status(username+'@'+hostname, 'writing to temp file')
    COM.write('echo "iface lo inet loopback" >> temp\n')
    check_status(username+'@'+hostname, 'writing to temp file')
    COM.write('echo "iface eth0 inet dhcp" >> temp\n')
    COM.write('echo "" >> temp\n')
    check_status(username+'@'+hostname, 'writing to temp file')
    COM.write('echo "allow-hotplug wlan0" >> temp\n')
    check_status(username+'@'+hostname, 'writing to temp file')
    COM.write('echo "iface wlan0 inet dhcp" >> temp\n')
    check_status(username+'@'+hostname, 'writing to temp file')
    COM.write("echo wpa-ssid '"+ssid+"' >> temp\n")
    check_status(username+'@'+hostname, 'writing to temp file')
    COM.write("echo wpa-psk '"+psk+"' >> temp\n")
    check_status(username+'@'+hostname, 'writing to temp file')
    
    COM.write('sudo cp temp /etc/network/interfaces.wifi\n')
    time.sleep(.1)
    COM.write('sudo mv temp /etc/network/interfaces\n')
    time.sleep(.1)
    check_status(username+'@'+hostname, 'moving interfaces file')

    COM.write('sudo ifdown wlan0\n')
    check_status(username+'@'+hostname, 'stopping wireless services',20)
    print '\n\nRestarting wireless services\n\n'
    COM.write('sudo ifup wlan0\n')
    time.sleep(20)
    check_status(username+'@'+hostname, 'restarting wireless services',60,True)
    print 'You can now connect to the device through SSH using the above \
IP address, or through a serial connection with the following parameters: \
115200 baud rate, 8 data bits, 1 stop bit, no parity, no hardware control.\n \
The default username is "pi" and password "raspberry".'

    

def main(hostname, username, password, ssid, psk):
    logged_in = port_check(username,hostname)

    if logged_in == None:
        print 'Failed to connect to Raspberry Pi'
        print 'Please check your cable connection'
        time.sleep(5)
        exit()

    elif logged_in == False:
        sign_in(username,password,hostname)

    create_interfaces(username,hostname,ssid,psk)


    
from Tkinter import *
import tkMessageBox
import Tkinter

def buttonPress(hostname, username, password, ssid, psk):
    global window
    window.quit()
    main(hostname, username, password, ssid, psk)
    os.system('pause')


# GUI setup
window = Tkinter.Tk()
ssid = StringVar()
psk = StringVar()
hostname = StringVar()
username = StringVar()
password = StringVar()

hostname_label = Label(window, text='Device Name:')
hostname_entry = Entry(window, textvariable=hostname)

username_label = Label(window, text='Username:')
username_entry = Entry(window, textvariable=username)

password_label = Label(window, text='Password:')
password_entry = Entry(window, textvariable=password)

ssid_label = Label(window, text='Network Name (SSID):')
ssid_entry = Entry(window, textvariable=ssid)

psk_label = Label(window, text='Network Password (PSK):')
psk_entry = Entry(window, textvariable=psk)

spacer = Label(window, text=' ')

button = Button(window, text='Upload', command=lambda: buttonPress(hostname.get(),username.get(),password.get(),ssid.get(),psk.get()))

hostname_label.grid(row=0,column=2,padx=10,pady=5)
hostname_entry.grid(row=0,column=3,padx=10,pady=5)
hostname_entry.insert(0,'prototype')

username_label.grid(row=1,column=2,padx=10,pady=5)
username_entry.grid(row=1,column=3,padx=10,pady=5)
username_entry.insert(0,'pi')

password_label.grid(row=2,column=2,padx=10,pady=5)
password_entry.grid(row=2,column=3,padx=10,pady=5)
password_entry.insert(0,'raspberry')

spacer.grid(row=3, column=2,pady=10)

ssid_label.grid(row=5,column=2,padx=10,pady=5)
ssid_entry.grid(row=5,column=3,padx=10,pady=5)
psk_label.grid(row=6,column=2,padx=10,pady=5)
psk_entry.grid(row=6,column=3,padx=10,pady=5)
button.grid(row=7,column=0,columnspan=4,padx=10,pady=5)
window.title('Wireless Network Setup')
window.mainloop()
