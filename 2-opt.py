import sys, json, math, random, copy
cal_dist = lambda a,b: math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
cal_length = lambda e: sum([cal_dist(l[0], l[1]) for l in e])
pts, edges = set([(p[0], p[1]) for p in json.loads(open(sys.argv[1], 'r').read())['points']]), []
point = random.sample(pts, 1)[0]
firstpoint = copy.copy(point)
pts = pts - set([point])
while len(pts) > 0:
	mindist, minpoint = 99**99, None
	for p in pts:
		dist = cal_dist(point, p)
		if dist < mindist:
			mindist = dist
			minpoint = p
	edges.append((point, minpoint))
	point = minpoint
	pts = pts - set([point])
print(len(edges))
edges.append((point, firstpoint))
print(len(edges))
counter = 1
for k in range(40):
	l_before = cal_length(edges)
	should_break = False
	for i1 in range(len(edges)):
		d1 = cal_dist(edges[i1][0],edges[i1][1])
		for i2 in range(i1+2, len(edges)):
			v1 = d1 + cal_dist(edges[i2][0],edges[i2][1])
			v2 = cal_dist(edges[i1][0],edges[i2][0]) + cal_dist(edges[i2][1],edges[i1][1])
			if v2 < v1:
				print('Swap', counter)
				t1 = (edges[i1][0],edges[i2][0])
				t2 = (edges[i1][1],edges[i2][1])
				edges[i1] = t1
				edges[i2] = t2
				for i in range(i1+1, i2):
					edges[i] = (edges[i][1], edges[i][0])
				assert(len(edges) == 100)
				should_break = True
				counter += 1
				break
			#else: print('No Swap!')
		if should_break:
			break
	print('2')
	l_after = cal_length(edges)
	print(l_before, l_after)
	assert(l_after <= l_before)
	if l_after == l_before:
		break
longest_edge, longest_edge_length = None, -1
for i in range(len(edges)):
	l = cal_dist(edges[i][0],edges[i][1])
	if l > longest_edge_length:
		longest_edge_length = l
		longest_edge = i
del edges[longest_edge]
with open('test/2-opt.json', 'w') as output:
	json.dump({ 'name': '2-opt tsp', 'lines': list(edges) }, output)