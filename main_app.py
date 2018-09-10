#!/usr/bin/python
# coding= utf-8

# Daniel Alves (principal contribuidor)
# Diogo Ferreira e Luís Leira
# Laboratórios de Informática, 2015
# Projeto 2
	
# Aplicação principal
# Programa desenhado para Python 2.x

import sqlite3
import os, os.path
import cherrypy
import sys
import json
import matplotlib.pyplot as plt
import socket
import urllib2
from inter import interp
from graph_creator import createForm
from sint import sintetizador

#cria as tabelas da base de dados, senão existirem
#criação da conexão ao ficheiro da base de dados e cronstrução do objecto de pesquisa
con = sqlite3.connect('music.db')
cur = con.cursor() 
reload(sys)  
sys.setdefaultencoding('utf8')
#cria tabela com informação de nome e pauta da música (se não existir)
cur.execute('''CREATE TABLE IF NOT EXISTS musics (music_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, stave TEXT)''')
#cria tabela com informação das diferentes interpretações e respetivos registos, e efeitos (se não existir)
cur.execute('''CREATE TABLE IF NOT EXISTS interpretations (interp_id INTEGER PRIMARY KEY AUTOINCREMENT, music_id INTEGER,
	register INTEGER, effect_echo TEXT, effect_tremolo TEXT, effect_perc TEXT, effect_chorus TEXT, effect_dist TEXT, effect_textttenv TEXT, posvotes INTEGER DEFAULT 0,
	negvotes INTEGER DEFAULT 0, FOREIGN KEY(music_id) REFERENCES music(music_id))''')


