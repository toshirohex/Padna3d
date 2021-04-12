from math import pi, sin, cos
import random as r
import time
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.gui.OnscreenText import OnscreenText

import random as r
# movement variable managers
appendz = 0
# vectors for rotational movement.
movementy = [1, 0.7071067812, 0, -0.7071067812, -1, -0.7071067812, 0, 0.7071067812]
movementx = [0, -0.7071067812, -1, -0.7071067812, 0, 0.7071067812, 1, 0.7071067812]
'''cameraX = [0,1.3334,2,1.3334,0,-1.3334,-2,-1.3334,0]
cameraY = [2,1.3334,0,-1.3334,-2,-1.3334,0,1.3334,2]'''

# Size manager
stretches = [0.0075, 0.0025]
canStretch = 0

# attack mechanics
canDamage = False
pandaActorHealth = 25
pandaActor2Health = 150

canRotate = True

def rotateManager():
    global canRotate
    if canRotate:
        canRotate = False
    else:
        canRotate = True

def viewRotate():
    global canRotate
    return canRotate

def posManager(plusminus):
    global appendz
    if plusminus:
        appendz += 1
    else:
        if appendz == 0:
            appendz += 8
        appendz += -1


def stretchCheck(strch):
    global stretches, canStretch
    if strch == 1:
        return stretches[canStretch % 2]
    else:
        canStretch += 1

#determines damage variables on panda collision.
def damageCheck(damage):
    global canDamage, pandaActorHealth, pandaActor2Health, canRotate
    if damage:
        if canDamage:
            canDamage = False
        else:
            canDamage = True
    else:
        if canRotate:
            if canDamage:
                dmg = r.randint(20, 30)
                bonus = r.randint(1, 10)
                if bonus > 9:
                    dmg += 20
                pandaActor2Health -= dmg
            else:
                dmg = 0
        # Using for loop to decrease the chance of the panda surviving a hit. will follow a binomial curve.
        # The higher I set iterations the less of a chance the panda has at surviving.
                iterations = r.randint(50,100)
                for i in range(iterations):
                    dmg+=(r.randint(20,30))
                dmg = dmg/iterations
                pandaActorHealth -= dmg
                dmg = 0

# check for health and "victory" conditions
def finishCheck():
    global pandaActorHealth, pandaActor2Health
    if pandaActorHealth <= 0:
        return 0
    elif pandaActor2Health <= 0:
        return 1
    else:
        return 2

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

def moveManager():
    if pandaActorHealth <= 0:
        return False
    else:
        return True

