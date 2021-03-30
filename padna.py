from math import pi, sin, cos
import random as r
import manager as m
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.gui.OnscreenText import OnscreenText

# movement variable managers
position = []
appendz = 0
# vectors for rotational movement.
movementy = [1, 0.7071067812, 0, -0.7071067812, -1, -0.7071067812, 0, 0.7071067812]
movementx = [0, -0.7071067812, -1, -0.7071067812, 0, 0.7071067812, 1, 0.7071067812]

#keeps panda from rotating when uses the disapear move triggered by e.
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
    mmm = len(position) % 8
    return movementx[mmm]


def ycormanager():
    global position, appendz, movementy
    mmm = len(position) % 8
    return movementy[mmm]


# Size manager
stretches = [0.0075, 0.0025]
stretch3s = []
canStretch = 0


def stretchCheck(strch):
    global stretch3s, stretches, canStretch
    if strch == 1:
        return stretches[len(stretch3s) % 2]
    else:
        stretch3s.append(canStretch)
        canStretch += 1


# attack mechanics
canDamage = False
pandaActorHealth = 25
pandaActor2Health = 150


def damageCheck(damage):
    global canDamage, pandaActorHealth, pandaActor2Health, canMove
    if damage:
        if canDamage:
            canDamage = False
        else:
            canDamage = True
    else:
        if canMove:
            if canDamage:
                dmg = r.randint(20, 30)
                bonus = r.randint(1, 10)
                if bonus > 9:
                    dmg += 20
                pandaActor2Health -= dmg
            else:
                pandaActorHealth -= pandaActorHealth


# check for health and "victory" conditions
def finishCheck():
    global pandaActorHealth, pandaActor2Health
    if pandaActorHealth <= 0:
        return 0
    elif pandaActor2Health <= 0:
        return 1
    else:
        return 2



canReset = False

def resetManager(true):
    global canReset, pandaActor2Health, pandaActorHealth
    if true:
        if pandaActorHealth <= 0 or pandaActor2Health <= 0:
            canReset = True
        else:
            canReset = False
    else:
        return canReset

def reset():
    global pandaActorHealth, pandaActor2Health, canReset
    if canReset:
        pandaActorHealth = 25
        pandaActor2Health = 150

textObjects = []
class Panda(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.pandaActor = Actor("models/panda-model",{"walk": "models/panda-walk4"})
        self.pandaActor2 = Actor("models/panda-model",{"walk": "models/panda-walk4"})
        scale = 0.0025
        self.pandaActor.setScale(scale, scale, scale)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")
        
        scale2 = 0.005
        self.pandaActor2.setScale(scale2, scale2, scale2)
        self.pandaActor2.reparentTo(self.render)
        self.pandaActor2.loop("walk")
        
        #set boss movement intervals for movement sequence.
        posInterval1 = self.pandaActor2.posInterval(13,Point3(0, -10, 0),startPos=Point3(0, 10, 0))
        posInterval2 = self.pandaActor2.posInterval(13,Point3(0, 10, 0),startPos=Point3(0, -10, 0))
        hprInterval1 = self.pandaActor2.hprInterval(3,Point3(180, 0, 0),startHpr=Point3(0, 0, 0))
        hprInterval2 = self.pandaActor2.hprInterval(3,Point3(0, 0, 0),startHpr=Point3(180, 0, 0))
        self.bossSequene = Sequence(posInterval1, hprInterval1,posInterval2,hprInterval2,name="pandaPace")
        self.bossSequene.loop()

        
    # Keybinds   
        map = base.win.get_keyboard_map()
        print(map)
        w_button = map.get_mapped_button("w")
        a_button = map.get_mapped_button("a")
        s_button = map.get_mapped_button("s")
        d_button = map.get_mapped_button("d")
        e_button = map.get_mapped_button("e")
        q_button = map.get_mapped_button("q")
        enter_button = map.get_mapped_button("f")
    # Register event handlers
        self.accept("%s" % (w_button), self.movePandaTask)
        self.accept("%s" % (a_button), self.leftPandaTask)
        self.accept("%s" % (s_button), self.backPandaTask)
        self.accept("%s" % (d_button), self.rightPandaTask)
        self.accept("%s" % (e_button), self.pandaVanish)
        self.accept("%s" % (q_button), self.pandaStretchAttack)
        self.accept("%s" % (enter_button), self.pandaResetTask)
        
    # Task stuff
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        
        return Task.cont
    
    def movePandaTask(self):
        global textObjects
        yes = m.ycormanager()
        xes = m.xcormanager()
        self.pandaActor.setY(self.pandaActor.getY()-yes)
        self.pandaActor.setX(self.pandaActor.getX()+xes)
        x = self.pandaActor.getX()
        x2 = self.pandaActor2.getX()
        y = self.pandaActor.getY()
        y2 = self.pandaActor2.getY()
        if x>x2-1 and x<x2+1:
            if y>y2-1 and y<y2+1:
                m.damageCheck(False)
                m.damageCheck(True)
                stretch = m.stretchCheck(1)
                self.pandaActor.setScale(stretch,stretch,stretch)
                m.stretchCheck(2)
        finish = m.finishCheck()
        if finish == 0:
            self.pandaActor.setZ(-5)
            textObj = OnscreenText(text='WASTED',pos=(0,0),scale=0.5,fg=(255,0,0,1))
            #textObj2 = OnscreenText(text='Press ENTER to reset',pos=(0,-0.25),scale=0.125,fg=(255,0,0,1))
            m.resetManager(True)
            textObjects.append(textObj)
            #textObjects.append(textObj2)
        elif finish == 1:
            self.bossSequene.finish()
            self.pandaActor2.setZ(-5)
            textObj = OnscreenText(text='YOU WIN!', pos=(0,0),scale=0.5,fg=(255,255,255,1))
            #tedtObj2 = OnscreenText(text='Press ENTER to reset',pos=(0,-0.25),scale=0.125,fg=(255,255,255,1))
            m.resetManager(True)
            textObjects.append(textObj)
            #textObjects.append(textObj2)

    def backPandaTask(self):
        yes = m.ycormanager()
        xes = m.xcormanager()
        padna = [self.pandaActor]
        padna[0].setY(self.pandaActor.getY()+yes)
        padna[0].setX(self.pandaActor.getX()-xes)        
    
    def rightPandaTask(self):
        move = m.viewMove()
        if move:
            m.posManager(True)
            self.pandaActor.setH(self.pandaActor, -15)
            self.pandaActor.setH(self.pandaActor, -15)
            self.pandaActor.setH(self.pandaActor, -15)
        
    def leftPandaTask(self):
        move = m.viewMove()
        if move:
            m.posManager(False)
            self.pandaActor.setH(self.pandaActor, 45)
    
    def pandaVanish(self):
        m.moveManager()
        self.pandaActor.setR(self.pandaActor, 180)
        
    def pandaStretchAttack(self):
        m.damageCheck(True)
        stretch = m.stretchCheck(1)
        self.pandaActor.setScale(stretch,stretch,stretch)
        m.stretchCheck(2)

    def pandaResetTask(self):
        global textObjects
        canReset = m.resetManager(False)
        if canReset:
            self.pandaActor2.setZ(0)
            self.bossSequene.loop
            self.pandaActor.setZ(0)
            m.resetManager(True)
            textObjects[0].destroy()
            #textObjects[1].destroy()

        
pdna = Panda()
pdna.run()