import sys, json, math, random
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from copy import deepcopy
from tqdm import tqdm

# Calculate minimum spanning tree
def cal_min_span_tree(points):
	e = []
	points_list = list(points)
	mat = [[round(math.sqrt((q[0]-p[0])*(q[0]-p[0])+(q[1]-p[1])*(q[1]-p[1])), 3) for q in points_list] for p in points_list]
	tree = minimum_spanning_tree(csr_matrix(mat)).toarray()
	for (r, row) in enumerate(tree):
		for (c, val) in enumerate(row):
			if val != 0:
				e.append((points_list[r], points_list[c]))
	return set(e)

# Fermat point calculation
d=lambda x,y:math.sqrt(((x[0]-y[0])**2+(x[1]-y[1])**2))
s=lambda A,B,C:(d(B,C), d(C,A), d(A,B))
def j(a,b,c):
	return math.acos((b*b+c*c-a*a)/(2*b*c))
t=lambda a,b,c:1/math.cos(j(a,b,c)-math.pi/6)
b=lambda A,B,C,p,q,r:[(p*A[i]+q*B[i]+r*C[i])/(p+q+r) for i in [0,1]] 
f=lambda A,B,C:b(A,B,C,d(B,C)*t(*s(A,B,C)),d(C,A)*t(*s(B,C,A)),d(A,B)*t(*s(C,A,B)))

def has_fermat_point(a, b, c):
	return math.degrees(j(a, b, c)) < 120 and math.degrees(j(c, a, b)) < 120 and math.degrees(j(b, c, a)) < 120

def select_3_random(s):
	return random.sample(s, 3)

def select_3(s):
	while True:
		sample = select_3_random(s)
		d1 = d(sample[0], sample[1])
		d2 = d(sample[1], sample[2])
		d3 = d(sample[2], sample[0])
		if has_fermat_point(d1, d2, d3):
			return sample

def cal_length(e):
	return sum([math.sqrt((line[0][0]-line[1][0])**2+(line[0][1]-line[1][1])**2) for line in e])

def add_point(t):
	global edges, length, c_pts, n_pts
	triangle = select_3(c_pts)
	new_point = tuple(f(triangle[0], triangle[1], triangle[2]))
	n_c_pts = c_pts | set([new_point])
	n_edges = cal_min_span_tree(n_c_pts)
	n_length = cal_length(n_edges)
	if(should_accept(length, n_length, t)):
		edges = n_edges
		length = n_length
		c_pts = n_c_pts
		n_pts = n_pts | set([new_point])
		print('Added point')

def del_point(t):
	global edges, length, c_pts, n_pts
	point = random.sample(n_pts, 1)[0]
	n_c_pts = c_pts - set([point])
	n_edges = cal_min_span_tree(n_c_pts)
	n_length = cal_length(n_edges)
	if(should_accept(length, n_length, t)):
		edges = n_edges
		length = n_length
		c_pts = n_c_pts
		n_pts = n_pts - set([point])
		print('Deleted point')

def should_accept(v1, v2, t):
	if(v2 < v1 or math.exp((v1-v2) * t) < random.random()):
		print('True')
		return True
	else:
		print('False')
		return False

pts, n_pts = set([(p[0], p[1]) for p in json.loads(open(sys.argv[1], 'r').read())['points']]), set([])
edges = cal_min_span_tree(pts)
c_pts, length = set(pts), cal_length(edges)
best_edges, best_length = edges, length

INIT_TEMP = 0.5
ITER = 10000

for i in range(ITER):
	temperature = INIT_TEMP * math.pow(0.999, i)
	if len(n_pts) >= len(pts)-2:
		del_point(temperature)
	elif len(n_pts) == 0:
		add_point(temperature)
	else:
		if random.random() < 0.5:
			add_point(temperature)
		else:
			del_point(temperature)
	if length < best_length:
		best_edges = edges
		best_length = length
		print('Found new best. Length = '+str(best_length))
	print('Finished iteration #'+str(i))
with open('steinertrees\sa.json', 'w') as output:
	json.dump({ 'name': 'sa', 'lines': list(best_edges) }, output)