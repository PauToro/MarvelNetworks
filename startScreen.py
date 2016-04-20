from Tkinter import *
from PIL import Image, ImageTk
import Tkinter as tk
import sqlite3


	
def char1Display():
	prompt1 = Label(char1Frame, text="Character name:")
	prompt1.pack()
	singleCharEntry = Entry(char1Frame, bd=5)
	singleCharEntry.pack()
	
	subtmitSingle = Button(char1Frame, text="Enter", command=getSingleChar)

def getSingleChar():
	singleCharName = singleCharEntry.get()
	
def char2Display():
	prompt2 = Label(char2Frame, text="Character names:")
	prompt2.pack()
	doubleCharEntry1 = Entry(char2Frame, bd=5)
	doubleCharEntry2 = Entry(char2Frame, bd=5)
	doubleCharEntry1.pack()
	doubleCharEntry2.pack()
	
	subtmitSingle = Button(char1Frame, text="Enter", command=getDoubleChar)

def getDoubleChar():
	doubleCharName1 = doubleCharEntry1.get()
	doubleCharName2 = doubleCharEntry2.get()

graphicHeight = 255
graphicWidth = 400


win = tk.Tk()
win.configure(background="red4")


singleGraphic = PhotoImage(file="single.gif")
doubleGraphic = PhotoImage(file="double.gif")

#title frame
titleFrame = tk.Frame(win)
titleFrame.pack(pady=(5,50))
title = tk.Label(titleFrame, text="MARVELIST", font = ('Helvetica', 40), borderwidth=0)
title.pack()

#options frame
optionsFrame = tk.Frame(win)
optionsFrame.pack(fill=X)
optionsFrame.configure(background="red4")

#single character frame
char1Frame = tk.Frame(optionsFrame)
char1Frame.pack(side=LEFT, padx=(10,40))
char1Text = tk.Button(char1Frame, text="View Individual Character's\n Network", height=2, wraplength=graphicWidth, font = ('Helvetica', 20), command=char1Display, borderwidth=0)
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

win.mainloop()