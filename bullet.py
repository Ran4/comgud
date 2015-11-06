import sys, os, random, math

import pygame
from pygame.locals import *

import constants as con
import game as game
from libvector3 import Vector3
from physicsobject import PhysicsObject
V3 = Vector3

class Bullet(object):
    def __init__(self):
        self.po = PhysicsObject(m=2.7, owner=self)
        self.po.invulnerable = True
        self.id = None
        self.bulletType = None
        self.BULLET_SPEED = 900.0
        self.owner = None
        
        self.markedForRemoval = False
        
    def update(self, game, key):
        if self.po:
            self.po.updatePhysics(game)
            pos = self.po.pos
            if pos.x < -con.BULLET_REMOVE_BORDER or \
                    pos.x > game.screenw + con.BULLET_REMOVE_BORDER or \
                    pos.y < -con.BULLET_REMOVE_BORDER or \
                    pos.y > game.screenh + con.BULLET_REMOVE_BORDER:
                self.markedForRemoval = True
            
        #self.updateControls(game, key)
            
    def draw(self, game, surface, img, fnt):
        if not self.po: #has no body, can't draw
            pass
        
        x, y = self.po.pos.x, self.po.pos.y
            
        if self.bulletType == "strawberry" or self.bulletType is None:
            surface.blit(img["strawberry"],
                    dest=(x, y), area=None)
        elif self.bulletType == "banana":
            surface.blit(img["banana"],
                    dest=(x, y), area=None)
