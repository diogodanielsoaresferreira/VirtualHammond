#!/usr/bin/python
# coding= utf-8

# Diogo Daniel Soares Ferreira
# Laboratórios de Informática, 2015
# Projeto 2

# Interpretador de Pauta
# Programa desenhado para Python 2.x
# Caso a pauta não esteja no formato certo, irá lançar exceção e retornar lista vazia.

import sys

def interp(music):
	pauta = []
	dura = []
	frequ = []

	try:
		# Tenta ver se a entrada é válida, contando o número de ":"
		# Se for inválida, lança uma exceção
		n = 0
		for i in music:
			if i == ':':
				n = n+1
		if n != 2:
			raise exception

		# Tenta encontrar 'd', 'o' e 'b' na string recebida.
		# Se vários valores forem encontrados, prevalece o último.
		# Se nenhum valor for definido, d=4, o=5 e b=63 por definição.
		# Se não estiver no formato definido, lança exceção.

		i=0
		for i in range(len(music)):
			if music[i] == ':':
				break
		i = i+1
		d = 4
		o = 5
		b = 63

		while i < (len(music)):
			if music[i] == ':':
				break
			elif music[i] == ',' and music[i-1].isdigit():
				pass
			elif music[i].isalpha() and not(music[i-1]==',' or music[i-1]==':'):
				raise exception
			elif not(music[i].isdigit() or music[i] == 'd' or music[i] == 'D' or music[i] == 'o' or music[i] == 'O' or music[i] == 'b' or music[i] == 'B' or music[i] == '=' or music[i] == ','):
				raise exception
			elif music[i] == 'd' or music[i] == 'D':
				if music[i+1] == '=' and music[i+2].isdigit():
					j = i+2
					k = ""
					while music[j].isdigit():
						k += "" + music[j]
						j += 1
					d = int(k)
					i = j-1
				else:
					raise exception
			elif music[i] == 'o' or music[i] == 'O':
				if music[i+1] == '=' and music[i+2].isdigit():
					j = i+2
					k = ""
					while music[j].isdigit():
						k += "" + music[j]
						j += 1
					o = int(k)
					i = j-1
				else:
					raise exception
			elif music[i] == 'b' or music[i] == 'B':
				if music[i+1] == '=' and music[i+2].isdigit():
					j = i+2
					k = ""
					while music[j].isdigit():
						k += "" + music[j]
						j += 1
					b = int(k)
					i = j-1
				else:
					raise exception
			else:
				raise Exception
			i=i+1



		i = i+1
		if i >= len(music):
			raise exception


		while i<len(music):

			# Tenta ler valor da nota.
			# Caso a nota não exista, toma o valor de d.
			# Caso a nota seja inválido, lança exceção.

			v = d
			if music[i].isdigit():
				v = ""
				while music[i].isdigit():
					v += str(music[i])
					i += 1

				v = int(v)
				if not(v == 1 or v == 2 or v== 4 or v == 8 or v == 16 or v == 32):
					raise exception



			# Tenta ler tom da nota.
			# Caso seja inválido ou não exista, lança exceção.

			if not(music[i] == "a" or music[i] == "b" or music[i] == "c" or music[i] == "d" or music[i] == "e" or music[i] == "f" or music[i] == "g" or music[i] == "p" or music[i] == "h"):
				raise exception

			t = ""
			dot = False
			if i+1<len(music) and (music[i+1] == "#" or music[i+1] == "_"):
				t = music[i]+"#"
				i = i+2
			else:
				t = music[i]
				i = i+1

			if t == "h":
				t = b

			# Deteção da existência do ".".
			if i<len(music) and music[i] == ".":
				dot = True
				i = i+1

			# Deteção da oitava da nota, se existir
			# Caso seja inválida, lança um erro.
			oit = o

			if i<len(music) and music[i].isdigit():
				oit = int(music[i])
				i = i+1
			if oit<1 or oit>8:
				raise Exception


			if i<len(music) and music[i] == ",":
				i = i+1
			else:
				if not(i == len(music)):
					raise Exception


			# Calcula a duração da nota e guarda-a numa lista
			dur = (4/float(v)) * (60/float(b))
			if dot:
				dur = 1.5*dur

			dura.append(float(dur))

			# Calcula a frequencia fundamental da nota e guarda-a numa lista
			# Calcula as notas baixando duas oitavas da original.

			if t == "p":
				freq = 0
			else:
				freq = lut[t+str(oit-2)]

			frequ.append(float(freq))


		# Se tudo correr sem qualquer erro, retorna a pauta.
		i=0
		while i<len(dura):
			pauta.append((dura[i], frequ[i]))
			i+=1

		return pauta

	except:
		print "ERRO: Musica não está no formato correto!"
		return []

