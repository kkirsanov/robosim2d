from copy import copy
from math import sin, cos, sqrt, atan, pi
#from numpy import array
from numpy import arange

import time

LEVEL = 40

def rotate (vector2d, angle):
    v = vector2d
    _cos = cos(angle)
    _sin = sin(angle)
    return [v[0] * _cos - v[1] * _sin, v[1] * _cos + v[0] * _sin]

def rotateAround(center, vector2d, angle):
    v = [0.0, 0.0]
    v[0] = vector2d[0] - center[0]
    v[1] = vector2d[1] - center[1]
    v = rotate(v, angle)
    v[0] = v[0] + center[0]
    v[1] = v[1] + center[1]
    return v

def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

class RobotSim:
    dT = 0.1
    timeUpdate = 0.0
    pixelToMeter = 10.0
    maxLen = 2.55
    U = [0.0, 0.0]
    X = [0.0, 0.0]
    V = [0.0, 0.0]
    vMax = 0.34
    maxU = 64.0
    k1 = 0.15
    phi = 0.0
    vX = []
    vY = []

    mPerPixel = 0.01
    sensorPoints = []
    scanRange = 2.0
    def __init__(self, mPerPixel=0.01):
        self.mPerPixel = mPerPixel
        self.X = [3.0, 3.0] #start position
        self.timeUpdate = time.clock()
        print "Robot simulation Started"
        self.sensorPoints.append([0.0, 0.3])
        #self.sensorPoints.append([0.0, (1.15 + self.scanRange)])

    def Au(self, U, X=(0, 0)):
        def g(x):
            if int(x) > self.maxU:return self.maxU
            if int(x) < -self.maxU: return - self.maxU
            return int(x)

        self.U = map(g, U)
        return self.U

    def Vr (self, U):
        self.V[0] = 0
        self.V[1] = 0

        if U[0] > self.maxU / 4.0:
            self.V[0] = self.vMax
        if U[0] < -self.maxU / 4.0:
            self.V[0] = -self.vMax
        if U[1] > self.maxU / 4.0:
            self.V[1] = self.vMax
        if U[1] < -self.maxU / 4.0:
            self.V[1] = -self.vMax

        x = self.X[0]
        y = self.X[1]

        p1 = [x - 0.2, y - 0.2]
        p2 = [x + 0.2, y - 0.2]

        #rotate whels
        p1 = rotateAround([x, y], p1, self.phi)
        p2 = rotateAround([x, y], p2, self.phi)

        alpha = atan((self.V[1] - self.V[0]) / dist(p1, p2))

        V1 = rotate([0, self.V[0]], self.phi)
        V2 = rotate([0, self.V[1]], self.phi)

        p1 = [p1[0] + V1[0] * self.dT, p1[1] + V1[1] * self.dT]
        p2 = [p2[0] + V1[0] * self.dT, p2[1] + V2[1] * self.dT]

        self.phi = self.phi - alpha * self.dT

        #move along phi
        X = [0, (self.V[0] + self.V[1]) * self.dT]
        X = rotate(X, self.phi)

        self.X[0] = X[0] + self.X[0]
        self.X[1] = X[1] + self.X[1]

    def Vs(self, enviroment, env2):
        S = self.maxLen
        self.sensorset = []
        #raytrace

        for scanlen in arange(0.1, self.maxLen, 0.15):
            p = copy(self.sensorPoints[0])
            p[1] = p[1] + scanlen

            scanAngle = (pi / 180.0) * 45
            for angle in arange(-scanAngle / 2.0, scanAngle / 2.0, 0.15):
                P = rotateAround(self.sensorPoints[0], p, angle)
                P[0] = P[0] + self.X[0]
                P[1] = P[1] + self.X[1]
                P = rotateAround(self.X, P, self.phi)
                self.sensorset.append(P)
                #cross with enviroment

                p1 = int(P[0] / (enviroment.square_size * self.mPerPixel))
                p2 = int (P[1] / (enviroment.square_size * self.mPerPixel))

                if p2 < 0:p2 = 0
                if p1 < 0:p1 = 0
                if p2 > len(enviroment.map) - 1:p2 = len(enviroment.map) - 1
                if p1 > len(enviroment.map[0]) - 1:p1 = len(enviroment.map[0]) - 1
                if enviroment.map[p2][p1] > LEVEL:
                    if env2.map[p2][p1] < LEVEL:
                        env2.map[p2][p1] == 255

                        #MakeTrueEachAngle
                        ########################################
                        for angle in arange(-scanAngle / 2.0, scanAngle / 2.0, 0.05):
                            P = rotateAround(self.sensorPoints[0], p, angle)
                            P[0] = P[0] + self.X[0]
                            P[1] = P[1] + self.X[1]
                            P = rotateAround(self.X, P, self.phi)
                            self.sensorset.append(P)
                            #cross with enviroment

                            p1 = int(P[0] / (enviroment.square_size * self.mPerPixel))
                            p2 = int (P[1] / (enviroment.square_size * self.mPerPixel))
                            try:
                                env2.map[p2][p1] = 255 - abs(angle) * 300
                                if env2.map[p2][p1] < 0:
                                    env2.map[p2][p1] = 0

                            except:
                                pass
                        ########################################

                        #paint optimisation
                        #do not repaint, untill 1 second pass
                        if self.timeUpdate + 0.3 < time.clock():
                            env2.UpadeImage()
                            self.timeUpdate = time.clock()
                    S = scanlen
                    break;
                else:
                    try:
                        env2.map[p2][p1] -= 30
                        if env2.map[p2][p1] < 0:
                            env2.map[p2][p1] = 0

                    except:
                        pass

            if S < self.maxLen: break
        return S
    def As(self, sensors):
        if sensors < 1:
            return [ -self.maxU, self.maxU]
        return [self.maxU, self.maxU]

