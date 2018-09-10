#!/usr/bin/python
# coding= utf-8

# Diogo Daniel Soares Ferreira
# Laboratórios de Informática, 2015
# Projeto 2

# Processador de Efeitos
# Programa desenhado para Python 2.x


import wave
from struct import pack
from math import sin, pi
import os

# Função que normaliza o audio para poder ser enviado para ficheiro wav
def normalize(data):
    max = 0

    for i in data:
        if abs(i)>max:
            max = abs(i)

    data2 = []
    for i in data:
        data2.append(float(i)*(32767/float(max)))

    return data2

# Função que limita o audio aos valores máximos e mínimos, sem evitar clipping.
def clipping(data):
    data2 = []
    for i in data:
        if i>32767:
            data2.append(32767)
        elif i<-32767:
            data2.append(-32767)
        else:
            data2.append(i)

    return data2

# Efeito nulo. Apenas copia origem para destino
def effect_none(data, samples):
    data += samples
    return data

# Função que soma o sinal atual a um sinal futuro
def echo(data, dur, aten):
    i = 0
    dura = dur*44100
    while i<len(data):
        if i+dura<len(data):
            data[i+dura] += aten*data[i]
        i=i+1

    return data

# Variação da amplitude do sinal
def tremolo(data, a):
    i = 0
    freq = 440
    sample_rate = 44100
    data2 = []
    while i<len(data):
        data2.append(data[i] + a*sin(2*pi*freq*i/sample_rate)*data[i])
        i=i+1

    return data2

# Função que aplica distorção ao áudio.
# Função ligeiramente diferente do pedido no enunciado, para efeito ficar mais agradável.
# Pedido do enunciado nos comentários abaixo.
def dist(data, n):
    i = 0
    data2 = []
    while i<len(data):
		# data[i] = data[i] ** 2
        data[i] = data[i] * 0.01*data[i]
        i += 1

    return data

# Função que acrescenta uma frequência ligeiramente superior à atual.
def chorus(data, samples, freq):
    i = 0
    while i<len(samples):
        data.append(samples[i] + 32767*sin(2*pi*(freq+30)*i/44100))
        i += 1


    return data

# Valores de funções seguintes (efeitos) poderão ser alterados.
# Valores escolhidos para efeito criado ficar minimamente agradável.
def create_wav_file(tones, effects):
    dir = "virtualhammond/musics/song.wav"
    wv = wave.open(dir, 'w')
    wv.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))

    data = []
    # Percorre tons
    for tone in tones:
        if 'chorus' in effects:
            data = chorus(data, tone['samples'], tone['freq'])
        else:
            data = effect_none(data, tone['samples'])

    # Soma uma onda com o quádruplo da frequência, com a sua amplitude a decair ao longo do tempo.
    if 'perc' in effects:
        data2 = []
        j = 0
        for tone in tones:
            i=0
            while i<len(tone['samples']):
                data2.append((len(data)-j)*0.1*sin(4*tone['freq']*2*pi*i/44100))
                j+=1
                i+=1
        i = 0
        while i<len(data):
            data[i]+=data2[i]
            i+=1
        data = normalize(data)


    if 'chorus' in effects:
        data = normalize(data)
    if 'tremolo' in effects:
        data = tremolo(data, 0.3)
        data = normalize(data)
    if 'dist' in effects:
        data = dist(data, 2)
        data = clipping(data)
    if 'echo' in effects:
        data = echo(data, 1, 0.2)
        data = normalize(data)

    # Modela nota a nota, caso a frequência seja diferente da nota anterior ou da seguinte.
    if 'textttenv' in effects:
        k = 0
        for tone in range(len(tones)):
            i = 0
            j = 0.0
            while i<len(tones[tone]['samples']):
                if i<=len(tones[tone]['samples'])/8:
                    if(tone-1 >= 0 and tones[tone-1]['freq']==tones[tone]['freq']):
                        j = 0.5
                    data[k]*=j
                    j += (0.5/(len(tones[tone]['samples'])/8))/0.5
                elif i<=2*(len(tones[tone]['samples'])/8):
                    if(tone-1 >= 0 and tones[tone-1]['freq']==tones[tone]['freq']):
                        j = 0.5
                    data[k]*=j
                    j -= 0.5/(len(tones[tone]['samples'])/8)
                elif i<=6*(len(tones[tone]['samples'])/8):
                    data[k]*=j
                else:
                    if(tone+1 < len(tones) and tones[tone+1]['freq']==tones[tone]['freq']):
                        j = 0.5
                    data[k]*=j
                    j -= 0.5/(2*(len(tones[tone]['samples'])/8))
                i += 1
                k += 1
        data = normalize(data)

    wvData = ''
    for v in data:
        wvData += pack('h', v)

    wv.writeframes(wvData)
    wv.close()

    return dir