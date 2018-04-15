# Ping Sweep

Ping Sweep is a fast subnet pinging tool. 

Currently Ping Sweep is only supported using Python 3 on Linux or OSX.

## Installation
Save the file, run the file.
python ping_sweep.py

## Getting Started
usage: ping_sweep.py [-h] [--hide] 1.2.3.4/24  OR 1.2.3.4/255.255.255.0

positional arguments:
  1.2.3.4/24  subnet in the form of ipaddress and netmask: 10.0.0.0/24 or 10.0.0.0/255.255.255.0

optional arguments:
  -h, --help  show this help message and exit
  --hide      hide hosts which are not reachable

## ToDo
- Add Windows Support
- Add sorting of the output (output can get out of order because of the multiprocessing)