#import borbot

class RobotReal:
    dT = 0.1
    timeUpdate = 0.0
    pixelToMeter = 10.0
    maxLen = 2.55
    U = [0.0, 0.0]
    X = [0.0, 0.0]
    V = [0.0, 0.0]
    vMax = 0.34
    maxU = 128.0
    k1 = 0.15
    phi = 0.0
    vX = []
    vY = []

    mPerPixel = 0.01
    sensorPoints = []
    sensorset = []
    scanRange = 4.0

    def __init__(self):

        #self.eng = rpyc.connect_by_servicr("ENGINE")
        #self.od = rpyc.connect_by_servicr("ODOMETRY")
        #self.us = rpyc.connect_by_servicr("USENSOR")

        self.X = [3.0, 3.0] #start position
        self.timeUpdate = time.clock()
        self.sensorPoints.append([0.0, 0.3])
    def Au(self, U, X=(0, 0)):
        def g(x):
            if int(x) > self.maxU:return self.maxU
            if int(x) < -self.maxU: return - self.maxU
            return int(x)

        self.U = map(g, U)

        #self.eng.root.SetASpeed(int(self.U[0]))
        #self.eng.root.SetBSpeed(int(self.U[1]))
        return self.U

    def Vr (self, U):
        self.V[0] = 0
        self.V[1] = 0

        if U[0] > self.maxU / 4.0:
            self.V[0] = self.vMax
        if U[0] < -self.maxU / 4.0:
            self.V[0] = -self.vMax
        if U[1] > self.maxU / 4.0:
            self.V[1] = self.vMax
        if U[1] < -self.maxU / 4.0:
            self.V[1] = -self.vMax

        x = self.X[0]
        y = self.X[1]

        p1 = [x - 0.2, y - 0.2]
        p2 = [x + 0.2, y - 0.2]

        #rotate whels
        p1 = rotateAround([x, y], p1, self.phi)
        p2 = rotateAround([x, y], p2, self.phi)

        alpha = atan((self.V[1] - self.V[0]) / dist(p1, p2))

        V1 = rotate([0, self.V[0]], self.phi)
        V2 = rotate([0, self.V[1]], self.phi)

        p1 = [p1[0] + V1[0] * self.dT, p1[1] + V1[1] * self.dT]
        p2 = [p2[0] + V1[0] * self.dT, p2[1] + V2[1] * self.dT]

        self.phi = self.phi - alpha * self.dT

        #move along phi
        X = [0, (self.V[0] + self.V[1]) * self.dT]
        X = rotate(X, self.phi)

        self.X[0] = X[0] + self.X[0]
        self.X[1] = X[1] + self.X[1]

        if self.X[0] < 0 or self.X[0] > 6:
            self.X[0] = 3
        if self.X[1] < 0 or self.X[1] > 6:
            self.X[1] = 3


    def Vs(self, enviroment, env2):
        try:
            z = self.us.root.GetLeft()[0][1]
            z = z / 100.0
            if z > self.scanRange * 10:
                print "Error in US Sensor"
                return self.scanRange

            self.sensorset = []
            for scanlen in arange(0.1, self.scanRange, 0.15):
                p = copy(self.sensorPoints[0])
                p[1] = p[1] + scanlen
                if scanlen >= z:
                    break

                scanAngle = (pi / 180.0) * 45
                for angle in arange(-scanAngle / 2.0, scanAngle / 2.0, 0.15):
                    P = rotateAround(self.sensorPoints[0], p, angle)
                    P[0] = P[0] + self.X[0]
                    P[1] = P[1] + self.X[1]
                    P = rotateAround(self.X, P, self.phi)
                    self.sensorset.append(P)

            return z
        except:
            return 0.01

    def As(self, sensors):
        if sensors < 1:
            return [ -self.maxU, self.maxU]
        return [self.maxU, self.maxU]
