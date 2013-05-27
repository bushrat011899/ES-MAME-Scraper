import re
import urllib2
import sys
import os
from os import listdir
from os.path import isfile, join
import argparse

try:
    import elementtree.ElementTree as et
    has_elementtree = True
except ImportError:
    print "Warning: Module ElementTree is NOT Available"
    has_elementtree = False
try:
    import requests
    from requests.exceptions import HTTPError
    has_requests = True
except ImportError:
    print "Warning: Module Requests is NOT Available"
    has_requests = False

parser          = argparse.ArgumentParser(description='Scrape rom info.',prog="romscraper")
parser.add_argument('rom', metavar='ROM', type=str, help='a rom file/folder (see -p)')
parser.add_argument('-o', '--output', type=str, help="output file (XML)", required=False, default="gamelist.xml")
parser.add_argument('-d', '--debug', action='store_true', help="print debug info", required=False)
parser.add_argument('-p', '--path', action='store_true', help="scrape info from a whole folder", required=False)
args            = parser.parse_args()

whole_file      = args.rom
debug_mode      = args.debug
folder_mode     = args.path
output          = args.output

def debug_print(string):
        if debug_mode:
                print string

debug_print(os.path.abspath(__file__))
debug_print(os.path.abspath(whole_file)) 

if folder_mode:
    files = [ f for f in listdir(whole_file) if isfile(join(whole_file,f)) ]
    debug_print("In Folder Mode")
else:
    files = [whole_file]
    debug_print("In File Mode")

if has_elementtree:          
    xml_root        = et.Element("gameList")
else:
    debug_print("XML File Output Disabled")


for i in xrange(len(files)):
    path, file      = os.path.split(files[i])
    rom             = re.sub('\.[a-zA-Z0-9]*','',file)
    #debug_print(os.path.abspath(whole_file) + " + " + file)
    path	    = os.path.abspath(whole_file) + "/" + file 

    debug_print("Getting page...")
    debug_print("Path  : " + path)
    debug_print("File  : " + file)
    debug_print("ROM   : " + rom)

    if has_requests:
        debug_print("Has Requests.......")
        debug_print("Using Try/Except...")
        try:
            r = requests.get('http://mamedb.com/game/'+ rom)
            r.raise_for_status()
        except HTTPError:
            debug_print('Could not download page')
            skip = True
        else:
            req = urllib2.Request('http://mamedb.com/game/'+ rom)
            response = urllib2.urlopen(req)
            debug_print('Downloaded Successfully')
            html = response.read()
            response.close()
            skip = False
    else:
        debug_print("Does NOT Have Requests.....")
        debug_print("Going Straight to Urllib...")
        req = urllib2.Request('http://mamedb.com/game/'+ rom)
        response = urllib2.urlopen(req)
        debug_print('Downloaded Successfully')
        html = response.read()
        response.close()
        skip = False

    if skip == False:
        debug_print("Filtering Results...")
        results = re.search('(\<title\>Game\sDetails\:[\s]*)[a-zA-Z0-9\:\s\.-]*', html)

        if results:
                name = re.sub('(\<title\>Game\sDetails\:[\s]*)',"",results.group(0))
                debug_print("Found Name:")
        else:
                debug_print("No Results Found")
        if has_elementtree:
            skip_node = False
            for node in xml_root:
                for game_node in node:
                    if game_node.text == name:
                        skip_node = True
           
            if skip_node == False:
		print "Found " + path
                print "Adding " + name
                debug_print("Done")

                xml_game        = et.SubElement(xml_root, "game")
                xml_path        = et.SubElement(xml_game, "path")
                xml_path.text   = path
                xml_name        = et.SubElement(xml_game, "name")
                xml_name.text   = name
            else:
                print "Skipping " + rom
    else:
        print "Skipping " + rom

if has_elementtree:
    xml_tree        = et.ElementTree(xml_root)
    xml_tree.write(output)

exit(0)
