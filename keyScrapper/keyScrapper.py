#Scrap key and full titles from Marvel Chronology Project at http://www.chronologyproject.com/key.php
#Had to edit typos in source code so saved on computer

from bs4 import BeautifulSoup
r = open('keyWebpage.html').read() 
soup = BeautifulSoup(r)

tables = soup.find_all('table')
key_table = tables[2]

for row in key_table.find_all('tr')[3:]:
	cells = row.find_all('td')
	print "%s|||%s" % (cells[0].text.encode('utf-8'), cells[1].text.encode('utf-8'))
