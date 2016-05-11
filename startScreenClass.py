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
	
#class Marvelist(tk.Frame):
#    def __init__(self, master):
#        self.master = master
#        tk.Frame.__init__(self, master)
#        container = tk.Frame(self.master)
#        container.pack(side="top", fill="both", expand=True)
#        container.grid_rowconfigure(0, weight=1)
#        container.grid_columnconfigure(0, weight=1)
#        startScreenFrame = startScreen(container, self.master)
#        startScreenFrame.tkraise()
        
class startScreen(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
#		self.controller = controller
		self.configure(background="red4")
		graphicHeight = 255
		graphicWidth = 400
		#singleGraphic = PhotoImage(file="single.gif")
		#doubleGraphic = PhotoImage(file="double.gif")
		
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
		self.char1Text = tk.Button(self.char1Frame, text="View Individual Character's\n Network", height=2, wraplength=graphicWidth, font = ('Helvetica', 20), command=self.char1Display, highlightthickness=0,bd=0)
		self.char1Text.pack()
		self.char1Image = Label(self.char1Frame, image=singleGraphic)
		self.char1Image.pack()

		#double character frame
		self.char2Frame = tk.Frame(self.optionsFrame)
		self.char2Frame.pack(side=LEFT, padx=(40,10))
		self.char2Text = tk.Button(self.char2Frame, text="Find Common Appearances\n Between Two Characters", height=2, wraplength=graphicWidth, font = ('Helvetica', 20), command=self.char2Display)
		self.char2Text.pack()
		self.char2Image = Label(self.char2Frame, image=doubleGraphic, padx=5, pady=5)
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

	def getDoubleChar(self):
		self.doubleCharName1 = self.doubleCharEntry1.get()
		self.doubleCharName2 = self.doubleCharEntry2.get()
		print self.doubleCharName1
		print self.doubleCharName2

namesList = []
namesList = getCharNamesForAutoComplete(namesList)

root = tk.Tk()
singleGraphic = PhotoImage(file="single.gif")
doubleGraphic = PhotoImage(file="double.gif")
startScreenFrame = startScreen(root)
startScreenFrame.pack()
root.mainloop()