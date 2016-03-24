import sqlite3
import wikia
conn = sqlite3.connect('MarvelNetworks')

print "Opened database successfully!"

cursor = conn.execute("SELECT DISTINCT Name FROM heroes_in_comics")

namesHIC = []

for row in cursor:
	namesHIC.append(row[0])

aliasList = []

for name in namesHIC:
	if '/' in name:
		sep = '/'
		alias = name.split(sep, 1)[0]
		aliasList.append(alias)

for name in namesHIC:
	if '/' in name:
		sep = '/'
		alias = name.split(sep, 1)[0]
		fullName = name.split(sep, 1)[-1]
	if ',' in name:
		sep = ','
		fullName = name.split(sep, 1)[-1] + " " + name.split(sep, 1)[0]
	if (('/') not in name) and ((',') not in name):
		i = 0
		while (i < (len(aliasList)) and (aliasList[i] not in name)):
			i += 1
		if  (i < len(aliasList)):
			alias = name
			fullName = 'NULL'
		else:
			alias = 'NULL'
			fullName = name			
				
conn.close()