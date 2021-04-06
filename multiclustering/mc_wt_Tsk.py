#Import modules
from greedy_weighted import greedyWeightedOQC
import sys
import time
import networkx as nx
import numpy as np

#Getting the inputs
graphfile = sys.argv[1]
outfname = sys.argv[2]
subgraphfileprefix = sys.argv[3]
iterations = int(sys.argv[4])

G = nx.read_edgelist(graphfile)

#Opening file for output
f = open(outfname, 'w')
alpha = 1/3.
"""
g=0;s=0;E=0
for node in G:
	if node.startswith("ENSG"):#changed for weighted
		g+= 1
		#print node
	else:#changed for weighted
		s+= 1
	E+=G.degree(node, weight='weight')
E /= 2
alpha = E / (g*s)
print alpha
E = G.number_of_edges()
alpha = E*1.0 / (g*s)
print alpha
sys.exit(0)
"""
#alpha=1
alpha=0.7
#alpha=0.5
#alpha=0.4

print >>f, '-------'
print >>f, 'Weighted Tsourakakis modified objective:'


for k in range(iterations):
	
	tic = time.clock()
	#Function call to Weighted Charikar
	S, obj = greedyWeightedOQC(G, alpha)
	
	#Printing the details of iteration
	toc = time.clock()
	print >> f, "i=",k,"\t",
	print >> f, 'time', toc-tic,"\t",
	
	n = len(S)
	e = S.number_of_edges()
	
	f.write('N: ' + str(n) + '\t')
	f.write('E: ' + str(e) + '\t')
	f.write('N/|G|: ' + str(n / float(len(G))) + '\t')
	f.write('2E/N(N-1): ' + str(2. * e / (n * (n - 1))) + '\t')
	#if nx.is_connected(S):
	#	f.write('Diameter: ' + str(nx.diameter(S)) + '\t')
	#else:
	#	f.write('Diameter: ' + 'inf\t')
	#f.write('CountingTriangles: ' + str( 2. * sum(i for i in nx.triangles(S).itervalues()) / (n * (n - 1) * (n - 2))) + '\t')
	f.write('Another metric: ' + str(e - alpha * ((n * (n - 1)) / 2)) + ',\n')
	f.write('Score: ' + str(obj) + '\t\n')
	
	#Setting weights to be included in the cluster output
	for i in S.edges_iter():
	    S[i[0]][i[1]]['weight'] = G[i[0]][i[1]]['weight']
	
	nx.write_edgelist(S,subgraphfileprefix+"_cluster"+str(k)+".txt")
	
	#Removing edges in the cluster from the graph
	for i in S.edges_iter():
		G[i[0]][i[1]]['weight']=0.0
	
	#nx.write_edgelist(G, subgraphfileprefix+"_G_after_"+str(k)+".txt")
	
	#Alt: filtering out non zero weight edges to write to the file
	#outfile = open(subgraphfileprefix+"_G_after_"+str(k)+".txt", "w")
	#for node1,node2 in G.edges_iter():
	#	if not G[node1][node2]['weight']==0.0:
	#		outfile.write(node1+" "+node2+" {\'weight\':"+str(G[node1][node2]['weight'])+"}\n")
	#outfile.close()

f.close()
