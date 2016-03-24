import sqlite3
from issueScrapper import scrapIssue, find_between

conn = sqlite3.connect('MarvelNetworks')

print "Opened database successfully!"

cursor = conn.execute("SELECT FullKey, URL FROM IssuesURL;")

for row in cursor:
	key = row[0]
	url = row[1]
	year = scrapIssue(url)
	print year

conn.close()