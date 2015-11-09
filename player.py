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
    def __init__(self, id=None):
        self.po = PhysicsObject(m=50.0, owner=self)
        self.po.invulnerable = False
        self.id = id
        self.numGuns = 2
        
        self.favoriteFruit = None
        
        self.w = 30
        self.h = 40
        self.hw = self.w / 2
        self.hh = self.h / 2
        
        self.respawn()
        
    def respawn(self):
        self.TIME_BETWEEN_SHOTS = 8
        self.timeUntilNextShot = 0
        self.timeUntilNextShot2 = 0
        
        if self.po:
            self.po.gravityFactor = con.GRAVITY_FACTOR_PLAYER_DEFAULT
            
            angle = 2*math.pi*random.random()
            ringRadius = 300
            spawnRadius = 200 + ringRadius * random.random()
            x = con.SCREEN_W/2.0 + spawnRadius * math.cos(angle)
            y = con.SCREEN_H/2.0 + spawnRadius * math.sin(angle)
            
            self.po.pos = V3(x,y)
            spawnVelocity = 200.0
            self.po.v = V3(spawnVelocity*math.sin(angle+math.pi/2.0),
                    spawnVelocity*math.cos(angle+math.pi/2.0))
            if random.random() > 0.5: self.po.v *= -1
            self.po.f = V3()
            self.po.a = V3()
            
            self.po.hp = self.po.maxHp

    def randomPosition(self):
        if self.po:
            self.po.pos.x = float(random.randint(0, con.SCREEN_W))
            self.po.pos.y = float(random.randint(0, con.SCREEN_H))
        
    def update(self, game, key):
        if self.po:
            self.po.updatePhysics(game)

	    if game.vectorToMiddle(self.po.pos + V3(self.hw, self.hh)).len() \
                    < con.BLACK_HOLE_SIZE:
                self.respawn()
            
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
                    self.po.v.y *= con.BOUNCE_FACTOR_ON_FLOOR

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
        
        #shooting
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
            
            if gun == 0:
                #b.isVisisble = False
                b.ttl = 4
                r = 4.0
                b.BULLET_SPEED *= r
                b.po.m /= r

            game.bullets.append(b)
            
            #p = mv const.
            #p1 = p2 => m1 v1 = m2 v2 => v1 = (m2 v2) / m1
            #where 1 is the player, 2 is the bullet
            vDiff = -(b.po.m * b.BULLET_SPEED) / self.po.m
            self.po.v += V3(dx, dy) * vDiff
        
    
    def draw(self, game, surface, img, fnt):
        if self.po:
            x, y = self.po.pos.x, self.po.pos.y
            #height = self.h * max(0, self.po.hp) / self.po.maxHp
            height = self.h
        else:
            height = self.h
        
        if self.id == 0 or self.id == 1:
            area=(self.id*self.w,0, self.w, height)
        else:
            area=(0,0,  30, 40) #he-man
        
        surface.blit(img["players"],
                #dest=(x, y), area=None)
                dest=(x, y), area=area)
        
        #draw text above head
        if self.po:
            percentText = "%d%%" % (100.0*(self.po.gravityFactor - 1.0))
        else:
            percentText = "NO BODY"
        percentTextSurface = fnt.render(percentText, False, con.FONT_COLOR)
        surface.blit(percentTextSurface,
                (self.po.pos.x+1, self.po.pos.y - 20))
