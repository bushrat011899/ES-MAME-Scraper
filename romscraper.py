#!/usr/bin/python
import re
import urllib2
import sys
import os
from os import listdir
from os.path import isfile, join
import argparse
import requests
import elementtree.ElementTree as et
from requests.exceptions import HTTPError

has_elementtree = True
has_requests = True

parser          = argparse.ArgumentParser(description='Scrape rom info.',prog="romscraper")
parser.add_argument('rom', metavar='ROM', type=str, help='a rom file/folder (see -p)')
parser.add_argument('-o', '--output', type=str, help="output file (XML)", required=False, default="gamelist.xml")
parser.add_argument('-d', '--debug', action='store_true', help="print debug info", required=False)
parser.add_argument('-p', '--path', action='store_true', help="scrape info from a whole folder", required=False)
parser.add_argument('-i', '--image', action='store_true', help="retrieve images (when available)", required=False)
args            = parser.parse_args()

whole_file      = args.rom
debug_mode      = args.debug
folder_mode     = args.path
image_mode		= args.image
output          = args.output

def debug_print(string):
        if debug_mode:
                print string

def test_url(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
	except HTTPError:
		return False
	else:
		return True

debug_print(os.path.abspath(__file__))
debug_print(os.path.abspath(whole_file)) 

if folder_mode:
    files = [ f for f in listdir(whole_file) if isfile(join(whole_file,f)) ]
    debug_print("In Folder Mode")
else:
    files = [whole_file]
    debug_print("In File Mode")

xml_root        = et.Element("gameList")


for i in xrange(len(files)):
    path, file      = os.path.split(files[i])
    rom             = re.sub('\.[a-zA-Z0-9]*','',file)
    path	    = os.path.abspath(whole_file) + "/" + file 

    debug_print("Getting page...")
    debug_print("Path  : " + path)
    debug_print("File  : " + file)
    debug_print("ROM   : " + rom)
    
    if test_url('http://mamedb.com/game/'+ rom):
        req = urllib2.Request('http://mamedb.com/game/'+ rom)
        response = urllib2.urlopen(req)
        debug_print('Downloaded Successfully')
        html = response.read()
        response.close()
    	skip = False
    else:
    	debug_print('Download Failed')
    	skip = True	

    if skip == False:
        debug_print("Filtering Results...")
        results = re.search('(\<title\>Game\sDetails\:[\s]*)[a-zA-Z0-9\:\s\.-]*', html)

        if results:
                name = re.sub('(\<title\>Game\sDetails\:[\s]*)',"",results.group(0))
                debug_print("Found Name: " + name)
        else:
                debug_print("No Results Found")
        
	year_results = re.search("</b> <a href='/year/[0-9]*", html)
	
	if year_results:
		year = re.sub("</b> <a href='/year/", '', year_results.group(0))
		debug_print("Found Year: " + year)
	else:
		debug_print("No Results Found")

	manu_results = re.search('/manufacturer/[a-zA-Z]*', html)
	
	if manu_results:
		manu = re.sub('/manufacturer/', '', manu_results.group(0))
		debug_print("Found Manufacturer: " + manu)
	else:
		debug_print("No Results Found")
		
	### Experimental Image Getting Code Start
	if image_mode:
		if test_url("http://mamedb.com/snap/" + rom + ".png"):
			urllib.urlretrieve("http://mamedb.com/snap/" + rom + ".png",  "images/snap/"+ rom + "_snap" + ".png")
			snap	= "images/snap/"+ rom + "_snap" + ".png"
			debug_print("Found Snap Image")
		else:
			snap 	= None
			debug_print("No Snap Image Found")
	
		if test_url("http://mamedb.com/titles/" + rom + ".png"):
			urllib.urlretrieve("http://mamedb.com/titles/" + rom + ".png",  "images/title/"+ rom + "_title" + ".png")
			title	= "images/title/"+ rom + "_title" + ".png"
			debug_print("Found Title Image")
		else:
			title	= None
			debug_print("No Title Image Found")
	
		if test_url("http://mamedb.com/cabinets/" + rom + ".png"):
			urllib.urlretrieve("http://mamedb.com/cabinets/" + rom + ".png",  "images/cabinet/"+ rom + "_cabinet" + ".png")
			cabinet	= "images/cabinet/"+ rom + "_cabinet" + ".png"
			debug_print("Found Cabinet Image")
		else:
			cabinet	= None
			debug_print("No Cabinet Image Found")
		
		if test_url("http://mamedb.com/marquees/" + rom + ".png"):
			urllib.urlretrieve("http://mamedb.com/marquees/" + rom + ".png",  "images/marquee/"+ rom + "_marquee" + ".png")
			marquee	= "images/marquee/"+ rom + "_marquee" + ".png"
			debug_print("Found Marquee Image")
		else:
			marquee	= None
			debug_print("No Marquee Image Found")
	else:
		snap 	= None
		title	= None
		cabinet	= None
		marquee	= None
		
	### End
	skip_node = False
	for node in xml_root:
		for game_node in node:
			if game_node.text == name:
				skip_node = True
   
	if skip_node == False:
		print "Found " + path
		print "Adding " + name
		print "From Year:	" + year
		print "Made By:	" + manu
		debug_print("Done")

		xml_game        = et.SubElement(xml_root, "game")
		xml_path        = et.SubElement(xml_game, "path")
		xml_path.text   = path
		xml_name        = et.SubElement(xml_game, "name")
		xml_name.text   = name
		xml_year		= et.SubElement(xml_game, "year")
		xml_year.text	= year
		xml_manu		= et.SubElement(xml_game, "manufacturer")
		xml_manu.text	= manu
	else:
		print "Skipping " + rom

xml_tree        = et.ElementTree(xml_root)
xml_tree.write(output)

exit(0)
