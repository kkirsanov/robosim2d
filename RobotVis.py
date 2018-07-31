# coding=cp1251
import math
import pygame
import RobotSim
class RobotVis:
    """
    RobotSize
    500 d;inna
    400 shirina
    12 shinki - lj cthtlbyy
    50 - koleso
    
    R kolesa = 8
    170 для гусенечногоы
    
    между осями - 250
    850 Длинна гусенец
    """
    robot = None
    points = []
    sensorPoints = []

    def __init__(self, robot, mPerPixel=0.01):
        self.mPerPixel = mPerPixel
        self.robot = robot

        self.points.append([ - 0.2, 0.5])
        self.points.append([0.2, 0.5])
        self.points.append([0.2, 0.16])
        self.points.append([0.25, 0.16])
        self.points.append([0.25, 0.0])
        self.points.append([ - 0.25, 0.0])
        self.points.append([ - 0.25, 0.16])
        self.points.append([ - 0.2, 0.16])
        self.points.append([ - 0.2, 0.5])
        self.points = [[x, y - 0.08] for x, y in self.points]

    def paint(self, screen):

        points = [RobotSim.rotate([p[0], p[1]], self.robot.phi) for p in self.points]
        points = [[x + self.robot.X[0], y + self.robot.X[1]] for x, y in points]
        points = [[x * (1 / self.mPerPixel), y * (1 / self.mPerPixel)] for x, y in points]        
        pygame.draw.polygon(screen, (150, 150, 150), points, 4)

        points = [RobotSim.rotate([p[0], p[1]], self.robot.phi) for p in self.robot.sensorPoints]
        points = [[x + self.robot.X[0], y + self.robot.X[1]] for x, y in points]
        points = [[x * (1 / self.mPerPixel), y * (1 / self.mPerPixel)] for x, y in points]

        pygame.draw.circle(screen, (255, 100, 100), map(int, points[0]), 4)

        i = 0;
        points = [[x * (1 / self.mPerPixel), y * (1 / self.mPerPixel)] for x, y in self.robot.sensorset]
        
        for p in points:
            i = i + 1
            if i > 255: i = 255
            if i < 0: i = 0
            pygame.draw.circle(screen, (255 - i, i, 0), map(int, p), 2)
