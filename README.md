ES-MAME-Scraper
===============

ROM Info Scraper with XML output designed for EmulationStation on the Raspberry Pi

The only information grabbed at the moment is the proper name, but support for genres, year, manufacturer, etc. can be added at a later date. This information is gotten from MameDB.com, as it is a reliable source of information for MAME ROMs.

Installation
============

Download and install ElementTree from [Here](http://effbot.org/zone/element-index.htm)

Download and install Requests from [Here](https://pypi.python.org/pypi/requests)

As this is a single file Python script, there is no need to "install" it, just place it anywhere you see fit.


Usage
=====

Running the script directly is very simple:

```bash
python romscraper.py ROM [-p] [-d] [-h] [-o=<file>]
```

Where ROM is either a directory or file, specify using -p flag (-p for folder, leave out for file)
-d Is used to output debug info.

After the script is run it dumps the information into a XML file (gamelist.xml) in the same directory as the script that EmulationStation can use. 

Examples:

```bash
python romscraper.py 19xx.zip
>>>19XX: The War Against Destiny

python romscraper.py /roms/19xx.zip
>>>19XX: The War Against Destiny

python romscraper.py /roms/ -p
>>>19XX: The War Against Destiny
>>>Frogger
>>>Pac-Man

python romscraper.py 19xx.zip -o /roms/gamelist.xml
>>>19XX: The War Against Destiny
>>>gamelist.xml
```

Plans
=====

- [x] Make Repo
- [x] Get it Working
- [x] Add Year
- [x] Add Manufacturer
- [ ] Add Description
- [x] Specify Output File
