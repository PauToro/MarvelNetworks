#Functions for start screen

from Tkinter import *
from PIL import Image, ImageTk
import Tkinter as tk
import sqlite3
from autocomplete import *
	
def char1Display():
	prompt1 = Label(char1Frame, text="Character name:")
	prompt1.pack()
	singleCharEntry = AutocompleteEntry(char1Frame, bd=5)
	singleCharEntry.set_completion_list(charNamesList)
	singleCharEntry.pack()
	singleCharEntry.focus_set()
	
	subtmitSingle = Button(char1Frame, text="Enter", command=getSingleChar)

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