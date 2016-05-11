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
	
def raise_frame(frameToRaise, frameToForget):
	frameToRaise.tkraise()
	frameToForget.grid_forget()
	 		
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

#	
def createSingleCharPage(characterName):
	currentChar = singleChar(characterName.title())
	currentChar.getID()
	#print currentChar.id
	currentChar.getDataAPI()
	#print currentChar.nameText
	#print currentChar.firstAppText
	currentChar.getMainImageURL()
	currentChar.findTopEncounters()
	currentChar.analyzeNetwork()
	#print currentChar.degreesText
	#print currentChar.close_centralityText
	#print currentChar.between_centralityText
	singleCharWin = Toplevel()
	currentCharFrame = singleCharScreen(singleCharWin, currentChar)
	currentCharFrame.grid(row=0, column=0, sticky="nsew")
	
#def printName(charName):
#	print "From global function: " + charName
	
class Marvelist(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
    
        startScreenFrame = startScreen(container, self)
        startScreenFrame.grid(row=0, column=0, sticky="nsew")
        
        startScreenFrame.tkraise()
        
    #def createSingleCharPage(characterName):
		#self.currentChar = singleChar(characterName)
		#self.currentCharScreen = singleCharScreen(self.container, self.currentChar, self)
		#self.currentCharScreen.grid(row=0, column=0, sticky="nsew")
		#self.currentCharScreen.tkraise()
        
class startScreen(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.configure(background="red4")
		graphicHeight = 255
		graphicWidth = 400 
		self.singleGraphic = PhotoImage(file="single.gif")
		self.doubleGraphic = PhotoImage(file="double.gif")
		self.singleCharName = ""
		
		#title frame
		self.titleFrame = tk.Frame(self)
		self.titleFrame.pack(pady=(5,50))
		self.title = tk.Label(self.titleFrame, text="MARVELIST", font = ('Helvetica', 40), borderwidth=0)
		self.title.pack()

		#options frame
		self.optionsFrame = tk.Frame(self)
		self.optionsFrame.pack(fill=X)
		self.optionsFrame.configure(background="red4")

		#single character frame
		self.char1Frame = tk.Frame(self.optionsFrame)
		self.char1Frame.pack(side=LEFT, padx=(10,40))
		self.char1Text = tk.Button(self.char1Frame, text="View Individual Character's\n Network", height=2, relief = "flat", wraplength=graphicWidth, font = ('Helvetica', 20), command=self.char1Display, highlightthickness=0,bd=0)
		self.char1Text.pack()
		self.singleGraphic = PhotoImage(file="single.gif")
		self.char1Image = Label(self.char1Frame, image = self.singleGraphic)
		self.char1Image.pack()

		#double character frame
		self.char2Frame = tk.Frame(self.optionsFrame)
		self.char2Frame.pack(side=LEFT, padx=(40,10))
		self.char2Text = tk.Button(self.char2Frame, text="Find Common Appearances\n Between Two Characters", height=2, relief="flat", wraplength=graphicWidth, font = ('Helvetica', 20), command=self.char2Display)
		self.char2Text.pack()
		self.doubleGraphic = PhotoImage(file="double.gif")
		self.char2Image = Label(self.char2Frame, image = self.doubleGraphic, padx=5, pady=5)
		self.char2Image.pack()

	def char1Display(self):
		self.prompt1 = Label(self.char1Frame, text="Character name:")
		self.prompt1.pack()
		self.singleCharEntry = AutocompleteEntry(self.char1Frame, bd=5)
		self.singleCharEntry.set_completion_list(namesList)
		self.singleCharEntry.pack()
		self.singleCharEntry.focus_set()
	
		self.submitSingle = Button(self.char1Frame, text="Enter", command=self.getSingleChar)
		self.submitSingle.pack()
	
	def getSingleChar(self):
		self.singleCharName = self.singleCharEntry.get()
		print self.singleCharName
		self.readySingle = Button(self.char1Frame, text="Ready", command=lambda: createSingleCharPage(self.singleCharName))		
		self.readySingle.pack()
		
	def char2Display(self):
		self.prompt2 = Label(self.char2Frame, text="Character names:")
		self.prompt2.pack()
		self.doubleCharEntry1 = AutocompleteEntry(self.char2Frame, bd=5)
		self.doubleCharEntry2 = AutocompleteEntry(self.char2Frame, bd=5)
		self.doubleCharEntry1.set_completion_list(namesList)
		self.doubleCharEntry2.set_completion_list(namesList)
		self.doubleCharEntry1.pack()
		self.doubleCharEntry2.pack()
		self.doubleCharEntry1.focus_set()
		self.doubleCharEntry2.focus_set()
	
		self.submitDouble = Button(self.char2Frame, text="Enter", command=self.getDoubleChar)
		self.submitDouble.pack()
		
		#self.goToDouble = Button(self.char2Frame, text="Ready", command=raise_frame(

	def getDoubleChar(self):
		self.doubleCharName1 = self.doubleCharEntry1.get()
		self.doubleCharName2 = self.doubleCharEntry2.get()
		#print self.doubleCharName1
		#print self.doubleCharName2
		
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
		self.degreesText = "" #default
		self.close_centralityText = "" #default
		self.between_centralityText = "" #default
				
	def getID(self):
		conn = sqlite3.connect('databases/MarvelNetworks')
		cursor = conn.execute("SELECT ID FROM MarvelAPIChars where Name = ?", (self.name,))
		for row in cursor:
			id = int(row[0])
		conn.close()
		self.id = id
		
	def getDataAPI(self):
		wikiID = self.id
		character = m.get_character(wikiID).data.result
		wikiURL = character.wiki
		#print wikiURL
		name, alias, app = scrapWiki(wikiURL)
		#print name
		#print app
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
				
class singleCharScreen(tk.Frame, singleChar):
	def __init__(self, parent, singleChar):
		tk.Frame.__init__(self, parent)
		#self.controller = controller
		self.configure(background="red4")
		wbox = 255
		hbox = 255

		self.mainImage = createMainImage(singleChar.mainImageURL)

		#Screen has two containers
		self.leftFrame = tk.Frame(self)
		self.rightFrame = tk.Frame(self)
		self.leftFrame.grid(row=0,column=0)
		self.rightFrame.grid(row=0, column=1)

		#Everything in left frame
		self.title = tk.Label(self.leftFrame, text=singleChar.name, anchor=W, wraplength = wbox, font = ('Helvetica', 24), padx=5, pady=5)
		self.charImage = tk.Label(self.leftFrame, image=self.mainImage, width=wbox, height=hbox)

		self.title.pack(fill=X)
		self.charImage.pack(fill=X)

		self.nameLabel = tk.Label(self.leftFrame, text=singleChar.nameText, anchor=W, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)
		self.faLabel = tk.Label(self.leftFrame, text=singleChar.firstAppText, anchor=W, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)

		self.nameLabel.pack(fill=X)
		self.faLabel.pack(fill=X)

		#Everything in right frame
		self.encounterFrame = tk.Frame(self.rightFrame)
		self.encounterTitle = tk.Label(self.encounterFrame, text="Top 5 Encounters", anchor=W, font = ('Helvetica', 16), padx=5, pady=2)
		self.encounterFrame.pack()
		self.encounterTitle.pack(fill=X)

		#Images of top 5 characters
		self.enCharFrame = tk.Frame(self.encounterFrame)
		self.enCharFrame.pack(fill=X)

		self.eimg1 = createEncounterImage(singleChar.encounterImageURLs[0])
		self.encounterImage1 = tk.Label(self.enCharFrame, image=self.eimg1)
		self.encounterName1 = tk.Label(self.enCharFrame, text=singleChar.encounterNames[0])

		self.eimg2 = createEncounterImage(singleChar.encounterImageURLs[1])
		self.encounterImage2 = tk.Label(self.enCharFrame, image=self.eimg2)
		self.encounterName2 = tk.Label(self.enCharFrame, text=singleChar.encounterNames[1])
		
		self.eimg3 = createEncounterImage(singleChar.encounterImageURLs[2])
		self.encounterImage3 = tk.Label(self.enCharFrame, image=self.eimg3)
		self.encounterName3 = tk.Label(self.enCharFrame, text=singleChar.encounterNames[2])

		self.eimg4 = createEncounterImage(singleChar.encounterImageURLs[3])
		self.encounterImage4 = tk.Label(self.enCharFrame, image=self.eimg4)
		self.encounterName4 = tk.Label(self.enCharFrame, text=singleChar.encounterNames[3])

		self.eimg5 = createEncounterImage(singleChar.encounterImageURLs[4])
		self.encounterImage5 = tk.Label(self.enCharFrame, image=self.eimg5)
		self.encounterName5 = tk.Label(self.enCharFrame, text=singleChar.encounterNames[4])
		
		self.encounterImage1.grid(row=0, column=0)
		self.encounterImage2.grid(row=0, column=1)
		self.encounterImage3.grid(row=0, column=2)
		self.encounterImage4.grid(row=0, column=3)
		self.encounterImage5.grid(row=0, column=4)
		self.encounterName1.grid(row=1, column=0)
		self.encounterName2.grid(row=1, column=1)
		self.encounterName3.grid(row=1, column=2)
		self.encounterName4.grid(row=1, column=3)
		self.encounterName5.grid(row=1, column=4)		
		
		#Network information
		self.networkFrame = tk.Frame(self.rightFrame)
		self.networkTitle = Label(self.networkFrame, text = "Network Statistics", anchor=W, font = ('Helvetica', 16), padx=5, pady=2)
		self.networkFrame.pack(fill=X, pady=10)
		self.networkTitle.pack(fill=X)
		
		self.degreesFrame = tk.Frame(self.networkFrame)
		self.degreesText = Label(self.degreesFrame, text = singleChar.degreesText, anchor=W, font = ('Helvetica', 12), padx=2, pady=2)
		self.degreesFrame.pack(fill=X)
		self.degreesText.pack(fill=X)
		
		self.closeFrame = tk.Frame(self.networkFrame)
		self.closeText = Label(self.closeFrame, text = singleChar.close_centralityText, anchor=W, font = ('Helvetica', 12), padx=2, pady=2)
		self.closeFrame.pack(fill=X)
		self.closeText.pack(fill=X)
		
		self.betweenFrame = tk.Frame(self.networkFrame)
		self.betweenText = Label(self.betweenFrame, text = singleChar.between_centralityText, anchor=W, font = ('Helvetica', 12), padx=2, pady=2)
		self.betweenFrame.pack(fill=X)
		self.betweenText.pack(fill=X)


namesList = []
namesList = getCharNamesForAutoComplete(namesList)

program = Marvelist()
#startScreenFrame = startScreen(root)
#startScreenFrame.pack()
program.mainloop()