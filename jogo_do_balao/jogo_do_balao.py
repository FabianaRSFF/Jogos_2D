from sys import exit
from typing import Any

import pygame
from pygame.locals import *

pygame.init()

largura = 640
altura = 480
preto = (0, 0, 0)

pygame.mixer.music.set_volume(0.1)
musica_de_fundo = pygame.mixer.music.load(
    'BoxCat Games - Battle (Special).mp3')
pygame.mixer.music.play(-1)

barulho_explosao = pygame.mixer.Sound('smw_firework.wav')

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('FabiBallon Game')

pontos = 0
fonte = pygame.font.SysFont('arial', 40, bold=True, italic=True)


class Balao(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('balao/sprite_00.png'))
        self.sprites.append(pygame.image.load('balao/sprite_01.png'))
        self.sprites.append(pygame.image.load('balao/sprite_02.png'))
        self.sprites.append(pygame.image.load('balao/sprite_03.png'))
        self.sprites.append(pygame.image.load('balao/sprite_04.png'))
        self.sprites.append(pygame.image.load('balao/sprite_05.png'))
        self.sprites.append(pygame.image.load('balao/sprite_06.png'))
        self.sprites.append(pygame.image.load('balao/sprite_07.png'))
        self.sprites.append(pygame.image.load('balao/sprite_08.png'))
        self.sprites.append(pygame.image.load('balao/sprite_09.png'))
        self.sprites.append(pygame.image.load('balao/sprite_10.png'))
        self.sprites.append(pygame.image.load('balao/sprite_11.png'))
        self.sprites.append(pygame.image.load('balao/sprite_12.png'))
        self.sprites.append(pygame.image.load('balao/sprite_13.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (128*3, 64*3))
        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 100

        self.animar = False

    def atacar(self):
        self.animar = True

    def update(self):
        if self.animar == True:
            self.atual = self.atual + 0.1
            if self.image == self.sprites[9]:
                barulho_explosao.play()
            if self.atual >= len(self.sprites):
                pygame.mixer.music.pause()
                self.atual = 0
                self.animar = False
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (128*3, 64*3))


todas_as_sprites = pygame.sprite.Group()
balao = Balao()
todas_as_sprites.add(balao)

imagem_fundo = pygame.image.load('pixel-art-city-background-at-sunset.jpg').convert()  # noqa
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    tela.fill(preto)
    for event in pygame.event.get():
        if event.type == QUIT:
            event.quit()
            exit()
        if event.type == KEYDOWN:
            balao.atacar()

    tela.blit(imagem_fundo, (0, 0))
    todas_as_sprites.draw(tela)
    todas_as_sprites.update()
    pygame.display.flip()