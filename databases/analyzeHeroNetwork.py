#Create network using networkMatch table.
#Get relevant measures for particular node (character)
#Draw graph and highlight location of particular node (character)

import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_edgelist('networkMatch.csv', delimiter=';')

character = "MAGNETO"

print "Degrees: " + str(G.degree(character))
close_cen = nx.closeness_centrality(G)
bet_cen = nx.betweenness_centrality(G)

for name, cc in close_cen.iteritems():
	if name == character:
		print "Betweenness Centrality: " + str(cc)

for name, bc in bet_cen.iteritems():
	if name == character:
		print "Closeness Centrality: " + str(bc)
		
nx.draw(G)
#plt.savefig("test.png")
				
#cent_items = [(b,a) for (a,b) in close_cen.iteritems()]
#cent_items.sort()
#cent_items.reverse()

#print tuple(reversed(cent_items[0]))