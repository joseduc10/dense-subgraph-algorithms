#Import modules
import networkx as nx
import charikar as ch
import sys
import time

#Getting the inputs
graphfile = sys.argv[1]
outfname = sys.argv[2]
subgraphfileprefix = sys.argv[3]
iterations = int(sys.argv[4])

G = nx.read_edgelist(graphfile)

#Opening file for output
f = open(outfname, 'w')

print >>f, '-------'
print >>f, 'Charikar with linear min degree search:'


for k in range(iterations):
	
	#Function call to Weighted Charikar
	S, avg = ch.charikarWeighted(G, weight='weight')
	
	#Printing the details of iteration
	tic = time.clock()
	toc = time.clock()
	print >> f, "i=",k,"\t",
	print >> f,  'time', toc-tic,"\t",
	print >> f,  'Average degree',avg,"\t",
	Sn, Sm =  S.number_of_nodes() , S.number_of_edges()
	print >> f,  'Dense subgraph stats:',
	print >> f,  '# nodes', Sn,"\t",
	print >> f,  '# edges', Sm,"\t",
	print >> f,  'avg degree', 2.0*Sm/Sn
	
	#Setting weights to be included in the cluster output
	for i in S.edges_iter():
	    S[i[0]][i[1]]['weight'] = G[i[0]][i[1]]['weight']
	
	nx.write_edgelist(S,subgraphfileprefix+"_cluster"+str(k)+".txt")
	
	#Removing edges in the cluster from the graph
	for i in S.edges_iter():
		G[i[0]][i[1]]['weight']=0
	
	nx.write_edgelist(G, "G_after_"+str(k)+".txt")

f.close()
