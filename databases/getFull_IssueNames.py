#Separate issue # from key so that we can later match series keys
#Inserts full key, the series key, and the issue number into separate columns in Issues table

import sqlite3

conn = sqlite3.connect('MarvelNetworks')

print "Opened database successfully!"

cursor = conn.execute("SELECT DISTINCT Issue FROM heroes_in_comics")

IssueKeysNums = []

for row in cursor:
	IssueKeysNums.append(row[0])
	
for issueKeyNum in IssueKeysNums:
	sep = " -1" #Have to separate by space and following integer since some codes have spaces in them already
	digit = -1	#Some Issues have a "-1" as the issue number
	while (digit < 10) and (sep not in issueKeyNum):
		digit += 1
		sep = " " + str(digit)
	if sep in issueKeyNum:
		i = issueKeyNum.index(sep)
		issueKey = issueKeyNum.split(sep, 1)[0]
		issueNum = issueKeyNum[i+1:]
	else:
		issueKey = issueKeyNum
		issueNum = "NULL"

	conn.execute("INSERT INTO Issues (FullKey, Key, IssueNumber) VALUES (?, ?, ?)"
			, (issueKeyNum, issueKey, issueNum))	

conn.commit()
print "Success!"

conn.close()