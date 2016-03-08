import numpy as np
import random as r
import pygame as pg
import sys

class lgs:
    """Lattice Gas Simulation - A 2D Implementation"""
    #Simulation parameters
    SIZE_X = 128
    SIZE_Y = 128
    SUBGRIDSIZE = 4
    MAX_P = float(SUBGRIDSIZE*SUBGRIDSIZE*4)
    DENSITY = 0.10
    # V_Dist holds the velocity distribution of the particles.
    V_DIST  = np.zeros(3, dtype=np.float )
    V_DIST  = [0.25, 0.25, 0.25, 0.25]
    #Pygame parameters
    SCALE = 15
    SIZE_PX = width, height = SIZE_X*SCALE/SUBGRIDSIZE, SIZE_Y*SCALE/SUBGRIDSIZE
    WHITE = 255,255,255

    ############################## Main Methods ################################
    def __init__(self):
        self.lattice = [np.zeros((lgs.SIZE_Y, lgs.SIZE_X), dtype=np.byte),
                        np.zeros((lgs.SIZE_Y, lgs.SIZE_X), dtype=np.byte)]
        self.lat = 0    # I alternate which of the lattice arrays i use as a
                        # buffer, and which as the current state.
                        # This tracks which is the current state.
        self.init_lattice()
        self.screen = pg.display.set_mode( lgs.SIZE_PX )
        pg.display.set_caption( "Lattice Gas")

    def run(self):
        print "Space to Pause, 'A' to create a dense region"
        pause = False
        while( True ):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == 32: # Space
                    pause = not pause
                    if pause: print "Paused"
                    else: print "Unpaused"
                if event.type == pg.KEYDOWN and event.key == 97: # A Key
                    self.addSquare()
                    print "Added Dense Region"
            if not pause:
                self.draw()
                self.update()

    ### Support Methods #########################
    def init_lattice(self):
        n = 0
        for y in range(lgs.SIZE_Y):
            for x in range(lgs.SIZE_X):
                for d in range(3):  # Looping over direction states.
                    if r.random() < lgs.DENSITY:
                        n += 1
                        self.lattice[0][y][x] += pow( 2, d )
        print("Created "+str(n)+" particles out of "+str(4*lgs.SIZE_X*lgs.SIZE_Y))
        print("Expecting around "+str(4*lgs.SIZE_X*lgs.SIZE_Y*lgs.DENSITY))

    def addSquare(self):
        #calculate the size
        SSIZE = 0.15
        l = int(0.5*(lgs.SIZE_X - SSIZE*lgs.SIZE_X))
        for x in range( l, l+int(SSIZE*lgs.SIZE_X) ):
            for y in range( l, l+int(SSIZE*lgs.SIZE_X) ):
                self.lattice[0][y][x] = 15
                self.lattice[1][y][x] = 15

    def update(self):
        self.propagate()
        self.lat = (self.lat+1)%2
        self.resolveCollisions()

    def draw(self):
        cy = 0
        for ly in range(0, lgs.SIZE_Y, lgs.SUBGRIDSIZE):
            cx = 0
            for lx in range(0, lgs.SIZE_X, lgs.SUBGRIDSIZE):
                cellsum = 0
                for y in range(lgs.SUBGRIDSIZE):
                    for x in range(lgs.SUBGRIDSIZE):
                        cellsum += bin(self.lattice[self.lat][ly+y][lx+x]).count("1")
                c = int(255.0*(1 - (float(cellsum)/lgs.MAX_P)))
                color = c, c, c
                rect = pg.Rect( cx*lgs.SCALE, cy*lgs.SCALE, lgs.SCALE, lgs.SCALE )
                self.screen.fill(color, rect)
                cx += 1
            cy += 1
        pg.display.flip()

    def propagate(self):
        for y in range(lgs.SIZE_Y):
            for x in range(lgs.SIZE_X):
                n = self.lattice[self.lat][y][x]
                if nthBit(n, 0):   #Up
                    self.setBufferBit( y-1, x, 0, 1 )
                if nthBit(n, 1):   #Right
                    self.setBufferBit( y, x+1, 1, 1 )
                if nthBit(n, 2):   #Down
                    self.setBufferBit( y+1, x, 2, 1 )
                if nthBit(n, 3):   #Left
                    self.setBufferBit( y, x-1, 3, 1 )
                self.lattice[self.lat][y][x] = 0

    def resolveCollisions(self):
        for y in range(lgs.SIZE_Y):
            for x in range(lgs.SIZE_X):
                n = self.lattice[self.lat][y][x]
                if n == 10:
                    self.lattice[self.lat][y][x] = 5
                elif n == 5:
                    self.lattice[self.lat][y][x] = 10

    # Sets the bit of the buffer array
    def setBufferBit(self, y, x, n, v):
        y %= lgs.SIZE_Y
        x %= lgs.SIZE_X
        lat = (self.lat + 1) % 2    # Mod to get the buffer array (the on thats not current)
        num = self.lattice[lat][y][x]
        self.lattice[lat][y][x] ^= (-v ^ num) & (1 << n)


def nthBit( i, n ):
    mask = [1, 2, 4, 8]
    return ( i & mask[n] ) != 0