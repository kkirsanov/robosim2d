#coding=cp1251
import Enviroment
import pygame
import time
import RobotVis
import grapher
import RobotSim

#import cProfile



def RunRobotSim(scale=0.5, dt=0.1, invert=False):
    counter = 0
    decTime = time.time()
    pygame.init()

    print "Screen: ", pygame.display.get_driver()

    mPerPixel = 0.01 / scale

    sizeX = int(1600 * scale)
    sizeY = int(800 * scale)

    screen = pygame.display.set_mode((sizeX, sizeY))

    disp = pygame.Surface((sizeX / 2, sizeY))
    disp2 = pygame.Surface((sizeX / 2, sizeY))

    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option("-a", default="", dest="ip", help="addres of robot", metavar="IP")
    parser.add_option("-c", default="auto", dest="acontrol", help="Automatic Control", metavar="CONTROL")

    options, args = parser.parse_args()

    ip = options.ip
    acontrol = options.acontrol
    #acontrol="auto"
    engine = None
    if ip:
        import rpyc
        engine = rpyc.connect_by_service("engine", ip)
        print "Connectted to service!"

    run = True

    robotV = RobotVis.RobotVis(RobotSim.RobotSim(mPerPixel), mPerPixel)
    #robotShaddow = RobotVis.RobotVis(RobotSim.RobotReal('192.168.0.203', 13500))

    activeU = [robotV.robot.maxU, robotV.robot.maxU]

    enviroment = Enviroment.Enviroment(sizeX / 2)
    enviroment2 = Enviroment.Enviroment(sizeX / 2)

    enviroment.LoadFromFile('map.txt')
    robotV.enviroment = enviroment

    enviroment2.SetClear(80, 60)
    graph = grapher.Grapher(sizeX, sizeY / 4)

    robotV.robot.dT = dt
    joy = None
    pygame.joystick.init()
    try:
        joy = pygame.joystick.Joystick(0)
        joy.init()
    except:
        pass

    timeControl = time.time()

#TODO:Fix
    while run:
        time.sleep(0.02)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
        #main cycle

        U = robotV.robot.Au(activeU)
        X = robotV.robot.Vr(U)
        S = robotV.robot.Vs(enviroment, enviroment2)

        activeU = [0, 0]
        if engine:
            activeU = [0, 0]
            #commands = engine.root.Get(5)
        else:
            try:
                #print [joy.get_axis(0) * 64, -joy.get_axis(1) * 64]
                #print joy.get_axis(0), joy.get_axis(1)
                x = joy.get_axis(0) * 60
                y = -joy.get_axis(1) * 60

                activeU = [y + x / 2, y - x / 2]
                if activeU == [0.0, 0.0]:
                    raise Exception()
                timeControl = time.time()
            #ret[0] = round(joy.get_axis(0))
            #ret[1] = round(joy.get_axis(1))
            except:
                pass
            if timeControl + 2 < time.time():
                if acontrol == "auto":
                    activeU = robotV.robot.As(S)
        #print activeU
        #paint sensor response
        graph.AddData(S)
        #paint robot
        enviroment.paint(disp)
        enviroment2.paint(disp2)
        if decTime + 2 < time.time():
            decTime = time.time()
            print decTime
            for i, x in enumerate(enviroment2.map):
                for j, y in enumerate(x):
                    enviroment2.map[i][j] -= 8
                    if enviroment2.map[i][j] < 0:
                        enviroment2.map[i][j] = 0

        robotV.enviroment.paint(disp)
        robotV.paint(disp)

        if invert:
            screen.fill((255, 255, 255))
            screen.blit(disp, (0, 0), None, pygame.BLEND_SUB)
            screen.blit(disp2, (sizeX / 2, 0), None, pygame.BLEND_SUB)
        else:
            screen.blit(disp, (0, 0))
            screen.blit(disp2, (sizeX / 2, 0))
            for y in range (0, int(sizeY * mPerPixel)):
                for x in range (0, int(sizeX * mPerPixel)):
                    pygame.draw.circle(screen, (255, 255, 0), map(int, (x / mPerPixel , y / mPerPixel)), 2)

        graph.Paint(screen, sizeY - graph.gr.get_height(), invert)

        pygame.display.flip()


if __name__ == '__main__':
    #import psyco
    #psyco.full()

    #cProfile.run("RunRobotSim(1.0, 0.1)")
    RunRobotSim(1.0, 0.1)
    pygame.quit()
