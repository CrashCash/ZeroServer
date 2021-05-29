# ZeroServer
This is a small website using Flask to monitor a Zero electric motorcycle
while it's charging.

![Webpage](/charging.png?raw=true "Webpage")

## Why?
Because I wanted to monitor the charging remotely. The bike's Bluetooth range
is only about 20 feet maximum, so I put a Raspberry Pi on the wall of my
garage to talk to the bike and serve a web page I can view on my phone from
anywhere in the house.

It leverages my [ZeroBT Python library](https://github.com/CrashCash/ZeroBT)
which handles the Bluetooth protocol.

Note at the moment I'm trying to package this, so all the pieces are there,
but the glue is not.

### Installation
Set up a Raspberry Pi with built-in Bluetooth and WiFi (like a Raspberry Pi 3
Model B) and install Raspberry Pi OS Lite on it.

Install

```wget -nd https://raw.githubusercontent.com/CrashCash/ZeroServer/master/dist/zeroserver-1.0.0-py3-none-any.whl```

I use gunicorn because it's a lot lighter than Apache. Install gunicorn

Pair the bike to the Raspberry Pi as described in https://github.com/CrashCash/ZeroBT

```gunicorn "ZeroServer:create_app()"```

### More Example Code
These are like the examples from ZeroBT, except they use the intermediate
server instead of talking to the bike directly.

charging_status_server - Short sweet charging status script for the command line.

charging_data_server - Script that retrieves information as the bike is charging, and
outputs it in a CSV format suitable for a spreadsheet.
