from marvel.marvel import Marvel
import time

public_key = "b94a41b2612dd7f86517f823b4319417"
private_key = "8512a4a913969be34e3574573036c8648a8aa26b"

m = Marvel(public_key, private_key)

namesMarvel = []

chars = m.get_characters(limit=100, offset=300)
for char in chars.data.results:
	namesMarvel.append([char.name, char.id])
	
for char in namesMarvel:
	id = str(char[1]).encode('utf8')
	name = char[0].encode('utf8')
	print id + ";" + name