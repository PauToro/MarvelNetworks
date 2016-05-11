#Single Character Class

from Tkinter import *
from PIL import Image, ImageTk
import io
from urllib import urlopen
import Tkinter as tk
import sqlite3
from marvel.marvel import Marvel
from scrapperDef import scrapWiki, find_between
from bs4 import BeautifulSoup
import networkx as nx
from urllib2 import HTTPError
try:
    from urllib2 import urlopen, HTTPError
except ImportError:
    from urllib.request import urlopen

#MarvelAPI keys
public_key = "b94a41b2612dd7f86517f823b4319417"
private_key = "8512a4a913969be34e3574573036c8648a8aa26b"
m = Marvel(public_key, private_key)

#Resize image function
def resize(width, height, wbox, hbox, pil_image):
	f1 = 1.0*wbox/width
	f2 = 1.0*hbox/height
	factor = min([f1, f2])
	width = int(width*factor)
	height = int(height*factor)
	return pil_image.resize((width, height), Image.ANTIALIAS)

#Image creation functions:
def createMainImage(url):
	wbox = 255
	hbox = 255
	image_bytes = urlopen(url).read()
	data_stream = io.BytesIO(image_bytes)
	pil_image = Image.open(data_stream)
	originalWidth, originalHeight = pil_image.size
	pil_image_resized = resize(originalWidth, originalHeight, wbox, hbox, pil_image)
	readyImage = ImageTk.PhotoImage(pil_image_resized)
	return readyImage	
	
def createEncounterImage(url):
	wbox = 75
	hbox = 75
	image_bytes = urlopen(url).read()
	data_stream = io.BytesIO(image_bytes)
	pil_image = Image.open(data_stream)
	originalWidth, originalHeight = pil_image.size
	pil_image_resized = resize(originalWidth, originalHeight, wbox, hbox, pil_image)
	readyImage = ImageTk.PhotoImage(pil_image_resized)
	return readyImage
	
class singleChar(object):	
	def __init__(self, singleCharName):
		self.name = singleCharName
		self.id = 0 #default
		self.mainImageURL = "" #default
		self.nameText = "" #default
		self.firstAppText = "" #default
		self.topEncounters = []
		self.encounterNames = []
		self.encounterImageURLs = []
		self.degreesText = 0 #default
		self.close_centralityText = 0 #default
		self.between_centralityText = 0 #default
				
	def getID(self):
		conn = sqlite3.connect('databases/MarvelNetworks')
		cursor = conn.execute("SELECT ID FROM MarvelAPIChars where Name = ?", (self.name,))
		for row in cursor:
			id = int(row[0])
		conn.close()
		self.id = id
		
	def getDataAPI(self):
		character = m.get_character(self.id).data.result
		wikiURL = character.wiki
		name, alias, app = scrapWiki(wikiURL)
		self.nameText = "Name: " + name
		self.firstAppText = "First Appearance: " + app
	
	def getMainImageURL(self):
		conn = sqlite3.connect('databases/MarvelNetworks')
		cursor = conn.execute("SELECT imageURL FROM MarvelAPIChars where ID = ?" , (self.id,))
		for row in cursor:
			self.mainImageURL = row[0]
		conn.close()

	def findTopEncounters(self):
		apiname = self.name.upper()
		conn = sqlite3.connect('databases/MarvelNetworks')
		cursor = conn.execute("SELECT DISTINCT nm2.APIname, COUNT(*) FROM heroes_in_comics AS hic1 INNER JOIN nameMatch AS nm1 ON hic1.Name = nm1.HICname INNER JOIN heroes_in_comics AS hic2 ON hic1.Issue = hic2.Issue INNER JOIN nameMatch AS nm2 ON hic2.Name = nm2.HICname WHERE nm1.APIname = ? GROUP BY nm2.APIname ORDER BY COUNT(*) DESC LIMIT 6" , (apiname,))
				
		for row in cursor:
			if row[0] != apiname:
				self.topEncounters.append(row[0])
		
		for encounter in self.topEncounters:
			encounter = encounter.title()
			cursor = conn.execute("SELECT ImageURL FROM MarvelAPIChars WHERE Name = ?" , (encounter,))
			for row in cursor:
				imgURL = row[0]
			self.encounterNames.append(encounter)
			self.encounterImageURLs.append(imgURL)
		conn.close()	
	
	def analyzeNetwork(self):
		G = nx.read_edgelist('networkMatch.csv', delimiter=';')
		character = self.name.upper()		
		self.degreesText = "Degrees: " + str(G.degree(character))
		close_cen = nx.closeness_centrality(G)
		bet_cen = nx.betweenness_centrality(G)
		for name, cc in close_cen.iteritems():
			if name == character:
				cc = '{0:.3f}'.format(cc)
				self.close_centralityText = "Closeness centrality: " + str(cc)
		for name, bc in bet_cen.iteritems():
			if name == character:
				bc = '{0:.3f}'.format(bc)
				self.between_centralityText = "Betweenness centrality: " + str(bc)
		
SW = singleChar("Banshee")
SW.getID()
SW.getDataAPI()
SW.getMainImageURL()
print SW.nameText
SW.findTopEncounters()
SW.analyzeNetwork()