import networkx as nx
from bh import BinomialHeap

def greedyWeightedOQC(G, alpha, weight='weight'):
	
	#Using binomial heap to maintain and get the nodes by min degree
	heap = BinomialHeap()#changed for weighted
	heap_pointers = {}#changed for weighted
	
	#E = G.number_of_edges()
	E = 0.0#changed for weighted
	N = G.number_of_nodes()
	best_score = 0.0
	best_iter = 0

	# trivial case, empty graph
	#if E == 0:
	#	print "in here"
	#	return G

	#nodes_by_degree = {i: dict() for i in xrange(len(G))}
	degree_by_node = {}
	order = []
	neighbors = {}
	
	#new dictionaries
	samples = {}#changed for weighted
	genes = {}#changed for weighted

	for node in G:
		deg = G.degree(node, weight=weight)#changed for weighted
		#nodes_by_degree[deg][node] = 1	#changed for weighted
		degree_by_node[node] = deg
		neighbors[node] = {neighbor: 1 for neighbor in G.neighbors_iter(node)}
		heap_pointers[node] = heap.insert(deg, node)#changed for weighted - keep track of nodes in the heap
		E += deg#changed for weighted
		
		if node.startswith("ENSG"):#changed for weighted
			genes[node] = 1
			#print node
		else:#changed for weighted
			samples[node] = 1
	E /= 2#changed for weighted

	min_deg = 0
	#while not nodes_by_degree[min_deg]:
	#	min_deg += 1

	for it in xrange(N - 1):
		# update best subgraph
		
		#score = E - (alpha * (N * (N - 1) / 2.))
		#Different formula - consider set of samples and genes
		score = E - (alpha * len(samples)*len(genes))
		
		if best_score <= score:
			best_score = score
			best_iter = it
		
		# pick a node with minimum degree for deletion
		#min_deg_node = nodes_by_degree[min_deg].iterkeys().next()
		next_in_heap = heap.extract_min()#changed for weighted
		if next_in_heap is None:
			break
		min_deg, min_deg_node = next_in_heap#changed for weighted
		
		order.append(min_deg_node)
		#del nodes_by_degree[min_deg][min_deg_node] #changed for weighted - extract_min removes minimum node by itself
		E -= min_deg
		N -= 1
		
		#changes for weighted - tracking if genes or samples
		if min_deg_node in samples:
			del samples[min_deg_node]
		else:
			del genes[min_deg_node]
		
		# update neighbors
		# decrease the degree of all neighbors of min_deg_node
		# by one
		#for neighbor in neighbors[min_deg_node]:
		#	del nodes_by_degree[degree_by_node[neighbor]][neighbor]
		#	degree_by_node[neighbor] -= 1
		#	nodes_by_degree[degree_by_node[neighbor]][neighbor] = 1
		#	del neighbors[neighbor][min_deg_node]
		
		for neighbor in neighbors[min_deg_node]:
			if neighbor != min_deg_node:
				degree_by_node[neighbor] -= (1 if weight is None else G[min_deg_node][neighbor][weight])
				heap_pointers[neighbor].decrease(degree_by_node[neighbor])
				del neighbors[neighbor][min_deg_node]
		
		#changes for weighted - min degree is not updated, rather assigned
		#if min_deg > 0 and nodes_by_degree[min_deg - 1]:
		#	min_deg -= 1
		#else:
		#	while not nodes_by_degree[min_deg]:
		#		min_deg += 1

	S = nx.Graph()
	to_ignore = set(order[:best_iter])
	for u, v in G.edges_iter():
		if u not in to_ignore and v not in to_ignore:
			S.add_edge(u, v)
			S[u][v]['weight'] = G[u][v]['weight']
	return S, best_score

