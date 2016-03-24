#Convert Issue Names to format used in Marvel Wikia URL
#Insert issue key and URL into IssuesURL table

import sqlite3

conn = sqlite3.connect('MarvelNetworks')

print "Opened database successfully!"

cursor = conn.execute("SELECT heroes_in_comics.Issue, SeriesKeys.SeriesName || ' ' || Issues.IssueNumber FROM heroes_in_comics INNER JOIN Issues ON heroes_in_comics.Issue = Issues.FullKey INNER JOIN SeriesKeys ON SeriesKeys.Key = Issues.Key;")

for row in cursor:
	issueKey = row[0]
	issueURL = row[1]
	issueURL = issueURL.replace(".", "")
	issueURL = issueURL.replace(" ", "_")
	issueURL = issueURL.title()
	issueURL = "http://marvel.wikia.com/wiki/" + issueURL
	
	conn.execute("INSERT INTO IssuesURL (FullKey, URL) VALUES (?, ?)"
			, (issueKey, issueURL))
			
conn.commit()
print "Success!"

conn.close()