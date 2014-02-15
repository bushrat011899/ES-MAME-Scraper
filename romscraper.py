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

parser          = argparse.ArgumentParser(description='Scrape rom info.',prog="romscraper")
parser.add_argument('rom', metavar='ROM', type=str, help='a rom file/folder (see -p)')
parser.add_argument('-o', '--output', type=str, help="output file (XML)", required=False, default="gamelist.xml")
parser.add_argument('-d', '--debug', action='store_true', help="print debug info", required=False)
parser.add_argument('-p', '--path', action='store_true', help="scrape info from a whole folder", required=False)
parser.add_argument('-i', '--image', action='store_true', help="retrieve images (when available)", required=False)
parser.add_argument('-s', '--imagepath', type=str, help="path to save images", required=False, default=os.getcwd()+"/images/")
args            = parser.parse_args()

whole_file      = args.rom
debug_mode      = args.debug
folder_mode     = args.path
image_mode		= args.image
output          = args.output
image_path		= args.imagepath

if not os.path.exists(image_path):
	os.makedirs(image_path)

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

def download_image(link, name, directory="", ext=None):
	ext = ext if ext else link[-4:]
	opener = urllib2.build_opener()
	page = opener.open(link)
	image = page.read()
	
	fout = open(directory+name+ext, "wb")
	fout.write(image)
	fout.close()

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
    path	    	= os.path.abspath(whole_file) + "/" + file 

    debug_print("Getting page...")
    debug_print("Path  : " + path)
    debug_print("File  : " + file)
    debug_print("ROM   : " + rom)
    
    if test_url('http://mamedb.com/game/'+ rom):
        req 		= urllib2.Request('http://mamedb.com/game/'+ rom)
        response 	= urllib2.urlopen(req)
        html 		= response.read()
    	skip 		= False
        response.close()
        debug_print('Downloaded Successfully')
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
	if image_mode and test_url("http://mamedb.com/marquees/" + rom + ".png"):
		download_image("http://mamedb.com/marquees/" + rom + ".png", rom, image_path)
		boxart	= image_path + rom + ".png"
		debug_print("Found Image")
	else:
		marquee	= None
		debug_print("No Image Found")
		
	### End
	skip_node = False
	for node in xml_root:
		for game_node in node:
			if game_node.text == name:
				skip_node = True
   
	if skip_node == False:
		print "\nFound		:	" + path
		print "Adding		:	" + name
		print "From Year	: 	" + year
		print "Made By		: 	" + manu
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
		if image_mode:
			xml_image		= et.SubElement(xml_game, "image")
			xml_image.text	= boxart
	else:
		print "Skipping " + rom

xml_tree        = et.ElementTree(xml_root)
xml_tree.write(output)

exit(0)
