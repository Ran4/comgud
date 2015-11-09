#!/bin/bash/python
import sys, os, random, math

import pygame
from pygame.locals import *

import constants as con
print "bef import game in MAIN"
from game import Game
print "after import game in MAIN"
def setScreen(game, toggle=False):
    if toggle:
        game.fullscreen = not game.fullscreen
    
    if game.fullscreen:
        return pygame.display.set_mode(game.screensize, FULLSCREEN)
    else:
        return pygame.display.set_mode(game.screensize)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Python+Pygame game")
    
    game = Game()
    screen = setScreen(game)
    pygame.mixer.init()
    
    try:
        #fnt = pygame.font.Font(None, 32) #font of size (=height) 32
        fnt = pygame.font.Font(None, 24) #font of size (=height) 32
        print "Loaded default font"
    except: #couldn't load default font, tries to load manually
        print "Couldn't load default font"
        fnt = pygame.font.SysFont("arial", 16)
        print "Loaded arial font"
    
    #load images, sounds and classes here
    img = loadImages()
    so = loadSounds()
    
    #############################
    ##Start of main loop        #
    while not game.exit:
        for event in pygame.event.get():
            if event.type == QUIT:
                game.exit = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    game.exit = True
                elif event.key == K_RETURN:
                    setScreen(game, toggle=True)
                elif event.key == K_r:
                    game.reset()
                elif event.key == K_F1:
                    print "fps: %s" % round(game.fps, 1)
        
        handleLogic(img, so, game)
        drawGame(screen, img, fnt, game)
        clock.tick(60)
        game.fps = clock.get_fps()
    #############################
    pygame.quit(); sys.exit()

def handleLogic(img, so, game):
    mpos = pygame.mouse.get_pos()
    mbut = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()
        
    game.update(key)
    
def drawGame(surface, img, fnt, game):
    surface.fill(game.bgColor)
    
    #Here goes drawing
    game.draw(surface, img, fnt)
    
    pygame.display.update()
    
def loadImages():
    opj = os.path.join
    imagenames = [
    ["players", opj("data","players","players.png")],
    ["strawberry", opj("data","bullets","strawberry.png")],
    ["banana", opj("data","bullets","banana.png")],
    ["powerup_health", opj("data","powerups","health.png")],
    ["powerup_gun", opj("data","powerups","gun.png")],
    ]
    img = {}
    for name in imagenames:
        try:
            img[name[0]] = pygame.image.load(name[1]).convert()
            img[name[0]].set_colorkey((255,0,255)) #pink
        except:
            print "Couldn't load",name[1],"\nExiting"
            sys.exit()
    return img
    
def loadSounds():
    opj = os.path.join
    soundnames = [
    #["toungeOut", opj("data","sounds","toungeout.wav")],
    ]
    so = {}
    for name in soundnames:
        try:
            so[name[0]] = pygame.mixer.Sound(name[1])
        except:
            print "Couldn't load",name[1],"\nExiting"
            sys.exit()
    return so

if __name__ == "__main__":
    main()
