#Issue web scrapper

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
		
currentURL = "http://marvel.wikia.com/wiki/Official_Handbook_of_the_Marvel_Universe_Master_Edition_Vol_1_11"

soup = BeautifulSoup(urlopen(currentURL))

lines = soup.find_all('a')

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

i = 0
	
for line in lines:
	i += 1
	for month in months:
		if month in line:
			lineYear = lines[i].encode('utf-8')
			print lineYear
			year = find_between(lineYear, ">", "<")