import sqlite3
from issueScrapper import scrapIssue, find_between

conn = sqlite3.connect('MarvelNetworks')

print "Opened database successfully!"

url = "http://marvel.wikia.com/wiki/What_If%3F_Vol_1_9"
key = "WI? 9"

cursor = conn.execute("UPDATE IssuesURL SET URL = ? WHERE FullKey = ?" , (url, key))

conn.commit()
conn.close()