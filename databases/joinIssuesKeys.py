#Inserts the full issue name with issue number into IssuesFullNames table by joining data from heroes_in_comics, Issues, and SeriesKeys tables

import sqlite3

conn = sqlite3.connect('MarvelNetworks')

print "Opened database successfully!"

cursor = conn.execute("SELECT heroes_in_comics.Issue, SeriesKeys.SeriesName || ' #' || Issues.IssueNumber FROM heroes_in_comics INNER JOIN Issues ON heroes_in_comics.Issue = Issues.FullKey INNER JOIN SeriesKeys ON SeriesKeys.Key = Issues.Key;")

for row in cursor:
	issueKey = row[0]
	fullIssueName = row[1]
	
	conn.execute("INSERT INTO IssuesFullNames (FullKey, FullName) VALUES (?, ?)"
			, (issueKey, fullIssueName))
			
conn.commit()
print "Success!"

conn.close()