import sys, json, math
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
pts, edges = json.loads(open(sys.argv[1], 'r').read())['points'], []
mat = [[round(math.sqrt((q[0]-p[0])**2+(q[1]-p[1])**2), 3) for q in pts] for p in pts]
tree = minimum_spanning_tree(csr_matrix(mat)).toarray()
for (r, row) in enumerate(tree):
	for (c, val) in enumerate(row):
		if val != 0:
			edges.append([pts[r], pts[c]])
with open('steinertrees\minspan.json', 'w') as output:
	json.dump({ 'name': 'minimum spanning tree', 'lines': edges }, output)