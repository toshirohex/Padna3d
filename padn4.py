from math import pi, sin, cos
#import pygame
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3



position = [] 
appendz = 0
#vectors for roational movement.
movementy = [1,0.66,-0.125,-0.66,-1,-0.66,0.125,0.66]
movementx = [0.125,-0.66,-1,-0.66,-0.125,0.66,1,0.66]
canMove = True 
def moveManager():
    global canMove
    if canMove:
        canMove = False
    else:
        canMove = True
def viewMove():
    global canMove
    return canMove
def posManager(plusminus):
    global position, appendz
    if plusminus:
        appendz += 1
        position.append(appendz)
    else:
        if appendz == 0:
            for i in range(8):
                appendz += 1
                position.append(appendz)
        position.remove(appendz)
        appendz += -1

def xcormanager():
    global position, appendz, movementx
    mmm = len(position) %8
    return movementx[mmm]
    
def ycormanager():
    global position, appendz, movementy
    mmm = len(position) %8
    return movementy[mmm]
                    
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor2 = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor3 = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor4 = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        scale = 0.0025
        self.pandaActor.setScale(scale, scale, scale)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")
        
        scale2 = 0.005
        self.pandaActor2.setScale(scale2, scale2, scale2)
        self.pandaActor2.reparentTo(self.render)
        self.pandaActor2.loop("walk")
        
        scale3 = 0.01
        self.pandaActor3.setScale(scale3, scale3, scale3)
        self.pandaActor3.reparentTo(self.render)
        self.pandaActor3.loop("walk")
        
        scale4 = 0.02
        self.pandaActor4.setScale(scale4, scale4, scale4)
        self.pandaActor4.reparentTo(self.render)
        self.pandaActor4.loop("walk")
        
    # Keybinds   
        map = base.win.get_keyboard_map()
        print(map)
        w_button = map.get_mapped_button("w")
        a_button = map.get_mapped_button("a")
        s_button = map.get_mapped_button("s")
        d_button = map.get_mapped_button("d")
        e_button = map.get_mapped_button("e")

    # Register event handlers
        self.accept("%s" % (w_button), self.movePandaTask)
        self.accept("%s" % (a_button), self.leftPandaTask)
        self.accept("%s" % (s_button), self.backPandaTask)
        self.accept("%s" % (d_button), self.rightPandaTask)
        self.accept("%s" % (e_button), self.pandaVanish)
    
    # Task stuff
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        
        return Task.cont
    
    def movePandaTask(self):
        yes = ycormanager()
        xes = xcormanager()
        self.pandaActor.setY(self.pandaActor.getY()-yes)
        self.pandaActor.setX(self.pandaActor.getX()+xes)
        self.pandaActor.setY(self.pandaActor2.getY()-yes)
        self.pandaActor2.setX(self.pandaActor2.getX()+xes)
        self.pandaActor3.setY(self.pandaActor3.getY()-yes)
        self.pandaActor3.setX(self.pandaActor3.getX()+xes)
        self.pandaActor4.setY(self.pandaActor4.getY()-yes)
        self.pandaActor4.setX(self.pandaActor4.getX()+xes)
    
    def backPandaTask(self):
        yes = ycormanager()
        xes = xcormanager()
        padna = [self.pandaActor, self.pandaActor2, self.pandaActor3, self.pandaActor4] 
        padna[0].setY(self.pandaActor.getY()+yes)
        padna[0].setX(self.pandaActor.getX()-xes)
        padna[1].setY(self.pandaActor2.getY()+yes)
        padna[1].setX(self.pandaActor2.getX()-xes)
        padna[2].setY(self.pandaActor3.getY()+yes)
        padna[2].setX(self.pandaActor3.getX()-xes)
        padna[3].setY(self.pandaActor4.getY()+yes)
        padna[3].setX(self.pandaActor4.getX()-xes)
    
    def rightPandaTask(self):
        move = viewMove
        if move:
            posManager(True)
            self.pandaActor.setH(self.pandaActor, -45)
            self.pandaActor2.setH(self.pandaActor2, -45)
            self.pandaActor3.setH(self.pandaActor3, -45)
            self.pandaActor4.setH(self.pandaActor4, -45)
        
    def leftPandaTask(self):
        move = viewMove
        if move:
            posManager(False)
            self.pandaActor.setH(self.pandaActor, 45)
            self.pandaActor2.setH(self.pandaActor2, 45)
            self.pandaActor3.setH(self.pandaActor3, 45)
            self.pandaActor4.setH(self.pandaActor4, 45)
    
    def pandaVanish(self):
        moveManager()
        self.pandaActor.setR(self.pandaActor, 180)
        
        

app = MyApp()
app.run()