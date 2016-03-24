import sqlite3

conn = sqlite3.connect('MarvelNetworks')

print "Opened database successfully!"

cursor = conn.execute("CREATE TABLE MarvelAPIChars(ID INT PRIMARY KEY, Name TEXT, ImageURL TEXT);")

conn.commit()