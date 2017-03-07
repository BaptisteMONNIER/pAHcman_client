#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
Client du jeu pAHcman
"""

import sys, pygame
import os
import time
from pygame.locals import *
import random
from PodSixNet.Connection import connection, ConnectionListener

"""
Charge une image png
Paramètres :
    - path : chemin de l'image
Retourne
    - image de type pygame.image
"""
def load_png(path):
        fullpath=os.path.join('.',name)
        try:
            image=pygame.image.load(fullpath)
            if image.get_alpha is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error:
            print('Cannot load image: %s' % name)
            raise SystemExit
        return image,image.get_rect()

"""
Classe GameClient
Hérite de :
    - ConnectionListener
"""
class GameClient(ConnectionListener):
    """
    Constructeur de la classe GameClient
    Parametres :
        - host : adresse du serveur
        - port : port du serveur en écoute
    """
    def __init__(self,host,port):
        self.Connect((host,port))
        self.run = False

    """
    Methode gérant le message connected
    Parametres :
        - data : message
    """
    def Network_connected(self,data):
        print('Client connecte au serveur')


    """
    Methode gérant le message start
    Parametres :
        - data : message
    """
    def Network_start(self,data):
        self.run = True


    """
    Methode gérant le message error
    Parametres :
        - data : message
    """
    def Network_connected(self,data):
        print('error :%s', data['error'][1])
        connection.Close()


    """
    Methode gérant le message disconnected
    Parametres :
        - data : message
    """
    def Network_disconnected(self,data):
        print('Deconnecte')
        sys.exit()

"""
Classe du sprite Denis
Hérite de :
    - pygame.sprite.sprite
    - ConnectionListener
"""
class Denis(pygame.sprite.Sprite, ConnectionListener):
    """
    Constructeur de la classe Denis
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        """
        self.image,self.rect=load_png("pics/denis/denis-w.png")

        self.image_e,_=load_png("pics/denis/denis-e.png")
        self.image_w,_=load_png("pics/denis/denis-w.png")
        self.image_ne,_=load_png("pics/denis/denis-ne.png")
        self.image_nw,_=load_png("pics/denis/denis-nw.png")
        self.image_se,_=load_png("pics/denis/denis-se.png")
        self.image_sw,_=load_png("pics/denis/denis-sw.png")

        self.rect.center = [SCREEN_WIDTH/2,SCREEN_HEIGHT/2]
        self.orientation = 'w'
        """
        
    """
    Methode gerant le message denis
    Parametres :
        - data : message
    """
    def Network_denis(self,data):
        self.orientation = data['denis'][2]
        if self.orientation == 'e'
            self.image = self.image_e
        elif self.orientation == 'w'
            self.image = self.image_w
        elif self.orientation == 'ne'
            self.image = self.image_ne
        elif self.orientation == 'nw'
            self.image = self.image_nw
        elif self.orientation == 'se'
            self.image = self.image_se
        elif self.orientation == 'sw'
            self.image = self.image_sw
        self.rect.center = data['denis'][0:2]

    """
    Methode mettant à jour l'affichage du sprite
    """
    def update(self):
        self.Pump()

"""
Main du client
"""
if __name__=='__main__':
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    gameClient = GameClient(sys.argv[1],int(sys.argv[2]))

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1,1)

    denis_sprite = pygame.sprite.RenderClear()
    denis_sprite.add(Denis())

    while True:
        clock.tick(60)
        connection.Pump()
        gameClient.Pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    if gameClient.run:
        keys = pygame.key.get_pressed()
        if keys[K_q]:
            sys.exit(0)

        conneciton.Send({'action':'keys','keystrokes':keys})

        denis_sprite.update()
        denis_sprite.draw(screen)


    pygame.display.flip()
