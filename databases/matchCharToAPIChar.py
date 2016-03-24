import sqlite3

conn = sqlite3.connect('MarvelNetworks')

print "Opened database successfully!"

cursor = conn.execute("SELECT DISTINCT Name FROM MarvelAPIChars;")

namesAPI = []

for row in cursor:
	namesAPI.append(row[0].upper())
	
#cursor = conn.execute("CREATE TABLE nameMatch(HICname TEXT, APIname TEXT, FOREIGN KEY(HICname) REFERENCES Characters(HICname), FOREIGN KEY(APIname) REFERENCES MarvelAPIChars(Name));")

#conn.commit()

null = "NULL"

cursor = conn.execute("SELECT HICname, Alias, FullName FROM Characters;")

for row in cursor:
	hicName = row[0]
	alias = row[1]
	fullName = row[2]
	if alias in namesAPI:
		apiAlias = namesAPI[namesAPI.index(alias)]
		conn.execute("UPDATE Characters SET APIname = ? WHERE HICname = ?" , (apiAlias, hicName))
	elif fullName in namesAPI:
		apiFN = namesAPI[namesAPI.index(fullName)]
		conn.execute("UPDATE Characters SET APIname = ? WHERE HICname = ?" , (apiFN, hicName))
	else:
		conn.execute("UPDATE Characters SET APIname = ? WHERE HICname = ?" , (null, hicName))
		
conn.commit()

conn.close()
	
