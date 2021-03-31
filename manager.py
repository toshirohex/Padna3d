import random as r
# movement variable managers
position = []
appendz = 0
# vectors for rotational movement.
movementy = [1, 0.7071067812, 0, -0.7071067812, -1, -0.7071067812, 0, 0.7071067812]
movementx = [0, -0.7071067812, -1, -0.7071067812, 0, 0.7071067812, 1, 0.7071067812]

#keeps panda from rotating when uses the disapear move triggered by e.
canMove = True

# Size manager
stretches = [0.0075, 0.0025]
stretch3s = []
canStretch = 0

# attack mechanics
canDamage = False
pandaActorHealth = 25
pandaActor2Health = 150

#Used to ensure that the reset isn't accidentally triggered.
canReset = False

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

def stretchCheck(strch):
    global stretch3s, stretches, canStretch
    if strch == 1:
        return stretches[len(stretch3s) % 2]
    else:
        stretch3s.append(canStretch)
        canStretch += 1

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