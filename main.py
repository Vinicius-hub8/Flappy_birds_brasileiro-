import pygame
import random
import os
from datetime import datetime
import pyttsx3
import json
import speech_recognition as sr
from recursos import funcoes

inicializarBancoDeDados = funcoes.inicializarBancoDeDados
escreverDados = funcoes.escreverDados
contar_partidas = funcoes.contar_partidas

def mostrar_historico_ultimas_partidas(tentativas=5):
    try:
        with open("base.atitus", "r") as banco:
            dados = banco.read()
        if dados != "":
            dadosDict = json.loads(dados)
        else:
            dadosDict = {}
    except:
        dadosDict = {}

    todas_partidas = []
    for nome, partidas in dadosDict.items():
        for p in partidas:
            if isinstance(p, dict):
                data = p.get('data', '')
                if len(data) <= 10:
                    data += " 00:00:00"
                pontos = p.get('pontos', '')
            elif isinstance(p, (tuple, list)) and len(p) == 2:
                pontos = p[0]
                data = p[1]
                if len(data) <= 10:
                    data += " 00:00:00"
            else:
                continue
            todas_partidas.append({
                "nome": nome,
                "data": data,
                "pontos": pontos
            })

    def parse_data(d):
        try:
            return datetime.strptime(d["data"], "%d/%m/%Y %H:%M:%S")
        except:
            return datetime.min
    todas_partidas.sort(key=parse_data, reverse=True)

    historico = []
    if not todas_partidas:
        historico.append("Nenhuma partida encontrada.")
    else:
        for p in todas_partidas[:tentativas]:
            historico.append(f"{p['nome']} | {p['pontos']} pts | {p['data']}")
    return historico

