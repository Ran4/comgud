import sys, os, random, math

import pygame
from pygame.locals import *

import constants as con
import game as game
from libvector3 import Vector3
from physicsObject import PhysicsObject
V3 = Vector3

class Bullet(object):
    def __init__(self):
        self.po = PhysicsObject(m=0.1, owner=self)
        self.po.invulnerable = True
        self.id = None
        self.BULLET_SPEED = 200.0
        self.owner = None
        
    def update(self, game, key):
        if self.po:
            self.po.updatePhysics(game)
            
        #self.updateControls(game, key)
            
    def draw(self, game, surface, img, fnt):
        if not self.po: #has no body, can't draw
            pass
        
        x, y = self.po.pos.x, self.po.pos.y
            
        surface.blit(img["strawberry"],
                dest=(x, y), area=None)
