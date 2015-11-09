import sys, os, random, math

import pygame
from pygame.locals import *

import constants as con
from libvector3 import Vector3
V3 = Vector3
import player
from powerup import Powerup

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
        self.powerups = []
        
        for i in range(con.NUM_PLAYERS):
            self.players.append(player.Player())
            
            spawnBorder = 50
            paneWidth = (con.SCREEN_W - spawnBorder) / (con.NUM_PLAYERS + 1.)
            x = (i+1)*paneWidth
            
            self.players[-1].po.pos = V3(x, 580)
            self.players[-1].id = i
            startVY = 300*(1 if x < self.screenw/2.0 else -1)
            self.players[-1].po.v = V3(0.0, startVY)
            
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
        
        if self.gameTime > 1 and self.gameTime % con.POWERUP_SPAWN_DELAY == 0:
            p = Powerup()
            p.respawn()
            self.powerups.append(p)
        
        for powerup in self.powerups:
            powerup.update(self, key)
        
        for bullet in self.bullets:
            bullet.update(self, key)
        
        self.bullets = filter(lambda x: not x.markedForRemoval, self.bullets)
        self.powerups = filter(lambda x: not x.markedForRemoval, self.powerups)
            
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
            
        for powerup in self.powerups:
            powerup.draw(self, surface, img, fnt)

        pygame.draw.circle(surface, con.BLACK_HOLE_COLOR, (self.screenw/2, self.screenh/2),
            con.BLACK_HOLE_SIZE, 0)
        
        #draw text
        percentText = ", ".join(["p%s: %s %%" % \
                (player.id + 1, 100*(player.po.gravityFactor - 1.0))
                for player in self.players])
        percentTextSurface = fnt.render(percentText, False, con.FONT_COLOR)
        surface.blit(percentTextSurface, (5,self.screenh - 40))

    def vectorToMiddle(self, otherVec):
        return V3(self.screenw/2.0, self.screenh/2.0) - otherVec
