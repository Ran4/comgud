#SCREEN_W = 1224
#SCREEN_H = 650
SCREEN_W = 980
SCREEN_H = 980
GRAVITY_X, GRAVITY_Y = 0, 200.0
START_IN_FULLSCREEN = False

BULLET_REMOVE_BORDER = 60 #remove bullets when they're this many pixels
                          #outside of a border
          
COLLISION_DIST = 35

#BG_COLOR = (255,255,255) #white
#BG_COLOR = (200,200,240) #light blue
BG_COLOR = (100,100,140)
#BLACK_HOLE_COLOR = (100,100,255)
BLACK_HOLE_COLOR = (0,0,42)
#BLACK_HOLE_SIZE = 16
BLACK_HOLE_SIZE = 64
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = GRAY = (128,128,128)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#BOTTOM_HEIGHT = 8
BOTTOM_HEIGHT = 0
STOP_BOUNCE_LIMIT = 160  #if we're going slower than this when bouncing,
                        #don't bounce: stop instead
BOUNCE_FACTOR_ON_FLOOR = -0.4

PLAYER_DRAG = 0.996
TOP_GLUE_START = 50
NUM_PLAYERS = 2
