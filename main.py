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
        fullpath=os.path.join('.',path)
        try:
            image=pygame.image.load(fullpath)
            if image.get_alpha is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error:
            print('Cannot load image: %s' % path)
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
    def Network_error(self,data):

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
        self.image,self.rect=load_png("pics/denis/denis-w.png")

        self.image_e,_=load_png("pics/denis/denis-e.png")
        self.image_w,_=load_png("pics/denis/denis-w.png")
        self.image_ne,_=load_png("pics/denis/denis-ne.png")
        self.image_nw,_=load_png("pics/denis/denis-nw.png")
        self.image_se,_=load_png("pics/denis/denis-se.png")
        self.image_sw,_=load_png("pics/denis/denis-sw.png")

        self.image = self.image_w
        self.rect.center = [SCREEN_WIDTH/2,SCREEN_HEIGHT/2]
        self.orientation = 'w'


    """
    Methode gerant le message denis
    Parametres :
        - data : message
    """
    def Network_denis(self,data):
        self.orientation = data['denis'][2]
        if self.orientation == 'e':
            self.image = self.image_e
        elif self.orientation == 'w':
            self.image = self.image_w
        elif self.orientation == 'ne':
            self.image = self.image_ne
        elif self.orientation == 'nw':
            self.image = self.image_nw
        elif self.orientation == 'se':
            self.image = self.image_se
        elif self.orientation == 'sw':
            self.image = self.image_sw

        self.rect.center = data['denis'][0:2]

    """
    Methode mettant à jour l'affichage du sprite
    """
    def update(self):
        self.Pump()

class AhBleu(pygame.sprite.Sprite, ConnectionListener):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image,_=load_png("pics/ah.png")
        self.rect = pygame.Rect(20,20,self.image.get_width(),self.image.get_height())

    def update(self):
        self.Pump()

    def Network_AhBleu(self,data):
        self.rect.center = data['AhBleu'][0:2]



class Mur(pygame.sprite.Sprite, ConnectionListener):
    def __init__(self,x,y,w,h,r,g,b):
        pygame.sprite.Sprite.__init__(self)


        self.image = pygame.Surface((w,h),0,None)
        self.rect = pygame.Rect(x,y,w,h)
        self.image.fill((r,g,b))

"""
Main du client
"""
if __name__=='__main__':
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768

    gameClient = GameClient(sys.argv[1],int(sys.argv[2]))

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.key.set_repeat(70,70)


    background = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),0, None)

    screen.blit(background,(0,0),None,0)

    denis_sprite = pygame.sprite.RenderClear()
    denis_sprite.add(Denis())

    mur_sprite = pygame.sprite.RenderClear()

    r = 255
    g = 0
    b = 0

    #Haut de la map
    mur_sprite.add(Mur(0,0,SCREEN_WIDTH,15,255,0,0))
    mur_sprite.add(Mur(SCREEN_WIDTH/2-5,15,10,100,255,0,0))


    #Côté gauche de la map
    mur_sprite.add(Mur(0,15,15,170,r,g,b))
    mur_sprite.add(Mur(0,185,200,15,r,g,b))
    mur_sprite.add(Mur(200,185,15,80,r,g,b))
    mur_sprite.add(Mur(0,265,215,15,r,g,b))
    mur_sprite.add(Mur(0,390,215,15,r,g,b))
    mur_sprite.add(Mur(200,405,15,80,r,g,b))
    mur_sprite.add(Mur(0,470,215,15,r,g,b))
    mur_sprite.add(Mur(0,470,15,SCREEN_HEIGHT-433,r,g,b))

    #Bas de la map
    mur_sprite.add(Mur(0,SCREEN_HEIGHT-15,SCREEN_WIDTH,15,r,g,b))

    #Côté droit de la map
    mur_sprite.add(Mur(SCREEN_WIDTH-15,15,15,170,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-200,185,200,15,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-215,185,15,80,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-215,265,215,15,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-215,390,215,15,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-215,405,15,80,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-215,470,215,15,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-15,470,15,SCREEN_HEIGHT-433,r,g,b))


    #Interieur de la map, partie haute
    mur_sprite.add(Mur(88,88,100,15,r,g,b))
    mur_sprite.add(Mur(300,88,130,15,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-188,88,100,15,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-430,88,130,15,r,g,b))

    #Cage à AH
    mur_sprite.add(Mur(SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2-70,300,15,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2+70,300,15,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2-55,15,130,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH/2+135,SCREEN_HEIGHT/2-55,15,130,r,g,b))

    #Partie entre cage à AH et haut de la map
    mur_sprite.add(Mur(288,185,1,100,r,g,b))
    mur_sprite.add(Mur(288,235,150,1,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-287,185,1,100,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-437,235,150,1,r,g,b))

    #barres entre la cage à AH et les côtés de la map
    mur_sprite.add(Mur(288,400,1,100,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-287,400,1,100,r,g,b))

    #Partie interieure basse de la map
    mur_sprite.add(Mur(88,SCREEN_HEIGHT-103,300,15,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-388,SCREEN_HEIGHT-103,300,15,r,g,b))
    mur_sprite.add(Mur(288,SCREEN_HEIGHT-153,15,50,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-303,SCREEN_HEIGHT-153,15,50,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH/2-5,SCREEN_HEIGHT-178,10,90,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH/2-110,SCREEN_HEIGHT-193,220,15,r,g,b))
    mur_sprite.add(Mur(88,570,127,15,r,g,b))
    mur_sprite.add(Mur(SCREEN_WIDTH-215,570,127,15,r,g,b))


    ahBleu_sprite = pygame.sprite.RenderClear()
    ahBleu_sprite.add=(AhBleu())

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

            connection.Send({'action':'keys','keystrokes':keys})



            denis_sprite.update()
            ahBleu_sprite.update()
            denis_sprite.clear(screen,background)
            mur_sprite.draw(screen)
            denis_sprite.draw(screen)
            ahBleu_sprite.draw(screen)

            collision = False
            mur_collidex = 0
            mur_collidey = 0


        pygame.display.flip()
