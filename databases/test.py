import wikia

search = wikia.search("Marvel", "Emmanuel")

for article in search:
	print article