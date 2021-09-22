import os

os.system('top -b -n1 | grep mongod > top.txt')

arq = open('top.txt', 'r')

for line in arq:
	splited = line.split()
	if splited[1] != 'mongodb': #print and kill it
		print(splited)
		os.system('kill %i' % int(splited[0]))

arq.close()
