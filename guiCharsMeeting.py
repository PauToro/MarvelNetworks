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

public_key = "b94a41b2612dd7f86517f823b4319417"
private_key = "8512a4a913969be34e3574573036c8648a8aa26b"

m = Marvel(public_key, private_key)

conn = sqlite3.connect('databases/MarvelNetworks')

char1 = raw_input("Character 1: ")
char2 = raw_input("Character 2: ")

char1Title = char1.title()
char2Title = char2.title()

#Get info and image for first character
cursor = conn.execute("SELECT ID FROM MarvelAPIChars where Name = ?", (char1Title,))

for row in cursor:
	char1ID = row[0]
	
character1 = m.get_character(char1ID).data.result

wikiURL1 = character1.wiki
charName1 = character1.name

name1, alias1, app1 = scrapWiki(wikiURL1)

conn = sqlite3.connect('databases/MarvelNetworks')

cursor = conn.execute("SELECT imageURL FROM MarvelAPIChars where ID = ?" , (char1ID,))

for row in cursor:
	imageURL1 = row[0]

name1Text = "Name: " + name1
alias1Text = "Aliases: " + alias1
fa1Text = "First Appearance: " + app1

#Get info and image for second character
cursor = conn.execute("SELECT ID FROM MarvelAPIChars where Name = ?", (char2Title,))

for row in cursor:
	char2ID = row[0]
	
character2 = m.get_character(char2ID).data.result

wikiURL2 = character2.wiki
charName2 = character2.name

name2, alias2, app2 = scrapWiki(wikiURL2)

cursor = conn.execute("SELECT imageURL FROM MarvelAPIChars where ID = ?" , (char2ID,))

for row in cursor:
	imageURL2 = row[0]

name2Text = "Name: " + name2
alias2Text = "Aliases: " + alias2
fa2Text = "First Appearance: " + app2

#Find common appearances between characters
cursor = conn.execute("SELECT DISTINCT iFN.FullName FROM heroes_in_comics AS hic1 INNER JOIN nameMatch AS nm1 ON hic1.Name = nm1.HICname INNER JOIN heroes_in_comics AS hic2 ON hic1.Issue = hic2.Issue INNER JOIN nameMatch AS nm2 ON hic2.Name = nm2.HICname INNER JOIN IssuesFullNames AS iFN ON hic1.Issue = iFN.FullKey WHERE nm1.APIname = ? AND nm2.APIname = ?" , (char1, char2))

issues = []

for row in cursor:
	issue = row[0]
	issueURL = issue.replace(".", "")
	issueURL = issue.replace("#", "")
	issueURL = issueURL.replace(" ", "_")
	issueURL = issueURL.title()
	issueURL = "http://marvel.wikia.com/wiki/" + issueURL
	issueYear = (scrapIssue(issueURL))
	if issueYear != "No record found." or issueYear is not None:
		issueYear = int(issueYear)
		issueTuple = (issue.title(), issueYear)
		issues.append(issueTuple)

conn.close()

sortedIssues = sorted(issues, key=getKey)

#Graphical interface

win = tk.Tk()
wbox = 255
hbox = 255

#Screen split into three

leftFrame = tk.Frame(win)
centerFrame = tk.Frame(win)
rightFrame = tk.Frame(win)

leftFrame.grid(column=0, row=0, sticky=NW)
centerFrame.grid(column=1, row=0)
rightFrame.grid(column=2, row=0, sticky=NE)

#Left frame is first character's image and information
charImage1 = createMainImage(imageURL1)

leftTitle = tk.Label(leftFrame, text=charName1, anchor=N, wraplength = wbox, font = ('Helvetica', 24), padx=5, pady=5)
leftCharImage = tk.Label(leftFrame, image=charImage1, anchor=N, width=wbox, height=hbox)

leftTitle.pack(fill=BOTH)
leftCharImage.pack(fill=BOTH)

leftNameLabel = tk.Label(leftFrame, text=name1Text, anchor=W, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)
leftAliasLabel = tk.Label(leftFrame, text=alias1Text, anchor=W, justify=LEFT, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)
leftFaLabel = tk.Label(leftFrame, text=fa1Text, anchor=W, justify=LEFT, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)

leftNameLabel.pack(fill=BOTH)
leftAliasLabel.pack(fill=BOTH)
leftFaLabel.pack(fill=BOTH)

#Right frame is second character's image and information
charImage2 = createMainImage(imageURL2)

rightTitle = tk.Label(rightFrame, text=charName2, anchor=N, wraplength = wbox, font = ('Helvetica', 24), padx=5, pady=5)
rightCharImage = tk.Label(rightFrame, image=charImage2, anchor=N, width=wbox, height=hbox)

rightTitle.pack(fill=BOTH)
rightCharImage.pack(fill=BOTH)

rightNameLabel = tk.Label(rightFrame, text=name2Text, anchor=W, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)
rightAliasLabel = tk.Label(rightFrame, text=alias2Text, anchor=W, justify=LEFT, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)
rightFaLabel = tk.Label(rightFrame, text=fa2Text, anchor=W, justify=LEFT, wraplength = wbox, font = ('Helvetica', 16), padx=5, pady=2)

rightNameLabel.pack(fill=BOTH)
rightAliasLabel.pack(fill=BOTH)
rightFaLabel.pack(fill=BOTH)

#Center frame holds common appearances
issuesScroll = Scrollbar(centerFrame)
issuesText = Text(centerFrame, height=10, width=60)
#height in lines, width in characters


issuesText.insert(END, "Common Appearances: \n")

for issue in sortedIssues:
	currentLine = '{0:<40}\t{1:4}'.format(issue[0], issue[1])
	issuesText.insert(END, currentLine + "\n")
	
issuesScroll.pack(side=RIGHT, fill=Y)
issuesText.pack(side=LEFT, fill=Y)
issuesScroll.config(command=issuesText.yview)
issuesText.config(yscrollcommand=issuesScroll.set, state=DISABLED)

win.mainloop()
