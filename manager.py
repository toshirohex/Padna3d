import random as r
# movement variable managers
position = []
appendz = 0
# vectors for roational movement.
movementy = [1, float(0.7071067812), 0, float(-0.7071067812), -1, float(-0.7071067812), 0, float(0.7071067812)]
movementx = [0, float(-0.7071067812), -1, float(-0.7071067812), 0, float(0.7071067812), 1, float(0.7071067812)]
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
    global canDamage, pandaActorHealth, pandaActor2Health
    if damage:
        if canDamage:
            canDamage = False
        else:
            canDamage = True
    else:
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
    global canReset
    if true:
        canReset == true
        return canReset
    else:
        canReset = False
