import os
import time
import json
from datetime import datetime
import random

def Limpartela():
    os.system('cls')

def aguardar(segundos):
    time.sleep(segundos)

def inicializarBancoDeDados():
    try:
        with open("base.atitus", "r") as banco:
            pass
    except:
        with open("base.atitus", "w") as banco:
            banco.write("{}")

def escreverDados(nome, pontos):
    try:
        with open("base.atitus", "r") as banco:
            dados = banco.read()
        if dados != "":
            dadosDict = json.loads(dados)
        else:
            dadosDict = {}
    except:
        dadosDict = {}

    datahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    registro = {"pontos": pontos, "data": datahora}
    if nome not in dadosDict:
        dadosDict[nome] = []
    dadosDict[nome].append(registro)
    with open("base.atitus", "w") as banco:
        banco.write(json.dumps(dadosDict))

def contar_partidas(nome):
    try:
        with open("base.atitus", "r") as banco:
            dados = banco.read()
        if dados != "":
            dadosDict = json.loads(dados)
        else:
            dadosDict = {}
    except:
        dadosDict = {}
    return len(dadosDict.get(nome, []))