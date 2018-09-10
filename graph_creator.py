#!/usr/bin/python
# encoding=utf-8

# Daniel Alves e Diogo Ferreira
# Laboratórios de Informática, 2015
# Projeto 2
	
# Graph plotter
# Programa desenhado para Python 2.x



#importado apenas o módulo matplotlib com o nome plt

import matplotlib.pyplot as plt
import os

# lista de teste criada pelo interpretador de pauta para a música dos Simpsons
#notes=[(0.5625, 1047.0), (0.375, 1319.0), (0.375, 1480.0), (0.1875, 1760.0), (0.5625, 1568.0), (0.375, 1319.0), (0.375, 1047.0), (0.1875, 880.0), (0.1875, 740.0), (0.1875, 740.0), (0.1875, 740.0), (0.75, 784.0), (0.1875, 0.0), (0.1875, 0.0), (0.1875, 740.0), (0.1875, 740.0), (0.1875, 740.0), (0.1875, 784.0), (0.5625, 932.0), (0.1875, 1047.0), (0.1875, 1047.0), (0.1875, 1047.0), (0.375, 1047.0)]

#função createForm será usada pela função getWaveForm na aplicação principal
def createForm(data):
	#Variável freqmin e freqmax são usadas para estabelecer um intervalo de visualização para o eixo vertical
	freqmax = float("-inf")
	freqmin = float("+inf")

	#O gráfico é criado usando retas horzintais entre dois pontos
	#Estes pontos são calculados com base na lista de frequências e os seus tempos de duração
	xinitial = 0.0
	for (time,freq) in data:
		#Procura o menor e o maior valor das frequencias
		if freq < freqmin:
			freqmin = freq
		if freq > freqmax:
			freqmax = freq

		#A variavel xfinal representa o valor da abcissa onde termina a linha horizontal e resulta da 
		#soma abcissa anterior com o valor do tempo para o qual se mantém a frequencia
		xfinal = xinitial + time

		#criação das linhas do gráfico com indicação dos pontos e da cor, padrão e grossura das linhas
		plt.plot((xinitial, xfinal), (freq,freq), 'k-', linewidth=7)

		#criação de um segundo gráfico de pontos nas extremidades finais de cada linha
		plt.plot(xfinal,freq, 'ro')
		xinitial = xfinal
	
	#O intervalo de visualização para o eixo vertical vai de uma valor 50 unidades inferior ao menor valor
	#de frequencias até um valor 50 unidades superior ao maior valor de frequencias
	plt.ylim(freqmin-50, freqmax+50)
	plt.axis('off')
	if os.path.isfile('virtualhammond/images/notes.png'):
		os.remove('virtualhammond/images/notes.png')
	plt.savefig('virtualhammond/images/notes.png', dpi=100)
	plt.clf()
	#Apresentação da imagem do gráfico
	#plt.show()

#createForm(notes)