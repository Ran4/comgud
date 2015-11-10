import sys, os, random, math, copy

import pygame
from pygame.locals import *

import constants as con
import game as game
from libvector3 import Vector3
from physicsobject import PhysicsObject
from bullet import Bullet
V3 = Vector3

class Player(object):
    def __init__(self, game, id=None, favoriteFruit=None):
        #self.po = PhysicsObject(m=50.0, owner=self)
        self.po = PhysicsObject(m=50.0, owner=self)
        self.po.invulnerable = False
        self.id = id
        self.numGuns = 2
        self.livesLeft = con.NUM_PLAYER_LIVES
        
        self.favoriteFruit = favoriteFruit
        
        self.w = 30
        self.h = 40
        self.hw = self.w / 2
        self.hh = self.h / 2
        
        self.respawn(game)
        
    def respawn(self, game):
        #self.TIME_BETWEEN_SHOTS = 24
        self.TIME_BETWEEN_SHOTS = 20
        if self.favoriteFruit == "shotgun":
            self.TIME_BETWEEN_SHOTS = 42
        self.timeUntilNextShot = 0
        self.timeUntilNextShot2 = 0
        
        if self.po:
            self.po.gravityFactor = con.GRAVITY_FACTOR_PLAYER_DEFAULT
            
            angle = 2*math.pi*random.random()
            ringRadius = 50
            spawnRadius = max(game.blackHoleSize + 70, 200) \
                    + ringRadius * random.random()
            x = con.SCREEN_W/2.0 + spawnRadius * math.cos(angle)
            y = con.SCREEN_H/2.0 + spawnRadius * math.sin(angle)
            
            self.po.pos = V3(x,y)
            spawnVelocity = 300.0
            self.po.v = V3(spawnVelocity*math.sin(angle),
                    spawnVelocity*math.cos(angle))
            if random.random() > 0.5: self.po.v *= -1
            self.po.f = V3()
            self.po.a = V3()
            
            self.po.hp = self.po.maxHp

    def update(self, game, key):
        if self.po:
            self.po.updatePhysics(game)

	    if game.vectorToMiddle(self.po.pos + V3(self.hw, self.hh)).len() \
                    < game.blackHoleSize:
                self.respawn(game)
                self.livesLeft -= 1
                game.blackHoleSize += con.BLACK_HOLE_INCREASE_BY_PLAYER
                
            """
            #move player to other side if outside
            pos = self.po.pos
            if pos.x + self.w < 0:
                pos.x = game.screenw
            elif pos.x >= game.screenw:
                pos.x = 0 - self.w
            if pos.y + self.h < 0:
                pos.y = game.screenh
            elif pos.y >= game.screenh:
                pos.y = 0 - self.h
            """
            
            #bouncy walls
            pos = self.po.pos
            if pos.x < 0 and self.po.v.x < 0:
                self.po.v.x *= con.BOUNCE_FACTOR_ON_WALLS
            elif pos.x + self.w >= game.screenw and self.po.v.x > 0:
                self.po.v.x *= con.BOUNCE_FACTOR_ON_WALLS
            if pos.y < 0 and self.po.v.y < 0:
                self.po.v.y *= con.BOUNCE_FACTOR_ON_WALLS
            elif pos.y + self.h >= game.screenh and self.po.v.y > 0:
                self.po.v.y *= con.BOUNCE_FACTOR_ON_WALLS
                
            """
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
                    
                    
            """
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
                    
            elif self.id == 1: #player 2
                if gun == 0:
                    if key[K_UP]: up = 1.
                    if key[K_DOWN]: down = 1.
                    if key[K_LEFT]: left = 1.
                    if key[K_RIGHT]: right = 1.
                elif gun == 1:
                    if key[K_i]: up = 1.
                    if key[K_k]: down = 1.
                    if key[K_j]: left = 1.
                    if key[K_l]: right = 1.
            elif self.id == 2 and gun == 0:
                pass
                #if key[K_i]: up = 1.
                #if key[K_k]: down = 1.
                #if key[K_j]: left = 1.
                #if key[K_l]: right = 1.
            elif self.id == 3 and gun == 0:
                pass
                #if key[K_t]: up = 1.
                #if key[K_g]: down = 1.
                #if key[K_f]: left = 1.
                #if key[K_h]: right = 1.
            
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
                if self.favoriteFruit == "shotgun": #ugly special case
                    self.timeUntilNextShot2 += 20
                else:
                    self.timeUntilNextShot2 += self.TIME_BETWEEN_SHOTS
            
            if self.favoriteFruit == "shotgun" and gun != 1:
                for degree in range(-10, 10, 3):
                    a = math.radians(degree)
                    
                    b = Bullet()
                    b.po.pos = copy.copy(self.po.pos)
                    b.po.v = copy.copy(self.po.v) + (V3(dx, dy).rotate(a)) \
                            * b.BULLET_SPEED
                    b.owner = self.id
                    b.bulletType = self.favoriteFruit
                    game.bullets.append(b)
                    
                    vDiff = -0.3*(b.po.m * b.BULLET_SPEED) / self.po.m
                    self.po.v += V3(dx, dy) * vDiff
            else:
                b = Bullet()
                b.po.pos = copy.copy(self.po.pos)
                b.po.v = copy.copy(self.po.v) + V3(dx, dy) * b.BULLET_SPEED
                b.owner = self.id
                b.bulletType = self.favoriteFruit
                if gun == 1: #gun 1 is like jetpack...
                    #b.isVisisble = False
                    b.ttl = 1
                    r = 4.0
                    b.BULLET_SPEED *= -r
                    b.po.m /= r
                    
                game.bullets.append(b)
            
                #p = mv const.
                #p1 = p2 => m1 v1 = m2 v2 => v1 = (m2 v2) / m1
                #where 1 is the player, 2 is the bullet
                vDiff = -(b.po.m * b.BULLET_SPEED) / self.po.m
                self.po.v += V3(dx, dy) * vDiff
        
    def draw(self, game, surface, img, fnt):
        x, y = self.po.pos.x, self.po.pos.y
        
        area = getAreaFromId(self.id, self.w, self.h)
        surface.blit(img["players"], dest=(x, y), area=area)
        
        #draw text above head
        if self.po:
            percentText = "%d%%" % (100.0*(self.po.gravityFactor - 1.0))
        else:
            percentText = "NO BODY"
        percentTextSurface = fnt.render(percentText, False, con.FONT_COLOR)
        surface.blit(percentTextSurface,
                (self.po.pos.x+1, self.po.pos.y - 20))
        
#separate
def getAreaFromId(id, w, h):
    #id += 10
    
    if id <= 8:
        startX = id * w
        startY = 0
    elif id <= 14:
        startX = (id - 9) * w
        startY = 42
    elif id <= 22:
        startX = (id - 15) * w
        startY = 2*42
    else:
        startX = 0
        startY = 0
        
    return [startX, startY, w, h]

