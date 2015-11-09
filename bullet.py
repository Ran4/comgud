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
        #self.po = PhysicsObject(m=2.7, owner=self)
        self.po = PhysicsObject(m=1.7, owner=self)
        self.po.invulnerable = True
        self.id = None
        self.bulletType = None
        self.damage = 1
        #self.BULLET_SPEED = 900.0
        #self.BULLET_SPEED = 600.0
        self.BULLET_SPEED = 700.0
        self.owner = None
	self.isVisisble = True
	#self.ttl = None
	self.ttl = 120

        #self.po.gravityFactor = 5.0
        #self.po.gravityFactor = 0.0
        self.po.gravityFactor = 0.2
        
        self.markedForRemoval = False
        
    def update(self, game, key):
        if self.po:
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
                if self.owner != player.id and player.po and \
                        (self.po.pos-player.po.pos).len() < con.COLLISION_DIST:
                    #print "player %s was hit!" % player.id
                    
                    if player.id == 1: #HANDICAP FOR P2
                        #player.po.hp -= self.damage / 2.0
                        player.po.hp -= self.damage
                    else:
                        player.po.hp -= self.damage
                        
                    #p=mv => m1 v1 = m2 v2 => v1 = m2 v2 / v1
                    vDiff = (self.po.m * self.BULLET_SPEED) / player.po.m
                    player.po.v += self.po.v.normalize() * vDiff
                    #player.po.gravityFactor += con.GRAVITY_FACTOR_PLAYER_INCREASE_PER_HIT
                    player.po.gravityFactor += self.damage/100.0
                    #check for player dying
                    if player.po.hp <= 11.0: #random value since we're not
                                                #drawing from the top
                        player.po.hp = player.po.maxHp
                        print "player with id=%s died!" % player.id
                        
                    self.markedForRemoval = True
                    return

            if self.ttl is not None:
                self.ttl -= 1
            
        #self.updateControls(game, key)
            
    def draw(self, game, surface, img, fnt):
        if not self.po or not self.isVisisble: #has no body, can't draw
            return
        
        x, y = self.po.pos.x, self.po.pos.y
            
        if self.bulletType == "strawberry" or self.bulletType is None:
            surface.blit(img["strawberry"],
                    dest=(x, y), area=None)
        elif self.bulletType == "banana":
            surface.blit(img["banana"],
                    dest=(x, y), area=None)
