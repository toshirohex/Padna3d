from math import pi, sin, cos
import random as r
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3


#movement variable managers
position = [] 
appendz = 0
#vectors for roational movement.
movementy = [1,float(0.7071067812),0,float(-0.7071067812),-1,float(-0.7071067812),0,float(0.7071067812)]
movementx = [0,float(-0.7071067812),-1,float(-0.7071067812),0,float(0.7071067812),1,float(0.7071067812)]
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

#Size manager
stretches = [0.0075, 0.0025]
stretch3s = []
canStretch = 0
def stretchCheck(strch):
    global stretch3s, stretches, canStretch
    if strch == 1:
        return stretches[len(stretch3s)%2]
    else:
        stretch3s.append(canStretch)
        canStretch+=1

#attack mechanics
canDamage = False
pandaActorHealth = 25
pandaActor2Health = 150
def damageCheck(damage, damage2):
    global canDamage, pandaActorHealth, pandaActor2Health
    if damage:
        if canDamage:
            canDamage = False
        else:
            canDamage = True
    else:
        if canDamage:
            dmg = r.randint(20,30)
            bonus = r.randint(1,10)
            if bonus > 9:
                dmg += 20
            pandaActor2Health -= dmg
        else:
            pandaActorHealth -= pandaActorHealth
            
#check for health and "victory" conditions
def finishCheck():
    global pandaActorHealth, pandaActor2Health
    if pandaActorHealth == 0:
        return 0
    elif pandaActor2Health == 0 and pandaActorHealth != 0:
        return 1
    else:
        return 2
    
    
    
   
class Panda(ShowBase):
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

    # Register event handlers
        self.accept("%s" % (w_button), self.movePandaTask)
        self.accept("%s" % (a_button), self.leftPandaTask)
        self.accept("%s" % (s_button), self.backPandaTask)
        self.accept("%s" % (d_button), self.rightPandaTask)
        self.accept("%s" % (e_button), self.pandaVanish)
        self.accept("%s" % (q_button), self.pandaStretchAttack)
        
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
        
    
    def backPandaTask(self):
        yes = ycormanager()
        xes = xcormanager()
        padna = [self.pandaActor]
        padna[0].setY(self.pandaActor.getY()+yes)
        padna[0].setX(self.pandaActor.getX()-xes)        
    
    def rightPandaTask(self):
        move = viewMove()
        if move:
            posManager(True)
            self.pandaActor.setH(self.pandaActor, -15)
            self.pandaActor.setH(self.pandaActor, -15)
            self.pandaActor.setH(self.pandaActor, -15)
        
    def leftPandaTask(self):
        move = viewMove()
        if move:
            posManager(False)
            self.pandaActor.setH(self.pandaActor, 45)
    
    def pandaVanish(self):
        moveManager()
        self.pandaActor.setR(self.pandaActor, 180)
        
    def pandaStretchAttack(self):
        stretch = stretchCheck(1)
        self.pandaActor.setScale(stretch,stretch,stretch)
        stretchCheck(2)
        
app = Panda()
app.run()