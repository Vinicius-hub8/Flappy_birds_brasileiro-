import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox  
from recursos import funcoes
from recursos.funcoes import inicializarBancoDeDados
pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho )  
branco=(255,255,255)
preto=(0,0,0)   
