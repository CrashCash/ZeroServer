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

### Installation
Set up a Raspberry Pi with built-in Bluetooth and WiFi (like a Raspberry Pi 3
Model B) and install Raspberry Pi OS Lite on it.

Pair the bike to the Raspberry Pi as described in the [ZeroBT Python
library](https://github.com/CrashCash/ZeroBT) README.

Install with:

```pip3 install https://github.com/CrashCash/ZeroServer/raw/master/dist/zeroserver-1.0.tar.gz```

This will install all the prerequisites, including my Bluetooth library and
the gunicorn server. I use gunicorn because it's a lot lighter than Apache.

Set up systemd with:

```wget -nd -N https://raw.githubusercontent.com/CrashCash/ZeroServer/master/gunicorn.service -P /etc/systemd/system```

Start web server with:

```systemctl enable --now gunicorn.service```

After this, it will be automatically started at boot time.

### Operational Notes

The motorcycle can handle only one Bluetooth connection at once, so there is a
zero_server.py script that runs as a daemon and serializes the communication
to the bike. It caches the socket and ensures it's properly closed.

### Example Code
These are similar to the examples from ZeroBT, except they use the
intermediate server instead of talking to the bike directly.

charging_status_server - Short sweet charging status script for the command line.

charging_data_server - Script that retrieves information as the bike is charging, and
outputs it in a CSV format suitable for a spreadsheet.