def pedir_nome_pygame():
    nome = ""
    ativo = True
    clock = pygame.time.Clock()
    input_box = pygame.Rect(300, 320, 400, 50)
    cor_ativa = pygame.Color('lightskyblue3')
    cor_inativa = pygame.Color('gray15')
    cor = cor_inativa
    fonte = pygame.font.SysFont(None, 48)
    fonte_pequena = pygame.font.SysFont(None, 28)
    while ativo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if nome.strip() == "":
                        nome = "Jogador"
                    ativo = False
                elif event.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 20 and event.unicode.isprintable():
                        nome += event.unicode

        tela.fill((30,30,30))
        bem_vindo_surface = fonte.render("Bem-vindo! Bote seu nome:", True, (0,255,255))
        tela.blit(bem_vindo_surface, (500 - bem_vindo_surface.get_width()//2, 200))
        txt_surface = fonte_pequena.render("Digite seu nome e pressione ENTER para começar", True, (255,255,255))
        tela.blit(txt_surface, (500 - txt_surface.get_width()//2, 250))
        pygame.draw.rect(tela, cor, input_box, 2)
        nome_surface = fonte_pequena.render(nome, True, (255,255,0))
        tela.blit(nome_surface, (input_box.x+10, input_box.y+10))
        pygame.display.flip()
        clock.tick(30)
    return nome

# --- Inicialização do pygame e assets ---
pygame.init()
pygame.mixer.init()
inicializarBancoDeDados()
tamanho = (1000, 700)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Flappy Tucano")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 48)
fonte_pequena = pygame.font.SysFont(None, 24)

tucano_img = pygame.image.load("assets/tucano-.png")
tucano = pygame.transform.scale(tucano_img, (60, 45))

tronco_img = pygame.image.load("assets/tronco.png")
tronco = pygame.transform.scale(tronco_img, (90, 600))

fundo = pygame.image.load("assets/fundo do jogo.png")
musica_fundo = pygame.mixer.Sound("assets/som de fundo.wav")
batida_tucano = pygame.mixer.Sound("assets/batida no tronco.mp3")
canto_tucano = pygame.mixer.Sound("assets/canto do tucano[.mp3")

def tela_morte(nome, score):
    historico = mostrar_historico_ultimas_partidas(tentativas=5)
    tela.fill((30,30,30))
    texto = fonte.render("VOCÊ MORREU!", True, (255, 0, 0))
    tela.blit(texto, (tamanho[0]//2 - texto.get_width()//2, 60))
    texto2 = fonte_pequena.render(f"Sua pontuação: {score}", True, (255,255,255))
    tela.blit(texto2, (tamanho[0]//2 - texto2.get_width()//2, 120))

    # Mostra cada linha do histórico, mas só se houver partidas
    y = 200
    if historico and historico[0] != "Nenhuma partida encontrada.":
        for linha in historico:
            if linha.strip() == "":
                continue
            linha_render = fonte_pequena.render(linha, True, (255,255,0))
            tela.blit(linha_render, (tamanho[0]//2 - 300, y))
            y += 32

    # Botão para jogar novamente
    botao_largura, botao_altura = 250, 50
    botao_x = tamanho[0]//2 - botao_largura//2
    botao_y = y + 60
    botao_rect = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)
    pygame.draw.rect(tela, (0, 150, 0), botao_rect)
    texto_botao = fonte_pequena.render("Jogar Novamente", True, (255,255,255))
    tela.blit(texto_botao, (botao_x + botao_largura//2 - texto_botao.get_width()//2, botao_y + botao_altura//2 - texto_botao.get_height()//2))

    # Botão para sair
    sair_largura, sair_altura = 120, 40
    sair_x = tamanho[0]//2 - sair_largura//2
    sair_y = botao_y + botao_altura + 30
    sair_rect = pygame.Rect(sair_x, sair_y, sair_largura, sair_altura)
    pygame.draw.rect(tela, (180, 0, 0), sair_rect)
    texto_sair = fonte_pequena.render("Sair", True, (255,255,255))
    tela.blit(texto_sair, (sair_x + sair_largura//2 - texto_sair.get_width()//2, sair_y + sair_altura//2 - texto_sair.get_height()//2))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(event.pos):
                    return "jogar"
                if sair_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    return "jogar"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def desenhar_sol(tela, frame, tamanho):
    import math
    raio = 30 + 10 * math.sin(frame/120)
    pygame.draw.circle(tela, (255,255,0), (tamanho[0]-60, 60), int(raio))

def jogar():
    nome = pedir_nome_pygame()
    player_x = 200
    player_y = 350
    player_vel = 7
    score = 0
    vivo = True
    dificuldade = 5
    pausa = False
    frame = 0

    espacamento = 400
    abertura = 180
    troncos = []
    for i in range(3):
        x = 1400 + i * espacamento
        altura = random.randint(150, 450)
        troncos.append([x, altura, False])  # [x, altura do topo, passou]

    musica_fundo.play(-1)

    while vivo:
        relogio.tick(60)
        frame += 1
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausa = not pausa
                if pausa:
                    tela.fill((0,0,0))
                    texto = fonte.render("PAUSE", True, (255,255,0))
                    tela.blit(texto, (tamanho[0]//2 - texto.get_width()//2, tamanho[1]//2 - texto.get_height()//2))
                    pygame.display.flip()
                    while pausa:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                                pausa = False
                        relogio.tick(10)
                    continue

        if pausa:
            continue

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            player_y -= player_vel
        if teclas[pygame.K_DOWN]:
            player_y += player_vel

        if player_y < 0:
            player_y = 0
        if player_y > tamanho[1] - tucano.get_height():
            player_y = tamanho[1] - tucano.get_height()

        for t in troncos:
            t[0] -= dificuldade
            if t[0] < -tronco.get_width():
                t[0] = max([tt[0] for tt in troncos]) + espacamento
                t[1] = random.randint(150, 450)
                t[2] = False

            if not t[2] and t[0] + tronco.get_width() < player_x:
                score += 1
                if random.random() < 0.1:
                    canto_tucano.play()
                dificuldade += 0.3
                t[2] = True

        tucano_rect = pygame.Rect(player_x, player_y, tucano.get_width(), tucano.get_height())
        for t in troncos:
            if not t[2]:
                tronco_cima_rect = pygame.Rect(
                    t[0],
                    t[1] - tronco.get_height(),
                    tronco.get_width(),
                    tronco.get_height()
                )
                tronco_baixo_rect = pygame.Rect(
                    t[0],
                    t[1] + abertura,
                    tronco.get_width(),
                    tronco.get_height()
                )
                if tucano_rect.colliderect(tronco_cima_rect) or tucano_rect.colliderect(tronco_baixo_rect):
                    batida_tucano.play()
                    vivo = False

        tela.blit(fundo, (0,0))
        for t in troncos:
            tela.blit(tronco, (t[0], t[1]-tronco.get_height()))
            tela.blit(tronco, (t[0], t[1]+abertura))
        tela.blit(tucano, (player_x, player_y))
        texto = fonte.render(f"Pontos: {score}  |  Dificuldade: {dificuldade:.1f}", True, (0,0,0))
        tela.blit(texto, (20, 20))
        texto_pausa = fonte_pequena.render("aperte espaço para pausar o jogo", True, (0,0,0))
        tela.blit(texto_pausa, (20, 80))
        desenhar_sol(tela, frame, tamanho)
        pygame.display.flip()

    escreverDados(nome, score)
    acao = tela_morte(nome, score)
    return acao

if __name__ == "__main__":
    while True:
        acao = jogar()
        if acao != "jogar":
            break
