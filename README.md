ES-MAME-Scraper
===============

ROM Info Scraper with XML output designed for EmulationStation on the Raspberry Pi

Installation
============

Download and install ElementTree from [Here](http://effbot.org/zone/element-index.htm)

Download and install Requests from [Here](https://pypi.python.org/pypi/requests)


Usage
=====

Running the script directly is very simple:

```
python romscraper.py [-p] [-d] [-h] ROM
```

Where ROM is either a directory or file, specify using -p flag (-p for folder, leave out for file)
-d Is used to output debug info.

Examples:

```
python romscraper 19xx.zip

python romscraper /roms/19xx.zip

python romscraper /roms/ -p
```

