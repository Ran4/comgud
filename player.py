import sys, os, random, math, copy

import pygame
from pygame.locals import *

import constants as con
import game as game
from libvector3 import Vector3
print "bef 'from physicsObject import PhysicsObject'"
from physicsobject import PhysicsObject
print "after 'from physicsObject import PhysicsObject'"
from bullet import Bullet
V3 = Vector3

class Player(object):
    def __init__(self):
        self.po = PhysicsObject(m=50.0, owner=self)
        self.po.invulnerable = False
        self.id = None
        self.numGuns = 2
        
        self.favoriteFruit = None
        
        self.w = 30
        self.h = 40
        
        self.TIME_BETWEEN_SHOTS = 8
        self.timeUntilNextShot = 0
        self.timeUntilNextShot2 = 0
        
    def update(self, game, key):
        if self.po:
            self.po.updatePhysics(game)
            
            pos = self.po.pos
            if pos.x < 0 and self.po.v.x < 0:
                self.po.v.x *= -0.9
            elif pos.x + self.w >= game.screenw and self.po.v.x > 0:
                self.po.v.x *= -0.9
                
            elif pos.y < con.TOP_GLUE_START and self.po.v.y < 5:
                if pos.y < 0:
                    self.po.v.y += 2.1
                    self.po.pos.y += 0.5
                self.po.v.y *= 0.6 + 0.2*max(0,pos.y)/float(con.TOP_GLUE_START)
            elif pos.y + self.h >= game.screenh - con.BOTTOM_HEIGHT \
                    and self.po.v.y > 0:
                
                #print "abs(self.po.v.y): ", abs(self.po.v.y)
                        
                if abs(self.po.v.y) < con.STOP_BOUNCE_LIMIT:
                    self.po.v.y = 0
                    pos.y = game.screenh - con.BOTTOM_HEIGHT - self.h
                else:
                    self.po.v.x *= 0.9
                    self.po.v.y *= -0.6
                    
                if pos.y + self.h >= game.screenh - con.BOTTOM_HEIGHT:
                    pos.y = game.screenh - con.BOTTOM_HEIGHT - self.h
                    self.po.v.x *= 0.7
                    
                    
            self.po.v *= con.PLAYER_DRAG
            
        self.updateControls(game, key)
    
    def updateControls(self, game, key):
        self.timeUntilNextShot = max(0, self.timeUntilNextShot-1)
        self.timeUntilNextShot2 = max(0, self.timeUntilNextShot2-1)
        
        #print self.timeUntilNextShot
        
        if not self.po:
            return
        
        for gun in range(self.numGuns):
            left, right, up, down = 0, 0, 0, 0
            if self.id == 0: #player 1
                if gun == 0:
                    if key[K_w]: up = 1.
                    if key[K_s]: down = 1.
                    if key[K_a]: left = 1.
                    if key[K_d]: right = 1.
                elif gun == 1:
                    if key[K_t]: up = 1.
                    if key[K_g]: down = 1.
                    if key[K_f]: left = 1.
                    if key[K_h]: right = 1.
                    
            if self.id == 1: #player 2
                if gun == 0:
                    if key[K_i]: up = 1.
                    if key[K_k]: down = 1.
                    if key[K_j]: left = 1.
                    if key[K_l]: right = 1.
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
            
            if gun == 0 and self.timeUntilNextShot > 0 \
                    or gun == 1 and self.timeUntilNextShot2 > 0:
                continue
            
            if gun == 0:
                self.timeUntilNextShot += self.TIME_BETWEEN_SHOTS
            elif gun == 1:
                self.timeUntilNextShot2 += self.TIME_BETWEEN_SHOTS
            
            b = Bullet()
            b.po.pos = copy.copy(self.po.pos)
            b.po.v = copy.copy(self.po.v) + V3(dx, dy) * b.BULLET_SPEED
            b.owner = self.id
            b.bulletType = self.favoriteFruit
            game.bullets.append(b)
            
            #p = mv const.
            #p1 = p2 => m1 v1 = m2 v2 => v1 = (m2 v2) / m1
            #where 1 is the player, 2 is the bullet
            vDiff = -(b.po.m * b.BULLET_SPEED) / self.po.m
            self.po.v += V3(dx, dy) * vDiff
        
    
    def draw(self, game, surface, img, fnt):
        if self.po:
            x, y = self.po.pos.x, self.po.pos.y
            
        if self.id == 0 or self.id == 1:
            area=(self.id*self.w,0, self.w, self.h)
        else:
            area=(0,0,  30, 40) #he-man
        
        surface.blit(img["players"],
                #dest=(x, y), area=None)
                dest=(x, y), area=area)
