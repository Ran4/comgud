import sys, os, random, math

import constants as con
from libvector3 import Vector3
V3 = Vector3
import player

class Game(object):
    def __init__(self):
        self.exit = False
        self.gameTime = 0
        self.gravity = V3(0.0, 98.2*0)
        
        self.dt = 1/60.
        
        self.players = []
        self.bullets = []
        
        self.players.append(player.Player())
        self.players[-1].po.pos = V3(400, 300)
        self.players[-1].id = 0
        
    def update(self, key):
        self.gameTime += 1
        self.dt = 1/60.
        
        for bullet in self.bullets:
            bullet.update(self, key)
            
        for player in self.players:
            player.update(self, key)
            
            
    def draw(self, surface, img, fnt):
        for player in self.players:
            player.draw(self, surface, img, fnt)
            
        for bullet in self.bullets:
            bullet.draw(self, surface, img, fnt)
