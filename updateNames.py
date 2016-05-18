from Tkinter import *
from PIL import Image, ImageTk
import Tkinter as tk
import sqlite3
from autocomplete import *
import io
from urllib import urlopen
from marvel.marvel import Marvel
from scrapperDef import scrapWiki, find_between
from bs4 import BeautifulSoup
import networkx as nx
from urllib2 import HTTPError
try:
    from urllib2 import urlopen, HTTPError
except ImportError:
    from urllib.request import urlopen

def getCharNamesForAutoComplete(list):
	conn = sqlite3.connect('databases/MarvelNetworks')
	cursor = conn.execute("SELECT APIname FROM nameMatch;")
	charNamesList = []
	for row in cursor:
		name = row[0]
		charNamesList.append(name)
	conn.close()
	return charNamesList
	
names = []
names = getCharNamesForAutoComplete(names)

for name in names:
	print name