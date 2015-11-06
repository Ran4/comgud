import sys, os, random, math, copy

import pygame
from pygame.locals import *

import constants as con
import game as game
from libvector3 import Vector3
from physicsObject import PhysicsObject
from bullet import Bullet
V3 = Vector3

class Player(object):
    def __init__(self):
        self.po = PhysicsObject(m=50.0, owner=self)
        self.po.invulnerable = False
        self.id = None
        self.numGuns = 2
        
        self.TIME_BETWEEN_SHOTS = 5
        self.timeUntilNextShot = 0
        
    def update(self, game, key):
        if self.po:
            self.po.updatePhysics(game)
            
        self.updateControls(game, key)
    
    def updateControls(self, game, key):
        self.timeUntilNextShot = max(0, self.timeUntilNextShot-1)
        
        print self.timeUntilNextShot
        
        if not self.po:
            return
        
        for gun in range(self.numGuns):
            left, right, up, down = 0, 0, 0, 0
            if self.id == 0:
                if gun == 0:
                    if key[K_w]: up = 1.
                    if key[K_s]: down = 1.
                    if key[K_a]: left = 1.
                    if key[K_d]: right = 1.
                elif gun == 1:
                    if key[K_UP]: up = 1.
                    if key[K_DOWN]: down = 1.
                    if key[K_LEFT]: left = 1.
                    if key[K_RIGHT]: right = 1.
            
            if left and right:
                left, right = 0, 0
            if up and down:
                up, down = 0, 0

            numHeld = float(left+right+up+down)
            if numHeld < 1:
                continue
            
            if numHeld > 1:
                s = numHeld**0.5
                left /= s
                right /= s
                up /= s
                down /= s
                
            dx, dy = right - left, down - up
            
            if self.timeUntilNextShot > 0:
                print "CANT"
                continue
            
            self.timeUntilNextShot += self.TIME_BETWEEN_SHOTS
            print "yeah more"
            
            b = Bullet()
            b.po.pos = copy.copy(self.po.pos)
            b.po.v = copy.copy(self.po.v) + V3(dx, dy) * b.BULLET_SPEED
            b.owner = self.id
            game.bullets.append(b)
            
            #p = mv const.
            #p1 = p2 => m1 v1 = m2 v2 => v1 = (m2 v2) / m1
            #where 1 is the player, 2 is the bullet
            vDiff = -(b.po.m * b.BULLET_SPEED) / self.po.m
            self.po.v += V3(dx, dy) * vDiff
        
    
    def draw(self, game, surface, img, fnt):
        if self.po:
            x, y = self.po.pos.x, self.po.pos.y
        
        surface.blit(img["players"],
                #dest=(x, y), area=None)
                dest=(x, y), area=(0,0, 30, 40))
