import pygame
import random

from colors import *
from functions import *


class SandBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 5
    fallProgress = 0

    name = "Sand"

    canBurn = False

    bitsToFallThrough = ["Water", "Smoke", "Gas", "Lava"]

    canHaveSmokeCover = True
    hasSmokeCover = False
    smokeFallSpeed = 5
    smokeFallProgress = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # red   - 171, 200
        # green - 124, 148
        # blue  -  49, 66
        self.randColor = RandomizeColor(171, 124, 49, 200, 148, 66)
        self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

    def GetPos(self):
        return [self.x, self.y]

    def SetPos(self, x, y):
        print("updated pos")
        self.x = x
        self.y = y

    def GetName(self):
        return self.name

    def SetSmokeCover(self, toSetToo):
        if toSetToo and not self.hasSmokeCover:
            self.hasSmokeCover = True

            self.ogColor = self.color

            self.randColor = RandomizeColor(50, 50, 50, 60, 60, 60)
            self.color = (self.randColor[0], self.randColor[1], self.randColor[2])
        elif not toSetToo and self.hasSmokeCover:
            self.hasSmokeCover = False

            self.color = self.ogColor

    def GetSmokeCover(self):
        return self.hasSmokeCover

    def HandleBehaviour(self, grid, grid_width, grid_height):
        bits = GetAdjacentBits(self.x, self.y, grid, grid_width, grid_height)
        bitDown = bits[3]

        if self.fallProgress >= self.fallSpeed and bitDown != -1:
            self.fallProgress = 0

            if bitDown:
                if bits[4][3].GetName() in self.bitsToFallThrough:
                    bits[4][3].SetPos(self.x, self.y)
                    self.y += 1

                    return [self.x, self.y, "MovedMultipleBits", bits[4][3]]
                else:
                    leftCheck = GetBit(self.x - 2, self.y + 1, grid)
                    leftGapCheck = GetBit(self.x - 1, self.y + 1, grid)

                    rightCheck = GetBit(self.x + 2, self.y + 1, grid)
                    rightGapCheck = GetBit(self.x + 2, self.y + 1, grid)

                    canMoveLeft = False
                    canMoveRight = False

                    isWaterLeft = False
                    isWaterRight = False

                    if ((leftCheck != -2 and leftCheck != -1) and leftCheck.GetName() in self.bitsToFallThrough) or ((leftGapCheck != -2 and leftGapCheck != -1) and leftGapCheck.GetName() in self.bitsToFallThrough):
                        if bits[0] == True and bits[4][0].GetName() in self.bitsToFallThrough:
                            isWaterLeft = True

                        canMoveLeft = True
                    elif leftCheck == -1 or leftGapCheck == -1:
                        canMoveLeft = True

                    if ((rightCheck != -2 and rightCheck != -1) and rightCheck.GetName() in self.bitsToFallThrough) or ((rightGapCheck != -2 and rightGapCheck != -1) and rightGapCheck.GetName() in self.bitsToFallThrough):
                        if bits[1] == True and bits[4][1].GetName() in self.bitsToFallThrough:
                            isWaterRight = True

                        canMoveRight = True
                    elif rightCheck == -1 or rightGapCheck == -1:
                        canMoveRight = True

                    if canMoveLeft and not canMoveRight:
                        if isWaterLeft:
                            bits[4][0].SetPos(self.x, self.y)
                            self.x -= 1
                            return [self.x, self.y, "MovedMultipleBits", bits[4][0]]
                        elif bits[0] == False:
                            self.x -= 1
                    elif not canMoveLeft and canMoveRight:
                        if isWaterRight:
                            bits[4][1].SetPos(self.x, self.y)
                            self.x += 1
                            return [self.x, self.y, "MovedMultipleBits", bits[4][1]]
                        elif bits[1] == False:
                            self.x += 1
                    elif canMoveLeft and canMoveRight:
                        randChance = random.random()

                        if randChance < 0.5:
                            if isWaterLeft:
                                bits[4][0].SetPos(self.x, self.y)
                                self.x -= 1
                                return [self.x, self.y, "MovedMultipleBits", bits[4][0]]
                            elif bits[0] == False:
                                self.x -= 1
                        elif randChance > 0.5:
                            if isWaterRight:
                                bits[4][1].SetPos(self.x, self.y)
                                self.x += 1
                                return [self.x, self.y, "MovedMultipleBits", bits[4][1]]
                            elif bits[1] == False:
                                self.x += 1

            elif not bitDown:
                self.y += 1

            return [self.x, self.y]

        else:
            return [self.x, self.y]

    def HandleSmokeCover(self, grid):
        if self.smokeFallProgress >= self.smokeFallSpeed and self.y - 1 >= 0:
            self.smokeFallProgress = 0
            bitUp = GetBit(self.x, self.y - 1, grid)

            if CheckBitExists(bitUp) and bitUp.canHaveSmokeCover:
                bitUp.SetSmokeCover(True)
                self.SetSmokeCover(False)
            elif not CheckBitExists(bitUp):
                self.SetSmokeCover(False)
                SetBit(SmokeBit(self.x, self.y - 1), self.x, self.y - 1, grid)

    def UpdateBitClock(self):
        self.fallProgress += 1
        if self.hasSmokeCover:
            self.smokeFallProgress += 1

    def DrawSelf(self, bit_width, bit_height):
        pygame.draw.rect(pygame.display.get_surface(), self.color,
                         [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class DirtBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 6
    fallProgress = 0

    name = "Dirt"

    canBurn = False

    bitsToFallThrough = ["Water", "Smoke", "Gas", "Lava"]

    canHaveSmokeCover = True
    hasSmokeCover = False
    smokeFallSpeed = 5
    smokeFallProgress = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # red   - 88, 120
        # green - 70, 96
        # blue  -  29, 43
        self.randColor = RandomizeColor(88, 70, 29, 120, 96, 43)
        self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

    def GetPos(self):
        return [self.x, self.y]

    def SetPos(self, x, y):
        self.x = x
        self.y = y

    def GetName(self):
        return self.name

    def SetSmokeCover(self, toSetToo):
        if toSetToo and not self.hasSmokeCover:
            self.hasSmokeCover = True

            self.ogColor = self.color

            self.randColor = RandomizeColor(50, 50, 50, 60, 60, 60)
            self.color = (self.randColor[0], self.randColor[1], self.randColor[2])
        elif not toSetToo and self.hasSmokeCover:
            self.hasSmokeCover = False

            self.color = self.ogColor

    def GetSmokeCover(self):
        return self.hasSmokeCover

    def HandleBehaviour(self, grid, grid_width, grid_height):
        if self.fallProgress >= self.fallSpeed or self.y == grid_height - 1:
            self.fallProgress = 0
            bitDown = GetBit(self.x, self.y + 1, grid)
            bitLeft = GetBit(self.x - 1, self.y, grid)
            bitRight = GetBit(self.x + 1, self.y, grid)

            isWaterDown = CheckBitExists(bitDown) and bitDown.GetName() in self.bitsToFallThrough

            if not isWaterDown and CheckBitExists(bitDown):
                downDistLeft = 3
                downDistRight = 3

                bitLeftDown = GetBit(self.x - 1, self.y + downDistLeft, grid)
                bitRightDown = GetBit(self.x + 1, self.y + downDistRight, grid)

                canMoveLeftDetails = CheckCanMoveWater(bitLeftDown, bitLeft, self.bitsToFallThrough)
                canMoveRightDetails = CheckCanMoveWater(bitRightDown, bitRight, self.bitsToFallThrough)

                canMoveLeft = canMoveLeftDetails[0]
                canMoveRight = canMoveRightDetails[0]

                if canMoveLeft and not canMoveRight:
                    if canMoveLeftDetails[1]:
                        newPos = SwapBits([self.x, self.y], bitLeft.GetPos(), grid)
                        return [newPos[0], newPos[1], "MovedMultipleBits", newPos[2]]
                    elif bitLeft == -1:
                        self.x -= 1
                elif not canMoveLeft and canMoveRight:
                    if canMoveRightDetails[1]:
                        newPos = SwapBits([self.x, self.y], bitRight.GetPos(), grid)
                        return [newPos[0], newPos[1], "MovedMultipleBits", newPos[2]]
                    elif bitRight == -1:
                        self.x += 1
                elif canMoveLeft and canMoveRight:
                    randChance = random.random()

                    if randChance < 0.5:
                        if canMoveLeftDetails[1]:
                            newPos = SwapBits([self.x, self.y], bitLeft.GetPos(), grid)
                            return [newPos[0], newPos[1], "MovedMultipleBits", newPos[2]]
                        elif bitLeft == -1:
                            self.x -= 1
                    elif randChance > 0.5:
                        if canMoveRightDetails[1]:
                            newPos = SwapBits([self.x, self.y], bitRight.GetPos(), grid)
                            return [newPos[0], newPos[1], "MovedMultipleBits", newPos[2]]
                        elif bitRight == -1:
                            self.x += 1

                return [self.x, self.y]
            elif isWaterDown:
                newPos = SwapBits([self.x, self.y], bitDown.GetPos(), grid)
                return [newPos[0], newPos[1], "MovedMultipleBits", newPos[2]]
            elif bitDown == -1:
                self.y += 1

            return [self.x, self.y]
        else:
            return [self.x, self.y]

    def HandleSmokeCover(self, grid):
        if self.smokeFallProgress >= self.smokeFallSpeed and self.y - 1 >= 0:
            self.smokeFallProgress = 0
            bitUp = GetBit(self.x, self.y - 1, grid)

            if CheckBitExists(bitUp) and bitUp.canHaveSmokeCover:
                bitUp.SetSmokeCover(True)
                self.SetSmokeCover(False)
            elif not CheckBitExists(bitUp):
                self.SetSmokeCover(False)
                SetBit(SmokeBit(self.x, self.y - 1), self.x, self.y - 1, grid)

    def UpdateBitClock(self):
        self.fallProgress += 1
        if self.hasSmokeCover:
            self.smokeFallProgress += 1

    def DrawSelf(self, bit_width, bit_height):
        pygame.draw.rect(pygame.display.get_surface(), self.color,
                         [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class SmokeBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 5
    fallProgress = 0

    name = "Smoke"

    canBurn = False

    canHaveSmokeCover = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # min = 35, 33, 33
        # max = 72, 69, 68
        self.randColor = RandomizeColor(50, 50, 50, 60, 60, 60)
        self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

    def GetPos(self):
        return [self.x, self.y]

    def SetPos(self, x, y):
        self.x = x
        self.y = y

    def GetName(self):
        return self.name

    def HandleBehaviour(self, grid, grid_width, grid_height):
        if self.y - 1 >= 0 and self.fallProgress >= self.fallSpeed:
            self.fallProgress = 0

            if GetBit(self.x, self.y - 1, grid) != -1:
                leftTestDistance = 1
                rightTestDistance = 1

                leftBit = -2
                rightBit = -2

                if self.x == 0:
                    return [self.x, self.y]
                else:
                    leftBit = GetBit(self.x - 1, self.y, grid)

                if self.x == grid_width - 1:
                    return [self.x, self.y]
                else:
                    rightBit = GetBit(self.x + 1, self.y, grid)

                if leftBit == -1 and rightBit != -1:
                    self.x -= 1

                    return [self.x, self.y]
                elif leftBit != -1 and rightBit == -1:
                    self.x += 1

                    return [self.x, self.y]
                elif leftBit == -1 and rightBit == -1:
                    randChance = random.random()

                    if randChance < 0.5:
                        self.x -= 1
                    elif randChance > 0.5:
                        self.x += 1

                    return [self.x, self.y]

            elif GetBit(self.x, self.y - 1, grid) == -1:
                self.y -= 1

                return [self.x, self.y]

        return [self.x, self.y]

    def HandleSmokeCover(self, grid):
        pass

    def UpdateBitClock(self):
        self.fallProgress += 1

    def DrawSelf(self, bit_width, bit_height):
        pygame.draw.rect(pygame.display.get_surface(), self.color,
                         [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class WaterBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 2
    fallProgress = 0

    name = "Water"

    canBurn = False

    canHaveSmokeCover = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # min = 32, 110, 127
        # max = 32, 158, 181
        self.randColor = RandomizeColor(36, 174, 140, 36, 174, 169)
        self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

    def GetPos(self):
        return [self.x, self.y]

    def SetPos(self, x, y):
        self.x = x
        self.y = y

    def GetName(self):
        return self.name

    def HandleBehaviour(self, grid, grid_width, grid_height):
        if self.fallProgress >= self.fallSpeed:

            bitDown = -2
            if self.y + 1 <= grid_height - 1:
                bitDown = GetBit(self.x, self.y + 1, grid)

            if bitDown != -2 and bitDown != -1:
                leftDistance = 1
                rightDistance = 1

                if self.x == 0:
                    leftDistance = 0
                if self.x == grid_width - 1:
                    rightDistance = 0

                leftBit = GetBit(self.x - leftDistance, self.y, grid)
                rightBit = GetBit(self.x + rightDistance, self.y, grid)

                if leftBit == -1 and rightBit != -1:
                    self.x -= 1

                    self.fallProgress = 0
                elif leftBit != -1 and rightBit == -1:
                    self.x += 1

                    self.fallProgress = 0
                elif leftBit == -1 and rightBit == -1:
                    randChance = random.random()

                    if randChance < 0.5:
                        if GetBit(self.x - 1, self.y, grid) == -1:
                            self.x -= 1
                    elif randChance > 0.5:
                        if GetBit(self.x + 1, self.y, grid) == -1:
                            self.x += 1

                    self.fallProgress = 0

            elif bitDown == -1:
                self.y += 1

                self.fallProgress = 0

        return [self.x, self.y]

    def HandleSmokeCover(self, grid):
        pass

    def UpdateBitClock(self):
        self.fallProgress += 1

    def DrawSelf(self, bit_width, bit_height):
        pygame.draw.rect(pygame.display.get_surface(), self.color,
                         [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class WallBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 6
    fallProgress = 0

    name = "Wall"

    canBurn = False

    canHaveSmokeCover = True
    hasSmokeCover = False
    smokeFallSpeed = 5
    smokeFallProgress = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.color = (144, 144, 144)

    def GetPos(self):
        return [self.x, self.y]

    def SetPos(self, x, y):
        self.x = x
        self.y = y

    def GetName(self):
        return self.name

    def SetSmokeCover(self, toSetToo):
        if toSetToo and not self.hasSmokeCover:
            self.hasSmokeCover = True

            self.ogColor = self.color

            self.randColor = RandomizeColor(50, 50, 50, 60, 60, 60)
            self.color = (self.randColor[0], self.randColor[1], self.randColor[2])
        elif not toSetToo and self.hasSmokeCover:
            self.hasSmokeCover = False

            self.color = self.ogColor

    def GetSmokeCover(self):
        return self.hasSmokeCover

    def HandleBehaviour(self, grid, grid_width, grid_height):
        return [self.x, self.y]

    def HandleSmokeCover(self, grid):
        if self.smokeFallProgress >= self.smokeFallSpeed and self.y - 1 >= 0:
            self.smokeFallProgress = 0
            bitUp = GetBit(self.x, self.y - 1, grid)

            if CheckBitExists(bitUp) and bitUp.canHaveSmokeCover:
                bitUp.SetSmokeCover(True)
                self.SetSmokeCover(False)
            elif not CheckBitExists(bitUp):
                self.SetSmokeCover(False)
                SetBit(SmokeBit(self.x, self.y - 1), self.x, self.y - 1, grid)

    def UpdateBitClock(self):
        if self.hasSmokeCover:
            self.smokeFallProgress += 1

    def DrawSelf(self, bit_width, bit_height):
        pygame.draw.rect(pygame.display.get_surface(), self.color,
                         [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class WoodBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 4
    fallProgress = 0

    name = "Wood"

    canBurn = True
    isBurning = False
    bitHealth = 30
    charcoalBitHealth = 15

    canHaveSmokeCover = True
    hasSmokeCover = False
    smokeFallSpeed = 5
    smokeFallProgress = 0

    ogColor = -1

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # red   - 88, 120
        # green - 70, 96
        # blue  -  29, 43
        self.randColor = RandomizeColor(88, 70, 29, 107, 80, 29)
        self.color = (self.randColor[0], self.randColor[1], self.randColor[2])
        self.ogColor = self.color

    def GetPos(self):
        return [self.x, self.y]

    def SetPos(self, x, y):
        self.x = x
        self.y = y

    def SetSmokeCover(self, toSetToo):
        if toSetToo and not self.hasSmokeCover:
            self.hasSmokeCover = True

            self.ogColor = self.color

            self.randColor = RandomizeColor(50, 50, 50, 60, 60, 60)
            self.color = (self.randColor[0], self.randColor[1], self.randColor[2])
        elif not toSetToo and self.hasSmokeCover:
            self.hasSmokeCover = False

            self.color = self.ogColor

    def GetSmokeCover(self):
        return self.hasSmokeCover

    def Ignite(self, grid):
        bitAbove = GetBit(self.x, self.y - 1, grid)
        isWaterAbove = CheckBitExists(bitAbove) and bitAbove.GetName() == "Water"

        if not self.isBurning and not isWaterAbove:
            self.isBurning = True

            self.randColor = RandomizeColor(160, 50, 20, 191, 60, 30)
            self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

    def GetName(self):
        return self.name

    def HandleBehaviour(self, grid, grid_width, grid_height):
        if self.fallProgress >= self.fallSpeed or self.y == grid_height - 1:
            self.fallProgress = 0

            bitDown = GetBit(self.x, self.y + 1, grid)

            adjacentBits = GetAdjacentBits(self.x, self.y, grid, grid_width, grid_height)

            if self.isBurning and self.bitHealth > 0:
                randChance = random.random()

                if randChance <= 0.15:
                    randDir = random.random()
                    if randDir >= 0 and randDir <= 0.25 and CheckBitExists(adjacentBits[4][0]) and adjacentBits[4][0].GetName() == "Wood":
                        adjacentBits[4][0].Ignite(grid)
                    elif randDir > 0.25 and randDir <= 0.50 and CheckBitExists(adjacentBits[4][1]) and adjacentBits[4][1].GetName() == "Wood":
                        adjacentBits[4][1].Ignite(grid)
                    elif randDir > 0.50 and randDir <= 0.75 and CheckBitExists(adjacentBits[4][2]) and adjacentBits[4][2].GetName() == "Wood":
                        adjacentBits[4][2].Ignite(grid)
                    elif CheckBitExists(adjacentBits[4][3]) and adjacentBits[4][3].GetName() == "Wood":
                        adjacentBits[4][3].Ignite(grid)

                if self.y - 1 >= 0 and randChance <= 0.25:
                    bitAbove = GetBit(self.x, self.y - 1, grid)
                    if not CheckBitExists(bitAbove):
                        SetBit(SmokeBit(self.x, self.y - 1), self.x, self.y - 1, grid)
                    elif CheckBitExists(bitAbove) and bitAbove.canHaveSmokeCover:
                        GetBit(self.x, self.y - 1, grid).SetSmokeCover(True)

                self.randColor = RandomizeColor(160, 50, 20, 191, 60, 30)
                self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

                self.bitHealth -= 1
                if self.bitHealth == 0:
                    self.bitHealth = -1
                    if randChance <= 0.5:
                        self.randColor = RandomizeColor(0, 0, 0, 75, 0, 0)
                        self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

                        self.fallSpeed *= 3
                    else:
                        return [self.x, self.y, "BitDied"]
            elif bitDown == -1:
                self.y += 1

            if self.bitHealth == -1:
                self.charcoalBitHealth -= 1
                if self.charcoalBitHealth <= 0:
                    return [self.x, self.y, "BitDied"]

                self.randColor = RandomizeColor(50, 25, 25, 100, 25, 25)
                self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

            return [self.x, self.y]
        else:
            return [self.x, self.y]

    def HandleSmokeCover(self, grid):
        if self.smokeFallProgress >= self.smokeFallSpeed and self.y - 1 >= 0:
            self.smokeFallProgress = 0
            bitUp = GetBit(self.x, self.y - 1, grid)

            if CheckBitExists(bitUp) and bitUp.canHaveSmokeCover:
                bitUp.SetSmokeCover(True)
                self.SetSmokeCover(False)
            elif not CheckBitExists(bitUp):
                self.SetSmokeCover(False)
                SetBit(SmokeBit(self.x, self.y - 1), self.x, self.y - 1, grid)

    def UpdateBitClock(self):
        self.fallProgress += 1
        if self.hasSmokeCover:
            self.smokeFallProgress += 1

    def DrawSelf(self, bit_width, bit_height):
        if not self.hasSmokeCover:
            pygame.draw.rect(pygame.display.get_surface(), self.color, [self.x * bit_width, self.y * bit_height, bit_width, bit_height])
        else:
            pygame.draw.rect(pygame.display.get_surface(), self.color, [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class GasBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 4
    fallProgress = 0

    name = "Gas"

    canBurn = True
    isBurning = False
    bitHealth = 30

    canHaveSmokeCover = False

    ogColor = -1

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # red   - 88, 120
        # green - 70, 96
        # blue  -  29, 43
        self.randColor = RandomizeColor(0, 200, 0, 0, 255, 0)
        self.color = (self.randColor[0], self.randColor[1], self.randColor[2])
        self.ogColor = self.color

    def GetPos(self):
        return [self.x, self.y]

    def SetPos(self, x, y):
        self.x = x
        self.y = y

    def GetSmokeCover(self):
        return False

    def Ignite(self, grid):
        bitAbove = GetBit(self.x, self.y - 1, grid)
        isWaterAbove = CheckBitExists(bitAbove) and bitAbove.GetName() == "Water"

        if not self.isBurning and not isWaterAbove:
            self.isBurning = True

            self.randColor = RandomizeColor(160, 50, 20, 191, 60, 30)
            self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

    def GetName(self):
        return self.name

    def HandleBehaviour(self, grid, grid_width, grid_height):
        if self.fallProgress >= self.fallSpeed:
            self.fallProgress = 0

            adjacentBits = GetAdjacentBits(self.x, self.y, grid, grid_height, grid_width)
            leftBit = adjacentBits[4][0]
            rightBit = adjacentBits[4][1]
            upBit = adjacentBits[4][2]
            downBit = adjacentBits[4][3]

            if self.isBurning and self.bitHealth > 0:
                self.bitHealth -= 1
                bitsAround = GetBitsAround(self.x, self.y, grid)

                for bit in bitsAround[8]:
                    randChance = random.random()
                    if randChance <= 0.25 and CheckBitExists(bit) and bit.canBurn:
                        bit.Ignite(grid)

                if self.bitHealth <= 0:
                    return [self.x, self.y, "BitDied", "ProduceSmoke"]

            randDir = random.random()
            if self.x > 0 and randDir >= 0 and randDir <= 0.25 and not CheckBitExists(leftBit):
                self.x -= 1
                return [self.x, self.y]
            elif self.x < grid_width - 1 and randDir > 0.25 and randDir <= 0.50 and not CheckBitExists(rightBit):
                self.x += 1
                return [self.x, self.y]
            elif self.y > 0 and randDir > 0.50 and randDir <= 0.75 and not CheckBitExists(upBit):
                self.y -= 1
                return [self.x, self.y]
            elif self.y < grid_height - 1 and randDir > 0.75 and not CheckBitExists(downBit):
                self.y += 1
                return [self.x, self.y]

            return [self.x, self.y]
        else:
            return [self.x, self.y]

    def HandleSmokeCover(self, grid):
        pass

    def UpdateBitClock(self):
        self.fallProgress += 1

    def DrawSelf(self, bit_width, bit_height):
            pygame.draw.rect(pygame.display.get_surface(), self.color,
                             [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class LavaBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 4
    fallProgress = 0

    name = "Lava"

    bitsToGlass = ["Sand"]
    bitsToEvaporate = ["Water"]

    canBurn = False

    canHaveSmokeCover = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # min = 32, 110, 127
        # max = 32, 158, 181
        self.randColor = RandomizeColor(150, 0, 0, 255, 0, 0)
        self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

    def GetPos(self):
        return [self.x, self.y]

    def SetPos(self, x, y):
        self.x = x
        self.y = y

    def GetName(self):
        return self.name

    def HandleBehaviour(self, grid, grid_width, grid_height):
        if self.fallProgress >= self.fallSpeed:

            if random.random() < 0.1:
                self.randColor = RandomizeColor(150, 0, 0, 255, 0, 0)
                self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

            if not CheckBitExists(GetBit(self.x, self.y - 1, grid)) and random.random() < 0.001:
                SetBit(SmokeBit(self.x, self.y - 1), self.x, self.y - 1, grid)

            bitDown = -2
            if self.y + 1 <= grid_height - 1:
                bitDown = GetBit(self.x, self.y + 1, grid)

            if bitDown != -2 and bitDown != -1:
                if bitDown in self.bitsToGlass:
                    pass
                elif bitDown in self.bitsToEvaporate:
                    pass
                else:
                    leftDistance = 1
                    rightDistance = 1

                    if self.x == 0:
                        leftDistance = 0
                    if self.x == grid_width - 1:
                        rightDistance = 0

                    leftBit = GetBit(self.x - leftDistance, self.y, grid)
                    rightBit = GetBit(self.x + rightDistance, self.y, grid)

                    if leftBit == -1 and rightBit != -1:
                        self.x -= 1

                        self.fallProgress = 0
                    elif leftBit != -1 and rightBit == -1:
                        self.x += 1

                        self.fallProgress = 0
                    elif leftBit == -1 and rightBit == -1:
                        randChance = random.random()

                        if randChance < 0.5:
                            if GetBit(self.x - 1, self.y, grid) == -1:
                                self.x -= 1
                        elif randChance > 0.5:
                            if GetBit(self.x + 1, self.y, grid) == -1:
                                self.x += 1

                        self.fallProgress = 0

            elif bitDown == -1:
                self.y += 1

                self.fallProgress = 0

        return [self.x, self.y]

    def HandleSmokeCover(self, grid):
        pass

    def UpdateBitClock(self):
        self.fallProgress += 1

    def DrawSelf(self, bit_width, bit_height):
        pygame.draw.rect(pygame.display.get_surface(), self.color,
                         [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class GlassBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 4
    fallProgress = 0

    name = "Wood"

    canBurn = False

    canHaveSmokeCover = True
    hasSmokeCover = False
    smokeFallSpeed = 5
    smokeFallProgress = 0

    ogColor = -1

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # red   - 88, 120
        # green - 70, 96
        # blue  -  29, 43
        self.randColor = RandomizeColor(240, 240, 240, 255, 255, 255)
        self.color = (self.randColor[0], self.randColor[1], self.randColor[2])
        self.ogColor = self.color

    def GetPos(self):
        return [self.x, self.y]

    def SetPos(self, x, y):
        self.x = x
        self.y = y

    def SetSmokeCover(self, toSetToo):
        if toSetToo and not self.hasSmokeCover:
            self.hasSmokeCover = True

            self.ogColor = self.color

            self.randColor = RandomizeColor(50, 50, 50, 60, 60, 60)
            self.color = (self.randColor[0], self.randColor[1], self.randColor[2])
        elif not toSetToo and self.hasSmokeCover:
            self.hasSmokeCover = False

            self.color = self.ogColor

    def GetSmokeCover(self):
        return self.hasSmokeCover

    def GetName(self):
        return self.name

    def HandleBehaviour(self, grid, grid_width, grid_height):
        if self.fallProgress >= self.fallSpeed or self.y == grid_height - 1:
            self.fallProgress = 0
            if GetBit(self.x, self.y + 1, grid) == -1:
                self.y += 1

            return [self.x, self.y]
        else:
            return [self.x, self.y]

    def HandleSmokeCover(self, grid):
        if self.smokeFallProgress >= self.smokeFallSpeed and self.y - 1 >= 0:
            self.smokeFallProgress = 0
            bitUp = GetBit(self.x, self.y - 1, grid)

            if CheckBitExists(bitUp) and bitUp.canHaveSmokeCover:
                bitUp.SetSmokeCover(True)
                self.SetSmokeCover(False)
            elif not CheckBitExists(bitUp):
                self.SetSmokeCover(False)
                SetBit(SmokeBit(self.x, self.y - 1), self.x, self.y - 1, grid)

    def UpdateBitClock(self):
        self.fallProgress += 1
        if self.hasSmokeCover:
            self.smokeFallProgress += 1

    def DrawSelf(self, bit_width, bit_height):
        if not self.hasSmokeCover:
            pygame.draw.rect(pygame.display.get_surface(), self.color, [self.x * bit_width, self.y * bit_height, bit_width, bit_height])
        else:
            pygame.draw.rect(pygame.display.get_surface(), self.color, [self.x * bit_width, self.y * bit_height, bit_width, bit_height])