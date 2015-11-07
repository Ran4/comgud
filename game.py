import sys, os, random, math

import pygame
from pygame.locals import *

import constants as con
from libvector3 import Vector3
V3 = Vector3
import player

class Game(object):
    def __init__(self):
        self.screensize = self.screenw, self.screenh = \
                con.SCREEN_W, con.SCREEN_H
        self.exit = False
        self.gameTime = 0
        self.gravity = V3(con.GRAVITY_X, con.GRAVITY_Y)
        
        self.bgColor = con.BG_COLOR
        self.fullscreen = con.START_IN_FULLSCREEN
        
        self.dt = 1/60.
        
        self.players = []
        self.bullets = []
        
        for i in range(con.NUM_PLAYERS):
            self.players.append(player.Player())
            
            spawnBorder = 50
            paneWidth = (con.SCREEN_W - spawnBorder) / (con.NUM_PLAYERS + 1.)
            x = (i+1)*paneWidth
            
            self.players[-1].po.pos = V3(x, 580)
            self.players[-1].id = i
            
            if i == 0:
                self.players[-1].favoriteFruit = "strawberry"
            elif i == 1:
                self.players[-1].favoriteFruit = "banana"
                
    def reset(self):
        for player in self.players:
            if player.po:
                player.po.hp = player.po.maxHp
        print "Game was reset!"
        
    def update(self, key):
        self.gameTime += 1
        self.dt = 1/60.
        
        for bullet in self.bullets:
            bullet.update(self, key)
        
        self.bullets = filter(lambda x: not x.markedForRemoval, self.bullets)
            
        for player in self.players:
            player.update(self, key)
            
    def draw(self, surface, img, fnt):
        for i in range(1,con.BOTTOM_HEIGHT+1):
            pygame.draw.line(surface, con.GREEN,
                    (0           , self.screenh-i),
                    (self.screenw, self.screenh-i))
        
        
        for bullet in self.bullets:
            bullet.draw(self, surface, img, fnt)
            
        for player in self.players:
            player.draw(self, surface, img, fnt)
