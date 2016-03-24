#Individual Network Info page text mock up
#Regular info: Image, name, alias, year created, first appearance
#Top 5 Encounters with other superheroes
#Network statistics

import sqlite3
from marvel.marvel import Marvel
from scrapperDef import scrapWiki, find_between

public_key = "b94a41b2612dd7f86517f823b4319417"
private_key = "8512a4a913969be34e3574573036c8648a8aa26b"

m = Marvel(public_key, private_key)

id = input("Enter ID: ")

id = int(id)

character = m.get_character(id).data.result

wikiURL = character.wiki

name, alias, app = scrapWiki(wikiURL)

conn = sqlite3.connect('databases/MarvelNetworks')

cursor = conn.execute("SELECT imageURL FROM MarvelAPIChars where ID = 1009378;")

for row in cursor:
	imageurl = row[0]

conn.close()

print imageurl 
print "Name: " + name
print "Alias: " + alias
print "First Appearance: " + app

apiname = character.name.upper()

conn = sqlite3.connect('databases/MarvelNetworks')

cursor = conn.execute("SELECT DISTINCT nm2.APIname, COUNT(*) FROM heroes_in_comics AS hic1 INNER JOIN nameMatch AS nm1 ON hic1.Name = nm1.HICname INNER JOIN heroes_in_comics AS hic2 ON hic1.Issue = hic2.Issue INNER JOIN nameMatch AS nm2 ON hic2.Name = nm2.HICname WHERE nm1.APIname = ? GROUP BY nm2.APIname ORDER BY COUNT(*) DESC LIMIT 6" , (apiname,))

topEncounters = []

for row in cursor:
	if row[0] != apiname:
		topEncounters.append(row[0])
		
print "Top 5 Encounters:"
for encounter in topEncounters:
	encounter = encounter.title()
	cursor = conn.execute("SELECT ImageURL FROM MarvelAPIChars WHERE Name = ?" , (encounter,))
	for row in cursor:
		img = row[0]
	print encounter
	print img
	
conn.close()


