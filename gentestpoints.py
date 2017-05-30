import random, json
l = []
for i in range(100):
	l.append([random.random()*10-5,random.random()*10-5])
with open('points.json', 'w') as output:
	json.dump({ 'points': l }, output)