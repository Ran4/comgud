import sys, os, random, math

import pygame
from pygame.locals import *

import constants as con
import game as game
from libvector3 import Vector3
from physicsobject import PhysicsObject
V3 = Vector3


class Powerup(object):
    def __init__(self):
        #self.po = PhysicsObject(m=50.0, owner=self)
        self.po = PhysicsObject(m=5, owner=self)
        self.maxHp = 5
        self.hp = self.maxHp
        self.po.invulnerable = True
        self.id = None
        self.owner = None
        
        self.type = random.choice(["health", "gun"])
        
        self.isVisible = True
	self.ttl = None

        self.po.gravityFactor = 0.6
        
        self.markedForRemoval = False
        
    def respawn(self, game):
        if self.po:
            self.po.gravityFactor = con.GRAVITY_FACTOR_POWERUP_DEFAULT
            
            angle = 2*math.pi*random.random()
            ringRadius = 300
            spawnRadius = 200 + ringRadius * random.random()
            x = con.SCREEN_W/2.0 + spawnRadius * math.cos(angle)
            y = con.SCREEN_H/2.0 + spawnRadius * math.sin(angle)
            
            self.po.pos = V3(x,y)
            spawnVelocity = 120.0
            self.po.v = V3(spawnVelocity*math.sin(angle+math.pi/2.0),
                    spawnVelocity*math.cos(angle+math.pi/2.0))
            if random.random() > 0.5: self.po.v *= -1
            self.po.f = V3()
            self.po.a = V3()
            
            self.po.hp = self.po.maxHp
    
    def update(self, game, key):
        self.po.updatePhysics(game)
        pos = self.po.pos
        if pos.x < -con.BULLET_REMOVE_BORDER or \
                pos.x > game.screenw + con.BULLET_REMOVE_BORDER or \
                pos.y < -con.BULLET_REMOVE_BORDER or \
                pos.y > game.screenh + con.BULLET_REMOVE_BORDER or \
                (pos - V3(game.screenw/2.0, game.screenh/2.0)).len() < 48.0 or \
                self.ttl is not None and self.ttl <= 0:
            self.markedForRemoval = True
            return
        
        #Collision detection with players
        for player in game.players:
            if (self.po.pos - player.po.pos).len() < con.POWERUP_PICKUP_DIST:
                
                if self.type == "health":
                    player.po.gravityFactor = max(1.0, player.po.gravityFactor - 0.25)
                elif self.type == "gun":
                    player.TIME_BETWEEN_SHOTS = \
                            max(1, player.TIME_BETWEEN_SHOTS - 2)
                    
                self.markedForRemoval = True
                return
        
        if self.ttl is not None and self.ttl <= 0:
            self.markedForRemoval = True
        else:
            if self.ttl is not None:
                self.ttl -= 1
    
    def draw(self, game, surface, img, fnt):
        if not self.po or not self.isVisible:
            return
        
        x, y = self.po.pos.x, self.po.pos.y
            
        if self.type == "health" or self.type is None:
            surface.blit(img["powerup_health"],
                    dest=(x, y), area=None)
        if self.type == "gun":
            surface.blit(img["powerup_gun"],
                    dest=(x, y), area=None)
