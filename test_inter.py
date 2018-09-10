#!/usr/bin/python
# coding= utf-8

# Diogo Ferreira
# Laboratórios de Informática, 2015
# Projeto 2

# Teste para interpretador de pauta
# Programa desenhado para Python 2.x

import sys
import pytest
from inter import interp

def test_invalido():
    print "Testa comportamento com pautas inválidas"
    assert interp("The Simpsons:e6,f#6,8a6,g.6") == []
    assert interp("The Simpsons:d=4,o=5,b=160:c.6,e6,f#6,86") == []
    assert interp("The Simpsons:d=4,o=9,b=160:c.6,e6,f#6,86") == []

def test_valido():
    print "Testa comportamento com pautas válidas"
    assert interp("The Simpsons:d=4,o=5,b=160:c.6,e6,f#6,8a6,g.6,e6,c6,8a,8f#,8f#,8f#,2g,8p,8p,8f#,8f#,8f#,8g,a#.,8c6,8c6,8c6,c6") == [(0.5625, 262.0), (0.375, 330.0), (0.375, 370.0), (0.1875, 440.0), (0.5625, 392.0), (0.375, 330.0), (0.375, 262.0), (0.1875, 220.0), (0.1875, 185.0), (0.1875, 185.0), (0.1875, 185.0), (0.75, 196.0), (0.1875, 0.0), (0.1875, 0.0), (0.1875, 185.0), (0.1875, 185.0), (0.1875, 185.0), (0.1875, 196.0), (0.5625, 233.0), (0.1875, 262.0), (0.1875, 262.0), (0.1875, 262.0), (0.375, 262.0)]
    assert interp("IWantItThatWay:d=16,o=5,b=25:32p,32g,8a#.,d6,g.,f.,32g,8a#.,d6,g.,c.6,32g,8a#.,d6,g.,8f.,g.,a#.,d6,c6,32a#,a#") == [(0.3, 0.0), (0.3, 196.0), (1.7999999999999998, 233.0), (0.6, 294.0), (0.8999999999999999, 196.0), (0.8999999999999999, 175.0), (0.3, 196.0), (1.7999999999999998, 233.0), (0.6, 294.0), (0.8999999999999999, 196.0), (0.8999999999999999, 262.0), (0.3, 196.0), (1.7999999999999998, 233.0), (0.6, 294.0), (0.8999999999999999, 196.0), (1.7999999999999998, 175.0), (0.8999999999999999, 196.0), (0.8999999999999999, 233.0), (0.6, 294.0), (0.6, 262.0), (0.3, 233.0), (0.6, 233.0)]
    assert interp("DGenerationX:d=4,o=6,b=160:8e5,8p,8e5,d,8e,8e,8e,8e,8e5,8e5,8e5,8d,p,16p,8e5,8p,8e5,8b5,8b5,8c,8c,b5,e5,8e,8d,e.,b.5,c,f5,8g5,8f5,e5,8e,8d,e,8p,c.,b5,2g5,16f5,e5,8e,8d,e.,b.5,c,f5,8g5,8f5,e5") == [(0.1875, 165.0), (0.1875, 0.0), (0.1875, 165.0), (0.375, 294.0), (0.1875, 330.0), (0.1875, 330.0), (0.1875, 330.0), (0.1875, 330.0), (0.1875, 165.0), (0.1875, 165.0), (0.1875, 165.0), (0.1875, 294.0), (0.375, 0.0), (0.09375, 0.0), (0.1875, 165.0), (0.1875, 0.0), (0.1875, 165.0), (0.1875, 247.0), (0.1875, 247.0), (0.1875, 262.0), (0.1875, 262.0), (0.375, 247.0), (0.375, 165.0), (0.1875, 330.0), (0.1875, 294.0), (0.5625, 330.0), (0.5625, 247.0), (0.375, 262.0), (0.375, 175.0), (0.1875, 196.0), (0.1875, 175.0), (0.375, 165.0), (0.1875, 330.0), (0.1875, 294.0), (0.375, 330.0), (0.1875, 0.0), (0.5625, 262.0), (0.375, 247.0), (0.75, 196.0), (0.09375, 175.0), (0.375, 165.0), (0.1875, 330.0), (0.1875, 294.0), (0.5625, 330.0), (0.5625, 247.0), (0.375, 262.0), (0.375, 175.0), (0.1875, 196.0), (0.1875, 175.0), (0.375, 165.0)]