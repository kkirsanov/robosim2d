import pygame
import numpy
from numpy import array


LEVEL = 20


class Enviroment:
    square_size = 0
    image = None
    map=None
    square_size = 0.0
    def __init__(self, pixelsW):
        self.len = pixelsW

    def Recalculate(self, Xcout):
        self.square_size = self.len / Xcout
        print "SqureSize = ", self.square_size

    def SetClear(self, h, w):
        self.Recalculate(h)
        self.map = []
        for x in xrange(w):
            self.map.append([False]*h)
        self.UpadeImage()
    def UpadeImage(self, newm=None):
        #self.image = None
        print self.square_size
        import time
        t=time.clock()
        print "Updating enviroment...",
        for y in xrange(len(self.map)):
            for x in xrange(len(self.map[y])):
                if self.image == None:
                    _x = len(self.map[y])
                    _y = len(self.map)
                    self.Recalculate(_x)
                    self.image = pygame.Surface((_x*self.square_size, _y*self.square_size))
                if self.map[y][x] > LEVEL:
                    color = (self.map[y][x], self.map[y][x], self.map[y][x])                    
                else:
                    color = (20, 20, 20)
                pygame.draw.rect(self.image, color, pygame.Rect(x * self.square_size, y * self.square_size, self.square_size, self.square_size))

        print "Done - ", time.clock()-t, 'sec.' 
    def LoadFromFile(self, fname):
        self.map = []
        print 'Loading "%s" with map: '%fname,
        f = open(fname)
        for line in f.readlines():
            l = []
            for val in line:
                if val == '\n': break
                if val == '\r': break
                if val == '*':
                    l.append(255)
                else:
                    l.append(0)
            self.map.append(l)
        self.UpadeImage()
        print "Done!"
    def paint(self, surface, x=0, y=0):
        """ Paint enviroment on Pygame surface      
        """
        surface.blit(self.image,(0,0))