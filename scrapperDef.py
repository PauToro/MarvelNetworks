#Scrap Real Name, Alias, and First Appearance from Marvel Wiki page

from bs4 import BeautifulSoup
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

def find_between( aString, first, last):
	try:
		start = aString.index(first) + len(first)
		end = aString.index(last, start)
		return aString[start:end]
	except ValueError:
		return ""
 
def scrapWiki(wikiURL):
	soup = BeautifulSoup(urlopen(wikiURL), "html.parser")
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
	aliases = find_between(aliasesLine, "<br/>", "</p>")
	aliases = aliases.rstrip("\n")
	firstApp = find_between(firstAppLine, "<br/>", "</p>")
	firstApp = firstApp.rstrip("\n")
	return (realName, aliases, firstApp)