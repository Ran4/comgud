import sys, os, random, math

import constants as con
import game as game
from libvector3 import Vector3
V3 = Vector3

class PhysicsObject(object):
    def __init__(self, m=50.0, pos=V3(), v=V3(), a=V3(), f=V3(),
            owner=None):
        self.m = m
        self.pos = V3()
        self.v = V3()
        self.a = V3()
        self.f = V3()
        self.owner = owner
        
        self.hp = 100
        self.maxHp = 100
        self.invulnerable = True
        
        self.gravityFactor = 1.0 #0.0 means don't apply gravity
    
    def updatePhysics(self, game):
        #self.f += game.gravity * self.gravityFactor * self.m
        middleOfScreen = V3(game.screenw/2.0, game.screenh/2.0)
        pullStrength = con.BLACK_HOLE_GRAVITY_STRENGTH * self.gravityFactor**2
        f = (middleOfScreen - self.pos) * pullStrength
        self.f += f
        
        #self.v += f * 1e-4 * (self.gravityFactor)**2
        if self.owner.id == 1:
            print "pullStrength:", pullStrength
        
        self.v += V3()
        
        self.a = self.f / self.m
        self.f = V3()
        self.v += self.a * game.dt
        self.pos += self.v * game.dt
        
        if self.owner and self.owner.id == 0 and False:
            print "f  :", self.f
            print "v  :", self.v
            print "a  :", self.a
            print "pos:", self.pos