class Root(object):

	@cherrypy.expose
	#devolve a página incial
	def index(self):
		
		cherrypy.response.headers['Content-Type'] = 'text/html'
		return open('virtualhammond/index.html','r').read()

	@cherrypy.expose
	#adiciona uma nova música com base no nome, notas da pautas, 
	def createSong(self, name, notes, register, effect_echo, effect_tremolo, effect_perc, effect_chorus, effect_dist, effect_textttenv):
		
		name1 = name.encode('utf-8')
		notes1 = notes.encode('utf-8')
        
		con = sqlite3.connect('music.db')
		cur = con.cursor() 

		pauta = interp(notes)
		if len(pauta) == 0:
			returnjson =  '{"message": "The music '+ name + ' is not in the right format."}'
		else:

			#inserção na tabela musics o nome e a pauta introduzida pelo utilizador
			cur.execute('''INSERT INTO musics (name, stave) VALUES (?,?)''',(name1, notes1))
			con.commit()
			cur.execute('''SELECT music_id FROM musics WHERE name LIKE ?''',(name1,))
			musicid = cur.fetchall()[0][0]

			# Cria interpretação da música
			url = "http://"+cherrypy.server.socket_host+":8080/createInterpretation?musicid="+str(musicid)+"&register="+str(register)+"&effect_echo="+effect_echo+"&effect_tremolo="+effect_tremolo+"&effect_perc="+effect_perc+"&effect_chorus="+effect_chorus+"&effect_dist="+effect_dist+"&effect_textttenv="+effect_textttenv+""
			data = urllib2.urlopen(url).read()

			#criação de uma string com sintaxe que permite a codificação em JSON
			returnjson =  '{"message": "The music '+ name + ' was sucessfully added."}'
		
		#codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		#definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		#devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	#cria uma nova interpretação de uma música existente com base no registo e efeitos
	def createInterpretation(self, musicid, register, effect_echo, effect_tremolo, effect_perc, effect_chorus, effect_dist, effect_textttenv):
		
		register1 = register.encode('utf-8')
		effect_echo1 = effect_echo.encode('utf-8')
		effect_tremolo1 = effect_tremolo.encode('utf-8')
		effect_perc1 = effect_perc.encode('utf-8')
		effect_chorus1 = effect_chorus.encode('utf-8')
		effect_dist1 = effect_dist.encode('utf-8')
		effect_textttenv1 = effect_textttenv.encode('utf-8')


		con = sqlite3.connect('music.db')
		cur = con.cursor()
		#inserção na tabela interpretations de uma nova interpretação baseada no musicid,
		#registo e efeitos escolhidos pelo utilizador
		cur.execute('''INSERT INTO interpretations(music_id, register, effect_echo, effect_tremolo, effect_perc, effect_chorus, effect_dist, effect_textttenv, posvotes, negvotes) 
			VALUES (?,?,?,?,?,?,?,?,?,?)''',(musicid, register1, effect_echo1, effect_tremolo1, effect_perc1, effect_chorus1, effect_dist1, effect_textttenv1, 0, 0))
		con.commit()
		
		#criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '{"mensagem":"The new version was created with success!"}'

		#codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		#definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		#devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	#apresenta o nome das música para as quais já existe pauta na base de dados
	def listSongs(self):

		con = sqlite3.connect('music.db')
		cur = con.cursor() 
		#pesquisa pelo nome e id de todas as músicas presentes na base de dados
		cur.execute('''SELECT music_id, name FROM musics ORDER BY name''')
		songlist = cur.fetchall()

		#criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '['
		for x in songlist:
			returnjson+= '{"musicid":'+str(x[0])+','+'"nome":"'+x[1]+'"},'
		returnjson=returnjson[:-1]
		returnjson+=']'
		
		#codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		#definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"
		#return simplejson.dumps(returnarray)
		#devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	#devolve a informação sobre nome, registos, efeitos sonoros e ID das interpretações da musica.
	def listSongFiles(self, musicid):
		
		con = sqlite3.connect('music.db')
		cur = con.cursor() 
		#pesquisa pelo nome, id da interpretação, registo e efeitos de uma interpretação especifica
		cur.execute('''SELECT interp_id, name, register, effect_echo, effect_tremolo, effect_perc, effect_chorus, effect_dist, effect_textttenv, posvotes, negvotes 
			FROM musics, interpretations WHERE interpretations.music_id	LIKE ?  and musics.music_id LIKE ? ORDER BY name''', (musicid,musicid,))
		songlist = cur.fetchall()
		
		if len(songlist) == 0:
			returnjson = '{"message": "unsucess"}'
		#criação de uma string com sintaxe que permite a codificação em JSON
		else:
			returnjson =  '['
			for x in songlist:
				returnjson+= '{"interpid":'+str(x[0])+',"nome":"'+x[1]+'","register":"'+str(x[2])+'","effect_echo":"'+unicode(x[3])+'","effect_tremolo":"'+unicode(x[4])+'","effect_perc":"'+unicode(x[5])+'","effect_chorus":"'+unicode(x[6])+'","effect_dist":"'+unicode(x[7])+'","effect_texttt":"'+unicode(x[8])+'","posvotes":"'+str(x[9])+'","negvotes":"'+str(x[10])+'"},'
			returnjson=returnjson[:-1]
			returnjson+=']'

		#codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		#definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		#devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	#apresenta a pauta relativa a uma música. devolve o ID da música, o nome e a pauta
	def getNotes(self, musicid):
		
		con = sqlite3.connect('music.db')
		cur = con.cursor() 
		#pesquisa pela pauta de uma música especifica
		cur.execute('''SELECT music_id, name, stave FROM musics WHERE music_id LIKE ? ORDER BY name''', (musicid,))
		noteslist = cur.fetchall()
		
		#criação de uma string com sintaxe que permite a conversão para JSON
		returnjson =  '['
		for x in noteslist:
			returnjson+=  '{"musicid":'+str(x[0])+','+'"name":"'+x[1]+'","stave":"'+x[2]+'"},'
		returnjson=returnjson[:-1]
		returnjson+=']'

		#codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		#definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		#devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	#atualiza os valores relativos aos votos das interpretações
	def updateVotes(self, interpretationid, pos, neg):

		con = sqlite3.connect('music.db')
		cur = con.cursor() 
		#pesquisa pela pauta de uma música associada a uma interpretação especifica e
		#atualiza o número de votos na base de dados
		if neg == "0" :
			cur.execute('''UPDATE interpretations SET posvotes = ? WHERE interp_id LIKE ?''', (pos,interpretationid,))
		elif pos == "0" :
			cur.execute('''UPDATE interpretations SET negvotes = ? WHERE interp_id LIKE ?''', (neg,interpretationid,))
		con.commit()
		

	@cherrypy.expose
	#devolve um ficheiro WAV contendo a interpretação da música.
	def getWaveFile(self, interpretationid):
		con = sqlite3.connect('music.db')
		cur = con.cursor() 
		#pesquisa pela pautae dados de uma música associada a uma interpretação especifica
		cur.execute('''SELECT stave, register, effect_echo, effect_tremolo, effect_perc, effect_chorus, effect_dist, effect_textttenv FROM musics, interpretations WHERE musics.music_id = interpretations.music_id
			and interp_id LIKE ?''', (interpretationid,))
		
		# Guarda resultados da base de dados em variáveis
		getdb = cur.fetchall()
		stave = ""
		register = 0
		effect_echo = ""
		effect_tremolo = ""
		effect_perc = ""
		effect_chorus = ""
		effect_dist = ""
		effect_textttenv = ""
		for i in getdb:
			stave = i[0]
			register = i[1]
			effect_echo = i[2]
			effect_tremolo = i[3]
			effect_perc = i[4]
			effect_chorus = i[5]
			effect_dist = i[6]
			effect_textttenv = i[7]

		# Adiciona os efeitos a uma lista para enviar para processador de efeitos
		effects = []
		if not(effect_echo == "None"):
			effects.append("echo")
		if not(effect_tremolo == "None"):
			effects.append("tremolo")
		if not(effect_chorus == "None"):
			effects.append("chorus")
		if not(effect_dist == "None"):
			effects.append("dist")
		if not(effect_perc == "None"):
			effects.append("perc")
		if not(effect_textttenv == "None"):
			effects.append("textttenv")

		#chamado o interpretador de pautas
		notes = interp(stave)

		# Cria música
		sintetizador(notes, register, effects)

		# Retorna valor que indica que a música criada	
		returnjson = '{"message":"'+'musics/song.wav'+'"}'
        
        #codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)
        
		#definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"
        
		#devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	#devolve uma imagem contendo uma representação gráfica das notas.
	def getWaveForm(self, musicid):
		con = sqlite3.connect('music.db')
		cur = con.cursor() 		
		#pesquisa pela pauta de uma música associada a uma interpretação especifica
		cur.execute('''SELECT stave FROM musics WHERE music_id LIKE ?''', (musicid,))
		
		#pauta guardada na variável notes
		stave=cur.fetchall()[0][0]
		#chamado o interpretador de stave
		notes = interp(stave)

		createForm(notes)
		#pauta da música depois de interpretada


		returnjson =  '{"message":"'+'notes.png'+'"}'
		#codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		#definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		#devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)


