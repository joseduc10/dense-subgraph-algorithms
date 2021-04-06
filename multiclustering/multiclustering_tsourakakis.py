#Import modules
import networkx as nx
from greedy_oqc import localSearchNegativeOQC
import sys
import time

#Getting the inputs
graphfile = sys.argv[1]
outfname = sys.argv[2]
subgraphfileprefix = sys.argv[3]
iterations = int(sys.argv[4])

#alpha value for OQC
alpha = 1/3.

G = nx.read_edgelist(graphfile)


#Opening file for output
f = open(outfname, 'w')

print >>f , '-------'
print >> f, "Running Tsourakakis local search"


for k in range(iterations):
	
	#Function call to Weighted Tsourakakis Local Search
	S, score = localSearchNegativeOQC(G, alpha, t_max=1000, seed=None)
	
	#Printing the details of iteration
	tic = time.clock()
	toc = time.clock()
	print >> f, "i=",k,"\t",
	print >> f, 'time', toc-tic
	header = "|S|,|E|,|S|/|V|,density,diameter,triangle density,OQC,time\n"
	
	n = len(S)
	e = S.number_of_edges()
	if n > 0:
		f.write(header)
		f.write(str(n) + ',')
		f.write(str(e) + ',')
		f.write(str(n / float(len(G))) + ',')
		f.write(str(2. * e / (n * (n - 1))) + ',')
		if nx.is_connected(S):
			f.write(str(nx.diameter(S)) + ',')
		else:
			f.write('inf,')
		f.write(str( 2. * sum(i for i in nx.triangles(S).itervalues()) / (n * (n - 1) * (n - 2))) + ',')
		f.write(str(e - alpha * ((n * (n - 1)) / 2)) + ',')
		f.write(str(toc-tic) + '\n')
	else:
		f.write("0,0,0,0,0,0,0,%s\n" % (end - start))
	
	#Setting weights to be included in the cluster output
	for i in S.edges_iter():
	    S[i[0]][i[1]]['weight'] = G[i[0]][i[1]]['weight']
	
	nx.write_edgelist(S,subgraphfileprefix+"_cluster"+str(k)+".txt")
	
	#Removing edges in the cluster from the graph
	for edge in S.edges_iter():
		G[i[0]][i[1]]['weight']=0
	
f.close()
