#!/usr/local/bin/python

#Traveling Salesman Solution using 2-opt Algorithm
#Scott Stevenson, Jack Koppenaal, John Costantino

import math, random, json, sys, copy

get_distance = lambda a,b: math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

#A function to get the total weight of a path
def get_weight(perm):
	return sum([get_distance(index_to_point[perm[i-1]], index_to_point[perm[i]]) for i in range(len(perm))])

#Calculate the 'best' tour for a set of cities using 2-opt
def two_opt(cities, numrounds, numiters):
	#Initialize the total weight to be averaged to 0
	results = 0
	#Create the initial 1...N permutation and find its weight
	curbest = [[], None]
	for city in cities:
		curbest[0].append(city[0])
	curbest[1] = get_weight(curbest[0])
	everbest = curbest

	for w in range(numrounds):
		for x in range(0, numiters):
			old_length = curbest[1]
			next = [curbest[0][:], curbest[1]]
			for num1 in range(len(cities)-1):
				break_iter = False
				for num2 in range(num1+1, len(cities)):
					#Swap the edges and get the new weight
					next[0][num1], next[0][num2] = next[0][num2], next[0][num1]
					next[1] = get_weight(next[0])
					#If the new tour is better than the old tour, set new tour as current best
					if next[1] < curbest[1]:
						curbest = next
						break_iter = True
						print('Made swap')
						break
					else:
						#Reset
						next[0][num1], next[0][num2] = next[0][num2], next[0][num1]
				if break_iter: break
			if curbest[1] == old_length:
				print('Reached local minimum after '+str(x)+' iterations')
				break
		print(everbest[1], curbest[1])
		if curbest[1] < everbest[1]:
			print('v-opt improvement made -- '+str(curbest[1]))
			everbest = copy.deepcopy(curbest)
		else:
			print('no v-opt improvement made -- '+str(curbest[1]))
			curbest = copy.deepcopy(everbest)
		to_shuffle = random.sample(curbest[0], 2)
		print(str(to_shuffle))
		temp = curbest[0][to_shuffle[0]]
		curbest[0][to_shuffle[0]] = curbest[0][to_shuffle[1]]
		curbest[0][to_shuffle[1]] = temp
		curbest[1] = get_weight(curbest[0])

	#Return an arbitrary path and the average of all of the results of the rounds
	return everbest[0]

cities = set([(i, p[0], p[1]) for i, p in enumerate(json.loads(open(sys.argv[1], 'r').read())['points'])])
index_to_point = { i: (p[0], p[1]) for i, p in enumerate(json.loads(open(sys.argv[1], 'r').read())['points']) }

city = random.sample(cities, 1)[0]
greedy_cities = [city]
cities = cities - set([city])
while len(cities) > 0:
	mindist, minpoint = 99**99, None
	for c in cities:
		dist = get_distance((city[1], city[2]), (c[1], c[2]))
		if dist < mindist:
			mindist = dist
			mincity = c
	greedy_cities.append(mincity)
	city = mincity
	cities = cities - set([mincity])

#Set the default values for rounds and iters
rounds = 50
iters = 999999

edges = []
ordered_pts = two_opt(greedy_cities, rounds, iters)
print(ordered_pts)
for i in range(len(greedy_cities)):
	edges.append((index_to_point[ordered_pts[i-1]], index_to_point[ordered_pts[i]]))
longest_edge, longest_edge_length = None, -1
for i in range(len(edges)):
	l = get_distance(edges[i][0],edges[i][1])
	if l > longest_edge_length:
		longest_edge_length = l
		longest_edge = i
del edges[longest_edge]
with open('steinertrees/v-opt.json', 'w') as output:
	json.dump({ 'name': 'v-opt tsp', 'lines': list(edges) }, output)