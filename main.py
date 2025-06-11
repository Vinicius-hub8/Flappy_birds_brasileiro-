import pygame
import random
import os
import tkinter as tk
from tkinter import simpledialog, messagebox  
from recursos import funcoes
from recursos import funcoesnew
from recursos.funcoes import inicializarBancoDeDados

# Função para pedir o nome do jogador
def pedir_nome():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    nome = simpledialog.askstring("Nome do Jogador", "Digite seu nome:")
    root.destroy()
    if not nome:
        nome = "Jogador"
    return nome

pygame.init()
inicializarBancoDeDados()

# Pede o nome antes de iniciar o jogo
nome_jogador = pedir_nome()

tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)  
branco = (255,255,255)
preto = (0,0,0)   

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