#	Source:
#   http://commandline.org.uk/python/how-to-find-out-ip-address-in-python/
#	Função que retorna o endereço que se liga à internet, para garantir que é endereço certo.

def get_ip_address():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    ipaddr=s.getsockname()[0]
    return ipaddr


if __name__ == '__main__':
	print "Pode aceder à interface Web através do endereço " + socket.gethostbyname(get_ip_address())
	print "Para aceder à interface mobile, insira "+ socket.gethostbyname(get_ip_address()) +":8080/mindex.html"
	print "A interface mobile só fornece páginas com ações touch a partir da página principal."
	print "Caso não consiga aceder à página, insira manualmente o seu ip."

	cherrypy.server.socket_port = 8080
	# Caso opte por inserir manualmente o seu ip, comente a linha abaixo.
	cherrypy.server.socket_host = socket.gethostbyname(get_ip_address())
	# Caso tenha problemas, insira manualmente o seu ip.
	# ip = Insira manualmente o seu ip aqui
	# descomente as linhas superior e inferior
	# cherrypy.server.socket_host = ip

	current_dir = os.path.dirname(os.path.abspath(__file__))
	conf = {'/': {'tools.staticdir.root': current_dir},
					'/css': {	'tools.staticdir.on': True,
								'tools.staticdir.dir': 'virtualhammond/css'},
					'/js': {	'tools.staticdir.on': True,
								'tools.staticdir.dir': 'virtualhammond/js'},
					'/font-awesome': {	'tools.staticdir.on': True,
								'tools.staticdir.dir': 'virtualhammond/font-awesome'},
					'/images': {'tools.staticdir.on': True,
								'tools.staticdir.dir': 'virtualhammond/images'},
					'/fonts': {'tools.staticdir.on': True,
								'tools.staticdir.dir': 'virtualhammond/fonts'},
					'/musics': {'tools.staticdir.on': True,
								'tools.staticdir.dir': 'virtualhammond/musics'},
					'/showall.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/showall.html'},
					'/developers.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/developers.html'},
					'/index.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/index.html'},
					'/showinfo.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/showinfo.html'},
					'/showversions.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/showversions.html'},
					'/newmusic.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/newmusic.html'},
					'/newversion.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/newversion.html'},
					'/favicon.ico':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/favicon.ico'},
					'/mobile/css': {	'tools.staticdir.on': True,
								'tools.staticdir.dir': 'virtualhammond/mobile/css'},
					'/mobile/js': {	'tools.staticdir.on': True,
								'tools.staticdir.dir': 'virtualhammond/mobile/js'},
					'/mobile/fonts': {	'tools.staticdir.on': True,
								'tools.staticdir.dir': 'virtualhammond/mobile/fonts'},
					'/mshowall.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/mshowall.html'},
					'/mindex.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/mindex.html'},
					'/mshowinfo.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/mshowinfo.html'},
					'/mshowversions.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/mshowversions.html'},
					'/mnewmusic.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/mnewmusic.html'},
					'/mnewversion.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/virtualhammond/mnewversion.html'}
								}
	cherrypy.tree.mount(Root(),"/",conf)
	cherrypy.engine.start()
	cherrypy.engine.block()
