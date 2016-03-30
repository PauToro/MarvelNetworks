import sqlite3

conn = sqlite3.connect('MarvelNetworks')

cursor = conn.execute("SELECT HICname, APIname FROM nameMatch;")

hicList = []
apiList = []

for row in cursor:
	hicList.append(row[0])
	apiList.append(row[1])
		
conn.close()

fNetwork = open('heroNetwork.txt', 'r')
sep = ';'
i = 0

for line in fNetwork:
	if sep in line:
		char1 = line.split(sep, 1)[0]
		char2 = line.split(sep, 1)[-1]
		char2 = char2.rstrip('\n')
		if char1 in hicList and char2 in hicList:
			print apiList[hicList.index(char1)] + ";" + apiList[hicList.index(char2)]
			
fNetwork.close()
			