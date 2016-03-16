from marvel.marvel import Marvel
from scrapperDef import scrapWiki, find_between
public_key = "b94a41b2612dd7f86517f823b4319417"
private_key = "8512a4a913969be34e3574573036c8648a8aa26b"

m = Marvel(public_key, private_key)

id = input("Enter ID: ")

character = m.get_character(id).data.result

wikiURL = character.wiki
print wikiURL

name, alias, app = scrapWiki(wikiURL)

print name
print alias
print app

print character.description