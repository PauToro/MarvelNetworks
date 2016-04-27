from Tkinter import *
from PIL import Image, ImageTk
import io
from urllib import urlopen
import Tkinter as tk
import sqlite3
from marvel.marvel import Marvel
from scrapperDef import scrapWiki, find_between
from bs4 import BeautifulSoup
from urllib2 import HTTPError
try:
    from urllib2 import urlopen, HTTPError
except ImportError:
    from urllib.request import urlopen

def find_between(aString, first, last):
	try:
		start = aString.index(first) + len(first)
		end = aString.index(last, start)
		return aString[start:end]
	except ValueError:
		return ""

def scrapIssue(issueURL):
	try:		
		soup = BeautifulSoup(urlopen(issueURL))
		lines = soup.find_all('a')
		months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		i = 0
		for line in lines:
			i += 1
			for month in months:
				if month in line:
					lineYear = lines[i].encode('utf-8')
					global year
					year = find_between(lineYear, ">", "<")
		return year
	except HTTPError:
		return "No record found."

#For sorting issue tuples
def getKey(item):
	return item[1]

def resize(width, height, wbox, hbox, pil_image):
	f1 = 1.0*wbox/width
	f2 = 1.0*hbox/height
	factor = min([f1, f2])
	width = int(width*factor)
	height = int(height*factor)
	return pil_image.resize((width, height), Image.ANTIALIAS)

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

public_key = "b94a41b2612dd7f86517f823b4319417"
private_key = "8512a4a913969be34e3574573036c8648a8aa26b"

m = Marvel(public_key, private_key)

id = input("Enter ID: ")

id = int(id)

character = m.get_character(id).data.result

wikiURL = character.wiki
charName = character.name

name, alias, app = scrapWiki(wikiURL)

conn = sqlite3.connect('databases/MarvelNetworks')

cursor = conn.execute("SELECT imageURL FROM MarvelAPIChars where ID = ?" , (id,))

for row in cursor:
	mainURL = row[0]

conn.close()

nameText = "Name: " + name
aliasText = "Aliases: " + alias
faText = "First Appearance: " + app

apiname = character.name.upper()

conn = sqlite3.connect('databases/MarvelNetworks')

cursor = conn.execute("SELECT DISTINCT nm2.APIname, COUNT(*) FROM heroes_in_comics AS hic1 INNER JOIN nameMatch AS nm1 ON hic1.Name = nm1.HICname INNER JOIN heroes_in_comics AS hic2 ON hic1.Issue = hic2.Issue INNER JOIN nameMatch AS nm2 ON hic2.Name = nm2.HICname WHERE nm1.APIname = ? GROUP BY nm2.APIname ORDER BY COUNT(*) DESC LIMIT 6" , (apiname,))

topEncounters = []
encounterNames = []
encounterImages = []

for row in cursor:
	if row[0] != apiname:
		topEncounters.append(row[0])
		
for encounter in topEncounters:
	encounter = encounter.title()
	cursor = conn.execute("SELECT ImageURL FROM MarvelAPIChars WHERE Name = ?" , (encounter,))
	for row in cursor:
		img = row[0]
	encounterNames.append(encounter)
	encounterImages.append(img)
	
conn.close()
win = tk.Tk()

wbox = 255
hbox = 255

mainImage = createMainImage(mainURL)

#Screen has two containers
leftFrame = tk.Frame(win)
rightFrame = tk.Frame(win)
leftFrame.grid(row=0,column=0)
rightFrame.grid(row=0, column=1)

#Everything in left frame
title = tk.Label(leftFrame, text=charName, anchor=W, wraplength = wbox, font = ('Helvetica', 24), padx=5, pady=5)
charImage = tk.Label(leftFrame, image=mainImage, width=wbox, height=hbox)

title.pack(fill=X)
charImage.pack(fill=X)

nameLabel = tk.Label(leftFrame, text=nameText, anchor=W, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)
aliasLabel = tk.Label(leftFrame, text=aliasText, anchor=W, justify=LEFT, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)
faLabel = tk.Label(leftFrame, text=faText, anchor=W, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)

nameLabel.pack(fill=X)
aliasLabel.pack(fill=X)
faLabel.pack(fill=X)

#Everything in right frame
encounterFrame = tk.Frame(rightFrame)
encounterTitle = tk.Label(encounterFrame, text="Top 5 Encounters", anchor=W, font = ('Helvetica', 16), padx=5, pady=2)
encounterFrame.pack()
encounterTitle.pack(fill=X)

#Images of top 5 characters
enCharFrame = tk.Frame(encounterFrame)
enCharFrame.pack(fill=X)

eimg1 = createEncounterImage(encounterImages[0])
encounterImage1 = tk.Label(enCharFrame, image=eimg1)
encounterName1 = tk.Label(enCharFrame, text=encounterNames[0])

eimg2 = createEncounterImage(encounterImages[1])
encounterImage2 = tk.Label(enCharFrame, image=eimg2)
encounterName2 = tk.Label(enCharFrame, text=encounterNames[1])

eimg3 = createEncounterImage(encounterImages[2])
encounterImage3 = tk.Label(enCharFrame, image=eimg3)
encounterName3 = tk.Label(enCharFrame, text=encounterNames[2])

eimg4 = createEncounterImage(encounterImages[3])
encounterImage4 = tk.Label(enCharFrame, image=eimg4)
encounterName4 = tk.Label(enCharFrame, text=encounterNames[3])

eimg5 = createEncounterImage(encounterImages[4])
encounterImage5 = tk.Label(enCharFrame, image=eimg5)
encounterName5 = tk.Label(enCharFrame, text=encounterNames[4])

encounterImage1.grid(row=0, column=0)
encounterImage2.grid(row=0, column=1)
encounterImage3.grid(row=0, column=2)
encounterImage4.grid(row=0, column=3)
encounterImage5.grid(row=0, column=4)
encounterName1.grid(row=1, column=0)
encounterName2.grid(row=1, column=1)
encounterName3.grid(row=1, column=2)
encounterName4.grid(row=1, column=3)
encounterName5.grid(row=1, column=4)

win.mainloop()





