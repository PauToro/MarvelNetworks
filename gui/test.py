from Tkinter import *
from PIL import Image, ImageTk
import io
from urllib import urlopen
import Tkinter as tk
import sqlite3
from marvel.marvel import Marvel
from scrapperDef import scrapWiki, find_between

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

print charName
print imageurl 
print "Name: " + name
print "Alias: " + alias
print "First Appearance: " + app

apiname = character.name.upper()

conn = sqlite3.connect('databases/MarvelNetworks')

cursor = conn.execute("SELECT DISTINCT nm2.APIname, COUNT(*) FROM heroes_in_comics AS hic1 INNER JOIN nameMatch AS nm1 ON hic1.Name = nm1.HICname INNER JOIN heroes_in_comics AS hic2 ON hic1.Issue = hic2.Issue INNER JOIN nameMatch AS nm2 ON hic2.Name = nm2.HICname WHERE nm1.APIname = ? GROUP BY nm2.APIname ORDER BY COUNT(*) DESC LIMIT 6" , (apiname,))

topEncounters = []

for row in cursor:
	if row[0] != apiname:
		topEncounters.append(row[0])
		
print "Top 5 Encounters:"
for encounter in topEncounters:
	encounter = encounter.title()
	cursor = conn.execute("SELECT ImageURL FROM MarvelAPIChars WHERE Name = ?" , (encounter,))
	for row in cursor:
		img = row[0]
	print encounter
	print img
	
conn.close()
win = tk.Tk()

wbox = 255
hbox = 255

mainImage = createMainImage(mainURL)

leftFrame = Frame(win)
rightFrame = Frame(win)
leftFrame.grid(row=0,column=0)
rightFrame.grid(row=0, column=1)

title = tk.Label(leftFrame, text="Magneto", font = ('Helvetica', 24), padx=5, pady=5)
charImage = tk.Label(leftFrame, image=mainImage, width=wbox, height=hbox)

#title.grid(row=0, column=0)
#charImage.grid(row=1, column=0)

title.pack()
charImage.pack()

win.mainloop()





