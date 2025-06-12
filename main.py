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


 # Criação da janela principal
    root = tk.Tk()
    # Obter as dimensões da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)


# Configurações do jogador
player_x = 100
player_y = 350
player_vel = 5
player_largura = 50
player_altura = 50

# Loop principal do jogo
rodando = True
while rodando:
    relogio.tick(60)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimentação do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP]:
        player_y -= player_vel
    if teclas[pygame.K_DOWN]:
        player_y += player_vel

    # Limitar o jogador à tela
    if player_y < 0:
        player_y = 0
    if player_y > tamanho[1] - player_altura:
        player_y = tamanho[1] - player_altura

    # Desenhar tudo
    tela.fill(branco)
    pygame.draw.rect(tela, preto, (player_x, player_y, player_largura, player_altura))
    # Exibe o nome do jogador no canto superior esquerdo
    fonte = pygame.font.SysFont(None, 36)
    texto_nome = fonte.render(f"Jogador: {nome_jogador}", True, preto)
    tela.blit(texto_nome, (10, 10))
    pygame.display.flip()

pygame.quit()