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

    bitsToFallThrough = ["Water", "Smoke", "Gas", "Lava", "Water Vapor"]

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

    bitsToFallThrough = ["Water", "Smoke", "Gas", "Lava", "Water Vapor"]

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

    bitsToFallThrough = ["Water Vapor"]

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

            if random.random() < 0.1:
                self.randColor = RandomizeColor(50, 50, 50, 60, 60, 60)
                self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

            bitUp = GetBit(self.x, self.y - 1, grid)

            if CheckBitExists(bitUp):
                if bitUp.GetName() in self.bitsToFallThrough:
                    newPos = SwapBits([self.x, self.y], bitUp.GetPos(), grid)
                    return [newPos[0], newPos[1], "MovedMultipleBits", newPos[2]]
                else:
                    bitLeft = GetBit(self.x - 1, self.y, grid)
                    bitRight = GetBit(self.x + 1, self.y, grid)

                    canMoveLeftDetails = CheckCanMoveWaterSide(bitLeft, self.bitsToFallThrough)
                    canMoveRightDetails = CheckCanMoveWaterSide(bitRight, self.bitsToFallThrough)

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

                    self.fallProgress = 0 
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

    bitsToFallThrough = ["Water Vapor"]

    name = "Water"

    canBurn = False

    canHaveSmokeCover = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # min = 32, 110, 127
        # max = 32, 158, 181
        self.randColor = RandomizeColor(36, 174, 140, 36, 200, 200)
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

            if random.random() < 0.08:
                self.randColor = RandomizeColor(36, 174, 140, 36, 200, 200)
                self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

            bitDown = -2
            if self.y + 1 <= grid_height - 1:
                bitDown = GetBit(self.x, self.y + 1, grid)

            if bitDown != -2 and bitDown != -1:
                if bitDown.GetName() in self.bitsToFallThrough:
                    self.fallProgress = 0
                    newPos = SwapBits([self.x, self.y], bitDown.GetPos(), grid)
                    return [newPos[0], newPos[1], "MovedMultipleBits", newPos[2]]
                else:
                    bitLeft = GetBit(self.x - 1, self.y, grid)
                    bitRight = GetBit(self.x + 1, self.y, grid)

                    canMoveLeftDetails = CheckCanMoveWaterSide(bitLeft, self.bitsToFallThrough)
                    canMoveRightDetails = CheckCanMoveWaterSide(bitRight, self.bitsToFallThrough)

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

                    self.fallProgress = 0 
                    return [self.x, self.y]

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

    bitsToFallThrough = ["Water", "Water Vapor"]

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
            if CheckBitExists(bitDown) and bitDown.GetName() in self.bitsToFallThrough:
                newPos = SwapBits([self.x, self.y], bitDown.GetPos(), grid)
                return [newPos[0], newPos[1], "MovedMultipleBits", newPos[2]]

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

    bitsToFallThrough = ["Water Vapor"]

    canBurn = False

    canHaveSmokeCover = False

    bitHealth = 10
    bitLife = 225

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
            self.fallProgress = 0
            if GetBit(self.x, self.y - 1, grid) == -1:
                self.bitLife -= 1
                if self.bitLife <= 0:
                    return [self.x, self.y, "LavaCooled"]

            bitsAround = GetBitsAround(self.x, self.y, grid)

            if random.random() < 0.1:
                self.randColor = RandomizeColor(150, 0, 0, 255, 0, 0)
                self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

            if not CheckBitExists(GetBit(self.x, self.y - 1, grid)) and random.random() < 0.005:
                SetBit(SmokeBit(self.x, self.y - 1), self.x, self.y - 1, grid)

            bitLeft = bitsAround[8][3]
            bitRight = bitsAround[8][4]
            bitDown = bitsAround[8][6]
            bitUp = bitsAround[8][1]

            if CheckBitExists(bitLeft):
                if bitLeft.GetName() in self.bitsToEvaporate:
                    SetBit(WaterVaporBit(self.x - 1, self.y), self.x - 1, self.y, grid)
                    self.bitHealth -= 1
                elif bitLeft.GetName() in self.bitsToGlass:
                    SetBit(GlassBit(self.x - 1, self.y), self.x - 1, self.y, grid)
                    self.bitHealth -= 1
                if self.bitHealth <= 0:
                    return [self.x, self.y, "LavaCooled"]

            if CheckBitExists(bitRight):
                if bitRight.GetName() in self.bitsToEvaporate:
                    SetBit(WaterVaporBit(self.x + 1, self.y), self.x + 1, self.y, grid)
                    self.bitHealth -= 1
                elif bitRight.GetName() in self.bitsToGlass:
                    SetBit(GlassBit(self.x + 1, self.y), self.x + 1, self.y, grid)
                    self.bitHealth -= 1
                if self.bitHealth <= 0:
                    return [self.x, self.y, "LavaCooled"]

            if CheckBitExists(bitUp):
                if bitUp.GetName() in self.bitsToEvaporate:
                    SetBit(WaterVaporBit(self.x, self.y - 1), self.x, self.y - 1, grid)
                    self.bitHealth -= 1
                elif bitUp.GetName() in self.bitsToGlass:
                    SetBit(GlassBit(self.x, self.y - 1), self.x, self.y - 1, grid)
                    self.bitHealth -= 1
                if self.bitHealth <= 0:
                    return [self.x, self.y, "LavaCooled"]

            if CheckBitExists(bitDown):
                if bitDown.GetName() in self.bitsToEvaporate:
                    SetBit(WaterVaporBit(self.x, self.y + 1), self.x, self.y + 1, grid)
                    self.bitHealth -= 1
                    if self.bitHealth <= 0:
                        return [self.x, self.y, "LavaCooled"]
                elif bitDown.GetName() in self.bitsToGlass:
                    SetBit(GlassBit(self.x, self.y + 1), self.x, self.y + 1, grid)
                    self.bitHealth -= 1
                    if self.bitHealth <= 0:
                        return [self.x, self.y, "LavaCooled"]
                elif bitDown.GetName() in self.bitsToFallThrough:
                    newPos = SwapBits([self.x, self.y], bitDown.GetPos(), grid)
                    return [newPos[0], newPos[1], "MovedMultipleBits", newPos[2]]
                else:

                    canMoveLeftDetails = CheckCanMoveWaterSide(bitLeft, self.bitsToFallThrough)
                    canMoveRightDetails = CheckCanMoveWaterSide(bitRight, self.bitsToFallThrough)

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

                    self.fallProgress = 0 
                    return [self.x, self.y]

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

    name = "Glass"

    canBurn = False

    bitsToFallThrough = ["Water", "Smoke", "Gas", "Lava", "Water Vapor"]

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
        self.randColor = RandomizeColor(230, 230, 230, 255, 255, 255)
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

    def DrawSelf(self, bit_width, bit_height, screen):
        if not self.hasSmokeCover:
            s = pygame.Surface((bit_width, bit_height))
            s.set_alpha(128)
            s.fill(self.color)
            screen.blit(s, (self.x * bit_width, self.y * bit_height))
        else:
            pygame.draw.rect(pygame.display.get_surface(), self.color, [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class WaterVaporBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 3
    fallProgress = 0

    name = "Water Vapor"

    canBurn = False

    canHaveSmokeCover = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # min = 35, 33, 33
        # max = 72, 69, 68
        self.randColor = RandomizeColor(36, 174, 140, 36, 200, 200)
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

            if random.random() < 0.08:
                self.randColor = RandomizeColor(36, 174, 140, 36, 200, 200)
                self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

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

    def DrawSelf(self, bit_width, bit_height, screen):
        s = pygame.Surface((bit_width, bit_height))
        s.set_alpha(128)
        s.fill(self.color)
        screen.blit(s, (self.x * bit_width, self.y * bit_height))
        # pygame.draw.rect(pygame.display.get_surface(), self.color,
        #                  [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class StoneBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 2
    fallProgress = 0

    name = "Stone"

    canBurn = False

    bitsToFallThrough = ["Water", "Smoke", "Gas", "Lava", "Water Vapor"]

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
        self.randColor = RandomizeColor(60, 60, 60, 65, 70, 65)
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
            bitDown = GetBit(self.x, self.y + 1, grid)
            bitLeft = GetBit(self.x - 1, self.y, grid)
            bitRight = GetBit(self.x + 1, self.y, grid)

            isWaterDown = CheckBitExists(bitDown) and bitDown.GetName() in self.bitsToFallThrough
            
            if not isWaterDown and CheckBitExists(bitDown):
                downDistLeft = 1
                downDistRight = 1

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
        if not self.hasSmokeCover:
            pygame.draw.rect(pygame.display.get_surface(), self.color, [self.x * bit_width, self.y * bit_height, bit_width, bit_height])
        else:
            pygame.draw.rect(pygame.display.get_surface(), self.color, [self.x * bit_width, self.y * bit_height, bit_width, bit_height])

class TNTBit():
    x = -1
    y = -1

    randColor = -1
    color = -1

    fallSpeed = 4
    fallProgress = 0

    bitsToFallThrough = ["Water", "Water Vapor"]

    name = "TNT"

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
        if self.fallProgress >= self.fallSpeed:
            self.fallProgress = 0

            bitDown = GetBit(self.x, self.y + 1, grid)
            if CheckBitExists(bitDown) and bitDown.GetName() in self.bitsToFallThrough:
                newPos = SwapBits([self.x, self.y], bitDown.GetPos(), grid)
                return [newPos[0], newPos[1], "MovedMultipleBits", newPos[2]]

            adjacentBits = GetAdjacentBits(self.x, self.y, grid, grid_width, grid_height)

            if self.isBurning:
                if random.random() <= 0.1:
                    self.randColor = RandomizeColor(160, 50, 20, 191, 60, 30)
                    self.color = (self.randColor[0], self.randColor[1], self.randColor[2])
                if self.bitHealth > 0:
                    randChance = random.random()

                    # if randChance <= 0.50:
                    #     randDir = random.random()
                    #     if randDir >= 0 and randDir <= 0.25 and CheckBitExists(adjacentBits[4][0]) and adjacentBits[4][0].GetName() == "TNT":
                    #         adjacentBits[4][0].Ignite(grid)
                    #     elif randDir > 0.25 and randDir <= 0.50 and CheckBitExists(adjacentBits[4][1]) and adjacentBits[4][1].GetName() == "TNT":
                    #         adjacentBits[4][1].Ignite(grid)
                    #     elif randDir > 0.50 and randDir <= 0.75 and CheckBitExists(adjacentBits[4][2]) and adjacentBits[4][2].GetName() == "TNT":
                    #         adjacentBits[4][2].Ignite(grid)
                    #     elif CheckBitExists(adjacentBits[4][3]) and adjacentBits[4][3].GetName() == "TNT":
                    #         adjacentBits[4][3].Ignite(grid)

                    if self.y - 1 >= 0 and randChance <= 0.1:
                        bitAbove = GetBit(self.x, self.y - 1, grid)
                        if not CheckBitExists(bitAbove):
                            SetBit(SmokeBit(self.x, self.y - 1), self.x, self.y - 1, grid)
                        elif CheckBitExists(bitAbove) and bitAbove.canHaveSmokeCover:
                            GetBit(self.x, self.y - 1, grid).SetSmokeCover(True)

                    self.randColor = RandomizeColor(160, 50, 20, 191, 60, 30)
                    self.color = (self.randColor[0], self.randColor[1], self.randColor[2])

                    self.bitHealth -= 1
                    if self.bitHealth <= 0:
                        self.bitHealth = -1

                        return [self.x, self.y, "Exploded", 4]

                    return [self.x, self.y]

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