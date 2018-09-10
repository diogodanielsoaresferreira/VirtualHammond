#!/usr/bin/python
# coding= utf-8
# Abel Neto e Diogo Ferreira            #
# Laboratórios de Informática, 2015     #
# Projeto 2                             #
#---------------------------------------#
#       Sintetizador                    #
#########################################

from struct import pack
import wave
import sys
import math
import time
import logging
from inter import interp
from effects_processor import create_wav_file

#  Função que normaliza o audio para poder ser enviado para ficheiro wav (limpa Clipping)
def normalize(data):
    max = 0
    for i in data:
        if abs(float(i))>max:
            max = abs(float(i))
    data2 = []
    if max==0:		# Para garantir a divisao por número diferente de 0.
        return data
    for i in data:
        data2.append(float(i)*(32767/float(max)))   #float(i) * constante de normalizacao
    return data2



def sintetizador(data, reg, effects):
    # Se registo não tiver 9 algarismos, lança exceção.
    # Se algum algarismo não estiver entre 0 e 8, lança exceção
    if len(str(reg))!=9:
        raise Exception
    for i in str(reg):
        if int(i)<0 or int(i)>8:
            raise Exception

    enddata = []
    rate = 44100.0    #frequência de amostragem
    amplitude = 32767 #valor maximo definido pelo numero max de bits por sample
    mult = [1/2, 2/3, 1, 2, 3, 4, 5, 6, 8]

    for j in data:      #A Formula desta funcao encontra-se no relatorio sob o Capitulo Sintetizador
        frame = []
        info = {}
        duration = j[0]
        freq = j[1]
        i=1
        while i < rate*duration:
            frame.append(amplitude*(int(str(reg)[0])/8.0)*math.sin(2.0*math.pi*(freq*mult[0])*i/rate)+
                         amplitude*(int(str(reg)[1])/8.0)*math.sin(2.0*math.pi*(freq*mult[1])*i/rate)+
                         amplitude*(int(str(reg)[2])/8.0)*math.sin(2.0*math.pi*(freq*mult[2])*i/rate)+
                         amplitude*(int(str(reg)[3])/8.0)*math.sin(2.0*math.pi*(freq*mult[3])*i/rate)+
                         amplitude*(int(str(reg)[4])/8.0)*math.sin(2.0*math.pi*(freq*mult[4])*i/rate)+
                         amplitude*(int(str(reg)[5])/8.0)*math.sin(2.0*math.pi*(freq*mult[5])*i/rate)+
                         amplitude*(int(str(reg)[6])/8.0)*math.sin(2.0*math.pi*(freq*mult[6])*i/rate)+
                         amplitude*(int(str(reg)[7])/8.0)*math.sin(2.0*math.pi*(freq*mult[7])*i/rate)+
                         amplitude*(int(str(reg)[8])/8.0)*math.sin(2.0*math.pi*(freq*mult[8])*i/rate))
            i+=1
        frame = normalize(frame)
        info['freq'] = j[1]
        info['samples'] = frame
        enddata.append(info)

    return create_wav_file(enddata, effects)

