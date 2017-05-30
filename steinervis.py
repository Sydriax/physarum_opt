import sys, json, os, math
import matplotlib.pyplot as plt
n, col = len(os.listdir(sys.argv[1])), sys.argv[2]
for (i, filename) in enumerate(os.listdir(sys.argv[1])):
	j = json.loads(open(sys.argv[1]+'/'+filename, 'r').read())
	name, lines = j['name'], j['lines'];
	length = round(sum([math.sqrt((line[0][0]-line[1][0])**2+(line[0][1]-line[1][1])**2) for line in lines]), 3)
	plt.plot([lines[0][0][0],lines[0][1][0]],[lines[0][0][1],lines[0][1][1]], lw=0.75, label=name+': '+str(length), c=col)
	for line in lines[1:]:
		plt.plot([line[0][0],line[1][0]],[line[0][1],line[1][1]], lw=0.75, c=col)
plt.title(sys.argv[1])
plt.legend(numpoints = 1)
plt.show()
