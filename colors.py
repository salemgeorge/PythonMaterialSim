import random

BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
YELLOW = (248, 196, 113)

def RandomizeColor(rMin, gMin, bMin, rMax, gMax, bMax):
    rRand = random.randint(rMin, rMax)
    gRand = random.randint(gMin, gMax)
    bRand = random.randint(bMin, bMax)

    return [rRand, gRand, bRand]