from Tkinter import *
from PIL import Image, ImageTk
import Tkinter as tk
import sqlite3
from autocomplete import *

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

class Marvelist:
    def __init__(self, master):
        self.master = master

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        startScreenFrame = startScreen(container, self)
        startScreenFrame.tkraise()
        
class startScreen(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.configure(background="red4")
		graphicHeight = 255
		graphicWidth = 400
		singleGraphic = PhotoImage(file="single.gif")
		doubleGraphic = PhotoImage(file="double.gif")
	
	def char1Display():
		prompt1 = Label(char1Frame, text="Character name:")
		prompt1.pack()
		singleCharEntry = AutocompleteEntry(char1Frame, bd=5)
		singleCharEntry.set_completion_list(charNamesList)
		singleCharEntry.pack()
		singleCharEntry.focus_set()
	
		subtmitSingle = Button(char1Frame, text="Enter", command=getSingleChar())

	def getSingleChar():
		singleCharName = singleCharEntry.get()
	
	def char2Display():
		prompt2 = Label(char2Frame, text="Character names:")
		prompt2.pack()
		doubleCharEntry1 = AutocompleteEntry(char2Frame, bd=5)
		doubleCharEntry2 = AutocompleteEntry(char2Frame, bd=5)
		doubleCharEntry1.pack()
		doubleCharEntry2.pack()
	
		subtmitSingle = Button(char1Frame, text="Enter", command=getDoubleChar)

	def getDoubleChar():
		doubleCharName1 = doubleCharEntry1.get()
		doubleCharName2 = doubleCharEntry2.get()

	#title frame
	titleFrame = tk.Frame(self)
	titleFrame.pack(pady=(5,50))
	title = tk.Label(titleFrame, text="MARVELIST", font = ('Helvetica', 40), borderwidth=0)
	title.pack()

	#options frame
	optionsFrame = tk.Frame(self)
	optionsFrame.pack(fill=X)
	optionsFrame.configure(background="red4")

	#single character frame
	char1Frame = tk.Frame(optionsFrame)
	char1Frame.pack(side=LEFT, padx=(10,40))
	char1Text = tk.Button(char1Frame, text="View Individual Character's\n Network", height=2, wraplength=graphicWidth, font = ('Helvetica', 20), command=char1Display, highlightthickness=0,bd=0)
	char1Text.pack()
	char1Image = Label(char1Frame, image=singleGraphic)
	char1Image.pack()

	#double character frame
	char2Frame = tk.Frame(optionsFrame)
	char2Frame.pack(side=LEFT, padx=(40,10))
	char2Text = tk.Button(char2Frame, text="Find Common Appearances\n Between Two Characters", height=2, wraplength=graphicWidth, font = ('Helvetica', 20), command=char2Display)
	char2Text.pack()
	char2Image = Label(char2Frame, image=doubleGraphic, padx=5, pady=5)
	char2Image.pack()
	
root = tk.Tk()	
startScreenTest = Marvelist(root)
root.mainloop()