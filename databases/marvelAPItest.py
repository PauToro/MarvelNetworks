# Calls Marvel API and adds outputs character IDs, name, and image thumbnail URLs to text file ready for csv
# Repeat until 1485 entries. Add 100 to b. While loop only works first time.  

from marvel.marvel import Marvel
import time

public_key = "b94a41b2612dd7f86517f823b4319417"
private_key = "8512a4a913969be34e3574573036c8648a8aa26b"

m = Marvel(public_key, private_key)

b = 0

namesMarvel = []

while b <= 200:
	chars = m.get_characters(limit=100, offset=b)
	for char in chars.data.results:
		namesMarvel.append([char.name, char.id, char.thumbnail])
	b += 100
	
for char in namesMarvel:
	id = str(char[1]).encode('utf8')
	name = char[0].encode('utf8')
	thumbnail = char[2].encode('utf8')
	print id + ";" + name + ";" + thumbnail