textObjects = [1,2]
class Panda(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        self.pandaActor = Actor("models/panda-model",{"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.0025,0.0025,0.0025)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")

        self.pandaActor2 = Actor("models/panda-model",{"walk": "models/panda-walk4"})
        self.pandaActor2.setScale(0.005,0.005,0.005)
        self.pandaActor2.reparentTo(self.render)
        self.pandaActor2.loop("walk")

        #set boss movement intervals for movement sequence.
        interval = [self.pandaActor2.posInterval(13,Point3(0, -10, 0),startPos=Point3(0, 10, 0)),self.pandaActor2.posInterval(13,Point3(0, 10, 0),startPos=Point3(0, -10, 0)),
                    self.pandaActor2.hprInterval(3,Point3(180, 0, 0),startHpr=Point3(0, 0, 0)),self.pandaActor2.hprInterval(3,Point3(0, 0, 0),startHpr=Point3(180, 0, 0))]
        self.bossSequene = Sequence(interval[0],interval[2],interval[1],interval[3],name="pandaPace")
        self.bossSequene.loop()

        #make camera fixed on panda
        #self.camera.reparentTo(self.pandaActor)

        # Keybinds
        map = base.win.get_keyboard_map()
        print(map)
        w_button = map.get_mapped_button("w")
        a_button = map.get_mapped_button("a")
        s_button = map.get_mapped_button("s")
        d_button = map.get_mapped_button("d")
        e_button = map.get_mapped_button("e")
        q_button = map.get_mapped_button("q")
        f_button = map.get_mapped_button("f")
        o_button = map.get_mapped_button("o")

    # Register event handlers
        self.accept("%s" % (w_button), self.movePandaTask)
        self.accept("%s" % (a_button), self.leftPandaTask)
        self.accept("%s" % (s_button), self.backPandaTask)
        self.accept("%s" % (d_button), self.rightPandaTask)
        self.accept("%s" % (e_button), self.pandaVanish)
        self.accept("%s" % (q_button), self.pandaStretchAttack)
        self.accept("%s" % (f_button), self.pandaSpinAttack)
        self.accept("%s" % (o_button), self.pandaResetTask)
        
    # Moves camera to fully show the 3d environment.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return task.cont

    # Moves pandaActor forward
    def movePandaTask(self):
        global textObjects,appendz,movementx,movementy
        x = self.pandaActor.getX()
        y = self.pandaActor.getY()
        z = self.pandaActor.getZ()
        xes = movementx[appendz%8]
        yes = movementy[appendz%8]
        forward = Sequence(self.pandaActor.posInterval(0.25,Point3(x+xes, y-yes, z),startPos=Point3(x, y, z)))
        if moveManager():
            forward.start()
        x2 = self.pandaActor2.getX()
        y2 = self.pandaActor2.getY()
        move = viewRotate()
        if x>x2-1 and x<x2+1 and move:
            if y>y2-1 and y<y2+1:
                damageCheck(False)
                damageCheck(True)
                stretch = stretchCheck(1)
                self.pandaActor.setScale(stretch,stretch,stretch)
                stretchCheck(2)
        finish = finishCheck()
        if finish == 0:
            self.pandaActor.setZ(-5)
            textObj = OnscreenText(text='WASTED',pos=(0,0),scale=0.5,fg=(255,0,0,1))
            textObj2 = OnscreenText(text='Press O to reset',pos=(0,-0.25),scale=0.125,fg=(255,0,0,1))
            resetManager(True)
            textObjects[0]=textObj
            textObjects[1]=textObj2
        elif finish == 1:
            self.bossSequene.finish()
            self.pandaActor2.setZ(-5)
            textObj = OnscreenText(text='YOU WIN!', pos=(0,0),scale=0.5,fg=(255,255,255,1))
            textObj2 = OnscreenText(text='Press O to reset',pos=(0,-0.25),scale=0.125,fg=(255,255,255,1))
            resetManager(True)
            textObjects[0]=textObj
            textObjects[1]=textObj2

    def backPandaTask(self):
        global appendz,movementx,movementy
        x = self.pandaActor.getX()
        y = self.pandaActor.getY()
        z = self.pandaActor.getZ()
        xes = movementx[appendz%8]
        yes = movementy[appendz%8]
        backward = Sequence(self.pandaActor.posInterval(0.25,Point3(x-xes, y+yes, z),startPos=Point3(x, y, z)))
        if moveManager():
            backward.start()
    
    def rightPandaTask(self):
        move = viewRotate()
        hpr = [self.pandaActor.getH(),self.pandaActor.getP(),self.pandaActor.getR()]
        rightSequence = Sequence(self.pandaActor.hprInterval(0.5,Point3(hpr[0]-45,hpr[1],hpr[2]),startHpr=Point3(hpr[0],hpr[1],hpr[2])), name="rightSequence")
        if move: 
            posManager(True)
            rightSequence.start()

    def leftPandaTask(self):
        move = viewRotate()
        hpr = [self.pandaActor.getH(),self.pandaActor.getP(),self.pandaActor.getR()]
        leftSequence = Sequence(self.pandaActor.hprInterval(0.5,Point3(hpr[0]+45,hpr[1],hpr[2]),startHpr=Point3(hpr[0],hpr[1],hpr[2])), name="rightSequence")
        if move:
            posManager(False)
            leftSequence.start()
    
    def pandaVanish(self):
        rotateManager()
        self.pandaActor.setR(self.pandaActor, 180)

    def pandaStretchAttack(self):
        damageCheck(True)
        stretch = stretchCheck(1)
        self.pandaActor.setScale(stretch,stretch,stretch)
        stretchCheck(2)

    def pandaSpinAttack(self):
        h = self.pandaActor.getH()
        p = self.pandaActor.getP()
        r = self.pandaActor.getR()
        hprInterval1 = self.pandaActor.hprInterval(1,Point3(h+180,p+180,r+180),startHpr=Point3(h,p,r))
        hprInterval2 = self.pandaActor.hprInterval(1,Point3(h+360,p+360,r+360),startHpr=Point3(h+180,p+180,r+180))
        pandaSpin = Sequence(hprInterval1, hprInterval2)
        for i in range(3):
            pandaSpin.start()

    def pandaResetTask(self):
        global textObjects,appendz,pandaActorHealth,pandaActor2Health
        canReset = resetManager(False)
        if canReset:
            appenz = appendz % 8
            self.pandaActor2.setZ(0)
            self.bossSequene.loop
            self.pandaActor.setZ(0)
            resetManager(True)
            textObjects[0].destroy()
            textObjects[1].destroy()
            pandaActorHealth = 25
            pandaActor2Health = 150

pdna = Panda()
pdna.run()

