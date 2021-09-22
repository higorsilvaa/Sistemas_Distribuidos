import subprocess 
import time
import pymongo
import os
import random
from matplotlib.pyplot import *

def encerra_processos():
	for p in r:
		p.kill()

def printa_banco(arqName, collec):
	arq = open(arqName, 'w')
	for b in collec.find():
		for c in b:
			arq.write("%s: %s\n" % (c, b[c]))
		arq.write("\n")
	arq.close()

def gera_grafico(x, y, titleGraf='Gráfico Bidimensional', t='-', col='blue'):
	plot(x, y, t, color=col)
	title(titleGraf)
	grid()
	xlabel('tempo corrente(s)')
	ylabel('tempo de processamento(s)')
	ylim((0.0,0.05))
	
	for my in [max(y),min(y)]:
		myi = y.index(my)
		mx = x[myi]
		plot(mx, my, t, color='black')
		text(mx+.1,my,'%.5f(%i)'%(my,myi+1))
	
	savefig('Results/%s.png' % titleGraf, format='png', dpi=300)
	clf()

if __name__ == '__main__':
	os.system('rm -r Logs Results')
	os.system('mkdir Logs Results')

	error = open('Logs/Error.log', 'a')
	
	#Inicia o MongoDB
	try:
		os.system('sudo service mongod start')
	except:
		error.write("Mongo: Erro ao iniciar serviço mongo!")
		error.close()
		exit(1)
	
	PORTi = 27018 #Porta inicial e primária

	try:
		entrada = input("Número de hosts desejado: ")
		HOSTs = int(entrada) # Numero de hosts desejado
		entrada = input("Tempo de execução(min): ")
		tempo = int(entrada) #converto para segundos depois
	except:
		error.write("Entrada: Erro na entrada do número de hosts/tempo de execução")
		error.close()
		exit(1)

	for i in range(HOSTs):
		os.system('rm -r Host%i'%(i+1))
		os.system('mkdir Host%i'%(i+1))
	
	#Inicia os hosts nas pastas
	r = []
	for i in range(HOSTs):
		dirHost = 'Host%i'%(i+1)
		port = str(PORTi+i)
		r.append(subprocess.Popen(['mongod', '--dbpath', dirHost, '-port', port, '--replSet', 'rs0']))

	#Espera 15 segundos para os servidores se estabelecerem
	time.sleep(15)
	
	#Cria a configuração do cluster
	arq = open('scriptMongoShell.txt', 'w')
	arq.write('use test\nrs.initiate()\nrs.secondaryOk()\n')
	for i in range(1,HOSTs):
		arq.write("rs.add('localhost:%i')\n"%(PORTi+i))
	arq.close()

	#Configura o cluster usando MongoShell
	try:
		os.system('mongo -port %i < scriptMongoShell.txt'%(PORTi))
	except:
		error.write("Mongo: Erro na execução do script de mongo!")
		error.close()
		encerra_processos()
		exit(1)
	
	#Conecta com o primário
	client = pymongo.MongoClient('localhost', PORTi)

	db = client.get_database('test')
	books = db.get_collection('books')
	
	history = open('Results/History (%i hosts, %i min).log'%(HOSTs,tempo), 'w')

	idf = 0 #Chave primária(ajuda para deleção saber quantos registros existem)
	outs = 0 #Auxilia no controle dos nomes dos arquivos

	printa_banco('Logs/OutPutInitial.log', books) #Salva o conteúdo inicial do banco

	while True:
		entrada = input("Comando: ")
		history.write("Comando: %s\n"%(entrada))
		
		if entrada == "insert":
			outs += 1
			printa_banco('Logs/OutPut%iInitialInsert.log'%(outs), books)
			
			x = time.time()
			y, w = [], []
			y.append(x)
			while(y[-1] - x < float(tempo*60)):
				try:
					y[-1] -= x
					z = time.time()
					books.insert_one({"_id": idf, "nome": "aleatorio_"+str(idf),"idade": idf})
					y.append(time.time())
					w.append(y[-1]-z)
					idf += 1
				except pymongo.errors.NotPrimaryError:
					error.write("Insert: Não foi possível inserir os dados pois ele não é o primário!")
					break
				except:
					error.write("Insert: Erro desconhecido!")
					break
					
			history.write("\tTempo médio de escrita(seg): %.9f\n"%(sum(w)/float(len(w))))
			history.write("\tNúmero de escritas: %i\n"%len(w))
			
			y.pop(0) #Removendo o tempo inicial
			y[-1] -= x	

			gera_grafico(y, w, 'Tempo de Escrita (%i hosts, %i min)'%(HOSTs,tempo), '.', 'blue')
			
			printa_banco('Logs/OutPut%iFinalInsert.log'%(outs), books)
			
		elif entrada == "delete":
			outs += 1
			printa_banco('Logs/OutPut%iInitialDelete.log'%(outs), books)
			
			x = time.time()
			y, w = [], []
			y.append(x)
			while(y[-1] - x < float(tempo*60)):
				try:
					idf -= 1
					if idf < 0:
						break; #Pára quando não tiver mais registros
					y[-1] -= x
					z = time.time()
					books.delete_one({'_id': idf})
					y.append(time.time())
					w.append(y[-1]-z)
				except pymongo.errors.NotPrimaryError:
					error.write("Delete: Não foi possível deletar os dados pois ele não é o primário!")
					break
				except:
					error.write("Delete: Erro desconhecido!")
					break
			
			history.write("\tTempo médio de deleção(seg): %.9f\n"%(sum(w)/float(len(w))))
			history.write("\tNúmero de deleções: %i\n"%len(w))

			y.pop(0) #Removendo o tempo inicial
			y[-1] -= x
			
			gera_grafico(y, w, 'Tempo de Deleção (%i hosts, %i min)'%(HOSTs,tempo), '.', 'blue')
			
			printa_banco('Logs/OutPut%iFinalDelete.log'%(outs), books)
			
		elif entrada == "update":
			outs += 1
			printa_banco('Logs/OutPut%iInitialUpdate.log'%(outs), books)
			
			x = time.time()
			y, w = [], []
			y.append(x)
			while(y[-1] - x < float(tempo*60)):
				try:
					idfToUpdate = random.randint(0,idf-1) #Sorteia um idf para ser atualizado
					y[-1] -= x
					z = time.time()
					books.update_one({'_id': idfToUpdate}, {'$set': {'idade':idfToUpdate*2}})
					y.append(time.time())
					w.append(y[-1]-z)
				except pymongo.errors.NotPrimaryError:
					error.write("Update: Não foi possível atualizar os dados pois ele não é o primário!")
					break
				except:
					error.write("Update: Erro desconhecido!")
					break
					
			history.write("\tTempo médio de atualização(seg): %.9f\n"%(sum(w)/float(len(w))))
			history.write("\tNúmero de atualizações: %i\n"%len(w))
			
			y.pop(0) #Removendo o tempo inicial
			y[-1] -= x
			
			gera_grafico(y, w, 'Tempo de Atualização (%i hosts, %i min)'%(HOSTs,tempo), '.', 'blue')
			
			printa_banco('Logs/OutPut%iFinalUpdate.log'%(outs), books)
			
		elif entrada == "find":
			try:
				outs += 1
				printa_banco('Logs/OutPut%iFind.log'%(outs), books)
				
				x = time.time()
				y, w = [], []
				y.append(x)
				while(y[-1] - x < float(tempo*60)):
					try:
						idfToFind = random.randint(0,idf-1) #Sorteia um registro para ser procurado
						y[-1] -= x
						z = time.time()
						books.find_one({'_id': idfToFind})
						y.append(time.time())
						w.append(y[-1]-z)
					except pymongo.errors.NotPrimaryError:
						error.write("Find: Não foi possível ler os dados pois ele não é o primário e/ou não está autorizado!")
						break
					except:
						error.write("Find: Erro desconhecido!")
						break
				
				history.write("\tTempo médio de leitura(seg): %.9f\n"%(sum(w)/float(len(w))))
				history.write("\tNúmero de leituras: %i\n"%len(w))
				
				y.pop(0) #Removendo o tempo inicial
				y[-1] -= x
				
				gera_grafico(y, w, 'Tempo de Leitura (%i hosts, %i min)'%(HOSTs,tempo), '.', 'blue')

			except:
				error.write("Find: Erro na leitura dos dados!")
		elif entrada == "exit":
			break
		else:
			print("Comando inválido!")

	history.close()

	printa_banco('Logs/OutPutFinal.log', books)
	
	#Espera 15s antes de matar as servidores
	time.sleep(15)

	encerra_processos()
	
	#Apaga todos os dados
	for i in range(HOSTs):
		os.system('rm -r Host%i'%(i+1))
	
	error.close()
	
