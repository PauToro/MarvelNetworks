#Two Character Meeting Screen text mock up
#List of shared appearances, chronological
#Series with most shared appearances
#Images of two characters

import sqlite3

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

	
char1 = raw_input("Character 1: ")
char2 = raw_input("Character 2: ")

conn = sqlite3.connect('databases/MarvelNetworks')

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
	if issueYear != "No record found.":
		issueYear = int(issueYear)
		issueTuple = (issue, issueYear)
		issues.append(issueTuple)

conn.close()

sortedIssues = sorted(issues, key=getKey)
	
for issue in sortedIssues:
	currentLine = '{0:<30}\t{1:4}'.format(issue[0], issue[1])
	print currentLine
	
