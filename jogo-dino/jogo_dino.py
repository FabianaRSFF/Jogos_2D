import os
from random import choice, randrange
from sys import exit

import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')


largura = 640
altura = 480
branco = (255, 255, 255)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Fabi_Dino_Game')

imagens_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()  # noqa

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'death_sound.wav'))  # noqa E501
som_colisao.set_volume(1)

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav'))   # noqa E501
som_pontuacao.set_volume(1)

colidiu = False

escolha_obstaculo = choice([0, 1])
pontos = 0

velocidade_jogo = 10


def exibe_mensagem(msg, tam_fonte, cor):
    fonte = pygame.font.SysFont('comicsansms', tam_fonte, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado


def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo
    pontos = 0
    velocidade_jogo = 10
    colidiu = False
    dino.rect.y = altura - 64 - 96 // 2
    dino.pulo = False
    dinovoador.rect.x = largura
    cactus.rect.x = largura
    escolha_obstaculo = choice([0, 1])
    

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))  # noqa
        self.som_pulo.set_volume(1)
        self.imagens_dinossauro = []
        for i in range(3):
            img = imagens_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = altura - 64 - 96//2
        self.rect.center = (100, altura - 64)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y_inicial
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]


class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagens_sheet.subsurface((7 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = largura - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= velocidade_jogo


class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagens_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.y = altura - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 10


class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagens_sheet.subsurface((5 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (largura, altura - 64)

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade_jogo


class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinovoador = []
        for i in range(3, 5):
            img = imagens_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dinovoador.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinovoador[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (largura, 300)
        self.rect.x = largura

    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_dinovoador[int(self.index_lista)]


todas_as_sprites = pygame.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)

for i in range(4):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

for i in range(largura * 2//64):
    chao = Chao(i)
    todas_as_sprites.add(chao)

cactus = Cactus()
todas_as_sprites.add(cactus)

dinovoador = DinoVoador()
todas_as_sprites.add(dinovoador)


grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(cactus)
grupo_obstaculos.add(dinovoador)

relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    tela.fill(branco)
    for event in pygame.event.get():
        if event.type == QUIT:
            event.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu == False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()
            if event.key == K_r and colidiu == True:
                reiniciar_jogo()
        
    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)  # noqa E501

    todas_as_sprites.draw(tela)

    if cactus.rect.topright[0] <= 0 or dinovoador.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0, 1])
        cactus.rect.x = largura
        dinovoador.rect.x = largura
        cactus.escolha = escolha_obstaculo
        dinovoador.escolha = escolha_obstaculo

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True
        
    if colidiu == True:
        if pontos % 100 == 0:
            pontos += 1
        game_over = exibe_mensagem('Game Over', 40, (0, 0, 0))
        tela.blit(game_over, (largura//2, altura//2))
        reiniciar = exibe_mensagem('Pressione r para reiniciar.', 20, (0, 0, 0))
        tela.blit(reiniciar, (largura//2, (altura//2) + 60))
    else:
        pontos += 1
        todas_as_sprites.update()
        texto_pontos = exibe_mensagem(pontos, 40, (0, 0, 0))

    if pontos % 100 == 0:
        som_pontuacao.play()
        if velocidade_jogo >= 23:
            velocidade_jogo += 0
        else:
            velocidade_jogo += 1
    
    tela.blit(texto_pontos, (520, 30))
    pygame.display.flip()
