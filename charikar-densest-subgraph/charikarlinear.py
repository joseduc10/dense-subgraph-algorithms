import charikar as ch
import time
import sys
from networkx import *

filename = sys.argv[1]
outfilename = sys.argv[2]

print filename

G = read_edgelist(filename)

print '-------'
print 'Charikar with linear min degree search:'
tic = time.clock()
S, avg = ch.charikarLinear(G)
toc = time.clock()
print 'time', toc-tic
print 'Average degree',avg
Sn, Sm =  S.number_of_nodes() , S.number_of_edges()
print 'Dense subgraph stats:'
print '# nodes', Sn
print '# edges', Sm
print 'avg degree', 2.0*Sm/Sn

for i in S.edges_iter():
    S[i[0]][i[1]]['weight'] = G[i[0]][i[1]]['weight']
write_edgelist(S,outfilename)

