# ZeroServer
This is a small website using Flask to monitor a Zero electric motorcycle
while it's charging.

![Webpage](/charging.png?raw=true "Webpage")

## Why?
Because I wanted to monitor the charging remotely. The bike's Bluetooth range
is only about 20 feet maximum, so I put a Raspberry Pi on the wall of my
garage to talk to the bike and serve a web page I can view on my phone from
anywhere in the house.

It leverages my ZeroBT Python library which handles the Bluetooth protocol.

### Installation
Set up a Raspberry Pi with built-in Bluetooth and WiFi like a Raspberry Pi 3
Model B and install Raspberry Pi OS Lite on it.

Place zerobt.py somewhere on the Python path like
/usr/lib/python3/dist-packages (Debian/Raspberry Pi OS)

```wget -nd https://raw.githubusercontent.com/CrashCash/ZeroBT/master/zerobt.py -P /usr/lib/python3/dist-packages/```

Install

```wget -nd https://raw.githubusercontent.com/CrashCash/ZeroServer/master/zerobt.py -P /usr/lib/python3/dist-packages/```

In

Pair the bike to the Raspberry Pi as described in https://github.com/CrashCash/ZeroBT

### More Example Code
charging_data_server - Script that retrieves information as the bike is charging, and
outputs it in a CSV format suitable for a spreadsheet.

charging_status_server - Short sweet charging status script for the command line.



![Ride displayed in Google Earth](/screenshot-1.png?raw=true "Ride displayed in Google Earth")

![One point with data](/screenshot-2.png?raw=true "One point with data")
