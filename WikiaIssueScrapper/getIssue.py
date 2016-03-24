#Test for using scrapIssue as def from another file

from issueScrapper import scrapIssue, find_between

url = "http://marvel.wikia.com/wiki/Thor_253"

aYear = scrapIssue(url)
print "Year: " + aYear