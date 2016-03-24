#Scrap key and full titles from Marvel Chronology Project at http://www.chronologyproject.com/key.php
#Had to edit typos in source code so saved on computer

from bs4 import BeautifulSoup
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

def find_between(aString, first, last):
	try:
		start = aString.index(first) + len(first)
		end = aString.index(last, start)
		return aString[start:end]
	except ValueError:
		return ""

def find_between_r(aString, first, last):
	try:
		start = aString.rindex(first) + len(first)
		end = aString.rindex(last, start)
		return aString[start:end]
	except ValueError:
		return ""
  
currentURL = "http://marvel.com/universe/Spider-Man_(Peter_Parker)?utm_campaign=apiRef&utm_source=b94a41b2612dd7f86517f823b4319417"

soup = BeautifulSoup(urlopen(currentURL))

lines = soup.find_all('p')

list = []

for line in lines:
	list.append(line.encode('utf-8'))

for i in list:
	if "Real Name" in i:
		realNameLine = i
	elif "Aliases" in i:
		aliasesLine = i
	elif "First Appearance" in i:
		firstAppLine = i

realName = find_between(realNameLine, "<br/>", "</p>")
realName = realName.rstrip("\n")
print realName
aliases = find_between(aliasesLine, "<br/>", "</p>")
aliases = aliases.rstrip("\n")
print aliases
firstApp = find_between(firstAppLine, "<br/>", "</p>")
firstApp = firstApp.rstrip("\n")
print firstApp