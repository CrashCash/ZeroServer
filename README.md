# ZeroBT
This is a small website using Flask to monitor a Zero electric motorcycle
while it's charging.

## Why?
Because I wanted to monitor the charging remotely. The Bluetooth range is only
about 20 feet maximum, so I put a Raspberry Pi on the wall of my garage to
talk to the bike and serve a web page I can view on my phone from anywhere in
the house.

It leverages my ZeroBT Python library.

### Installation
Set up a Raspberry Pi with built-in Bluetooth and WiFi like a Raspberry Pi 3
Model B and install Raspberry Pi OS Lite on it.

Place zerobt.py somewhere on the Python path like
/usr/lib/python3/dist-packages (Debian/Raspberry Pi OS)

```wget -nd https://raw.githubusercontent.com/CrashCash/ZeroBT/master/zerobt.py -P /usr/lib/python3/dist-packages/```

Do the same with zero_server.py

```wget -nd https://raw.githubusercontent.com/CrashCash/ZeroBT/master/zerobt.py -P /usr/lib/python3/dist-packages/```

In

Pair the bike to the Raspberry Pi as described in https://github.com/CrashCash/ZeroBT

### More Example Code
charging_data - Script that retrieves information as the bike is charging, and
outputs it in a CSV format suitable for a spreadsheet.

charging_status - Short sweet charging status script for the command line.

record_ride - Record a ride with the Raspberry Pi in a saddlebag.

extract_ride - Extract data suitable for a spreadsheet from data file produced
by above.

extract_ride_text - Extract data as Python statements from data file produced
by above.

record_ride_gps - Record a ride with the Raspberry Pi and a GPS in a
saddlebag. You can use your phone as a GPS - read the script header for
details. The "ride_gps.dat" file is an example.

extract_ride_gps - Extract data suitable for Google Maps/Google Earth from
data file produced by above. The "ride_gps.kml" file is an example.

![Ride displayed in Google Earth](/screenshot-1.png?raw=true "Ride displayed in Google Earth")

![One point with data](/screenshot-2.png?raw=true "One point with data")
