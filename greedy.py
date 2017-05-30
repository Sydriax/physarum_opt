import sys, json, math, random
pts, edges = set([(p[0], p[1]) for p in json.loads(open(sys.argv[1], 'r').read())['points']]), []
point = random.sample(pts, 1)[0]
pts = pts - set([point])
while len(pts) > 0:
	mindist, minpoint = 99**99, None
	for p in pts:
		dist = math.sqrt((point[0]-p[0])**2+(point[1]-p[1])**2)
		if dist < mindist:
			mindist = dist
			minpoint = p
	edges.append((point, minpoint))
	point = minpoint
	pts = pts - set([point])
with open('steinertrees\greedy.json', 'w') as output:
	json.dump({ 'name': 'greedy tsp', 'lines': edges }, output)