# Lookup table com frequências fundamentais
# Retirado de "Music Theory and Composition", http://donrathjr.com/wp-content/uploads/2010/07/Table-of-Frequencies1.png

lut = {'b#0': 16, 'b#1': 33, 'b#2': 65, 'b#3': 131, 'b#4': 262, 'b#5': 523, 'b#6': 1047, 'b#7': 2093, 'b#8': 4186,
	   'b0': 31, 'b1': 62, 'b2': 123, 'b3': 247, 'b4': 494, 'b5': 988, 'b6': 1976, 'b7': 3951, 'b8': 7902,
	   'a#0': 29, 'a#1': 58, 'a#2': 117, 'a#3': 233, 'a#4': 466, 'a#5': 932, 'a#6': 1865, 'a#7': 3729, 'a#8': 7459,
	   'a0': 28, 'a1': 55, 'a2': 110, 'a3': 220, 'a4': 440, 'a5': 880, 'a6': 1760, 'a7': 3520, 'a8': 7040,
	   'g#0': 26, 'g#1': 52, 'g#2': 104, 'g#3': 208, 'g#4': 415, 'g#5': 831, 'g#6': 1661, 'g#7': 3322, 'g#8': 6645,
	   'g0': 25, 'g1': 49, 'g2': 98, 'g3': 196, 'g4': 392, 'g5': 784, 'g6': 1568, 'g7': 3136, 'g8': 6272,
	   'f#0': 23, 'f#1': 46, 'f#2': 92, 'f#3': 185, 'f#4': 370, 'f#5': 740, 'f#6': 1480, 'f#7': 2960, 'f#8': 5920,
	   'f0': 22, 'f1': 44, 'f2': 87, 'f3': 175, 'f4': 349, 'f5': 698, 'f6': 1397, 'f7': 2794, 'f8': 5588,
	   'e#0': 22, 'e#1': 44, 'e#2': 87, 'e#3': 175, 'e#4': 349, 'e#5': 698, 'e#6': 1397, 'e#7': 2794, 'e#8': 5588,
	   'e0': 21, 'e1': 41, 'e2': 82, 'e3': 165, 'e4': 330, 'e5': 659, 'e6': 1319, 'e7': 2637, 'e8': 5274,
	   'd#0': 20, 'd#1': 39, 'd#2': 78, 'd#3': 156, 'd#4': 311, 'd#5': 622, 'd#6': 1245, 'd#7': 2489, 'd#8': 4978,
	   'd0': 18, 'd1': 37, 'd2': 73, 'd3': 147, 'd4': 294, 'd5': 587, 'd6': 1175, 'd7': 2349, 'd8': 4698,
	   'c#0': 17, 'c#1': 35, 'c#2': 69, 'c#3': 139, 'c#4': 277, 'c#5': 554, 'c#6': 1109, 'c#7': 2217, 'c#8': 4434,
	   'c0': 16, 'c1': 33, 'c2': 65, 'c3': 131, 'c4': 262, 'c5': 523, 'c6': 1047, 'c7': 2093, 'c8': 4186}

# Pauta para testes
#pauta = interp("EnterSan:d=4,o=5,b=225:8d5,4d6,4f6,4g#5,8g5,4d6,8d5,4d6,4f6,4g#5,8g5,4d6,8d5,4d6,4f6,4g#5,8g5,4d5,8f5,4d5,4e5,4d5,4e5,4f5,4e5,8d5")
#for i in pauta:
#	print i
