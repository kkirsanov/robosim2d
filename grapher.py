import pygame
import time

class Grapher:
    data = []

    gr = pygame.Surface((100, 20))
    scale = 1.0
    paintClock = 0.0
    sizeX = 800
    sizeY = 200
    maxval = 0
    def __init__(self, sizeX=800, sizeY=200):
        self.sizeX = int(sizeX)
        self.sizeY = int(sizeY)
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont("Courier-new", 15)
    def Paint(self, surface, Y=400, invert = False):
        if invert:
            surface.blit(self.gr, (0, Y), None, pygame.BLEND_SUB)
        else:
            surface.blit(self.gr, (0, Y))
    def AddData(self, x):
        self.data.append(x)
        if x>self.maxval:
            self.maxval = x

        if len(self.data) > self.sizeX:
            self.data = self.data[ - self.sizeX:]
        
        if self.paintClock + 0.1 < time.clock():
            self.gr = pygame.Surface((self.sizeX, self.sizeY))
            self.paintClock = time.clock()

            counter = 0
            for y in self.data:
                counter = counter + 1
                z = (y / self.maxval)*self.sizeY                
                self.gr.set_at((int(counter), int(self.sizeY - z)), (255, 255, 255))
            
            self.gr.blit(self.myfont.render("%f m"%self.maxval, 1, (0, 255, 0)), (0, 0))
            pygame.draw.line(self.gr, (0, 255, 0), (0, 1), (self.sizeX, 1))
            
            v = self.maxval/2.0
            
            self.gr.blit(self.myfont.render("%f m"%v, 1, (255, 255, 0)), (0, self.sizeY/2))
            pygame.draw.line(self.gr, (255, 255, 0), (0, self.sizeY/2), (self.sizeX, self.sizeY/2))
            
            self.gr.blit(self.myfont.render("0.0m ", 1, (255, 255, 0)), (0, self.sizeY-1))
            pygame.draw.line(self.gr, (255, 255, 0), (0, self.sizeY-1), (self.sizeX, self.sizeY-1))
