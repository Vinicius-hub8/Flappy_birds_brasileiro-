import pygame
import random
import os
import tkinter as tk
from tkinter import simpledialog, messagebox  
from recursos import funcoes
from recursos import funcoesnew
from recursos.funcoes import inicializarBancoDeDados

tucano = pygame.image.load("assets/tucano.png")
tucano_caindo= pygame.image.load("assets/tucano_caindo.png")
tronco_cima = pygame.image.load("assets/tronco_cima.png")
tronco_baixo = pygame.image.load("assets/tronco_baixo.png")
fundo = pygame.image.load("assets/fundo do jogo.png")
musica_fundo = pygame.mixer.Sound("assets/musica_fundo.wav")
batida_tucano = pygame.mixer.Sound("assets/batida_tucano.wav")
canto_tucano = pygame.mixer.Sound("assets/canto_tucano.wav")
pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)  
branco = (255,255,255)
preto = (0,0,0)   

def jogar():
    largura_janela = 300
    altura_janela = 50
    def obter_nome():
        global nome
        nome = entry_nome.get()  
        if not nome:  
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  
        else:
            root.destroy()  


    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

        
    entry_nome = tk.Entry(root)
    entry_nome.pack()

    
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()


    root.mainloop()


#