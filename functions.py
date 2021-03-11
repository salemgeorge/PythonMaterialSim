import random

def MouseToGridCoords(mousePos, bit_width, bit_height):
    posX = mousePos[0]
    posY = mousePos[1]

    gridX = round(posX / bit_width)
    gridY = round(posY / bit_height)

    return [gridX, gridY]


def GetBit(x, y, grid):
    xValid = x >= 0 and x < len(grid[0])
    yValid = y >= 0 and y < len(grid[0])

    if xValid and yValid:
        return grid[x][y]
    else:
        return -2



def GetBitExists(x, y, grid):
    xValid = x >= 0 and x <= len(grid[0]) - 1
    yValid = y >= 0 and y <= len(grid[0]) - 1

    if xValid and yValid:
        if grid[x][y] == -1:
            return False
        else:
            return True
    else:
        return -2

    return grid[x][y]


def SetBit(bit, x, y, grid):
    grid[x][y] = bit


def DeleteBit(bit, grid):
    bitPos = bit.GetPos()
    grid[bitPos[0]][bitPos[1]] = -1


def GetAdjacentBits(x, y, grid, grid_width, grid_height):
    bits = [-2, -2, -2, -2, [-2, -2, -2 ,-2]]

    xLeft = x - 1
    xRight = x + 1

    yUp = y - 1
    yDown = y + 1

    if xLeft < 0:
        bits[0] = -1
    else:
        bitLeft = GetBit(xLeft, y, grid)
        if bitLeft == -1:
            bits[0] = False
        else:
            bits[0] = True
            bits[4][0] = bitLeft

    if xRight > grid_width - 1:
        bits[1] = -1
    else:
        bitRight = GetBit(xRight, y, grid)
        if bitRight == -1:
            bits[1] = False
        else:
            bits[1] = True
            bits[4][1] = bitRight

    if yUp < 0:
        bits[2] = -1
    else:
        bitUp = GetBit(x, yUp, grid)
        if bitUp == -1:
            bits[2] = False
        else:
            bits[2] = True
            bits[4][2] = bitUp

    if yDown > grid_height - 1:
        bits[3] = -1
    else:
        bitDown = GetBit(x, yDown, grid)
        if bitDown == -1:
            bits[3] = False
        else:
            bits[3] = True
            bits[4][3] = bitDown

    return bits

def GetBitsAround(x, y, grid):
    bits = [-2, -2, -2, -2, -2, -2, -2, -2, [-2, -2, -2, -2, -2, -2, -2, -2]]

    bits[0] = GetBitExists(x - 1, y - 1, grid)
    bits[8][0] = GetBit(x - 1, y - 1, grid)

    bits[1] = GetBitExists(x, y - 1, grid)
    bits[8][1] = GetBit(x, y - 1, grid)

    bits[2] = GetBitExists(x + 1, y - 1, grid)
    bits[8][2] = GetBit(x + 1, y - 1, grid)

    bits[3] = GetBitExists(x - 1, y, grid)
    bits[8][3] = GetBit(x - 1, y, grid)

    bits[4] = GetBitExists(x + 1, y, grid)
    bits[8][4] = GetBit(x + 1, y, grid)

    bits[5] = GetBitExists(x - 1, y + 1, grid)
    bits[8][5] = GetBit(x - 1, y + 1, grid)

    bits[6] = GetBitExists(x, y + 1, grid)
    bits[8][6] = GetBit(x, y + 1, grid)

    bits[7] = GetBitExists(x + 1, y + 1, grid)
    bits[8][7] = GetBit(x + 1, y + 1, grid)

    return bits

def GetBitToSide(x, y, xDist, yDist, grid):
    bit = GetBit(x + xDist, y + yDist, grid)
    return bit


def GenerateChance(chance):
    randChance = random.random()

    if randChance <= chance:
        return True
    elif randChance > chance:
        return False

def CheckCanMoveWater(sideBitDown, sideBit, bitsToFallThrough):
    canMove = False
    isWater = False

    if sideBitDown == -1 and sideBit == -1:
        canMove = True
        return [canMove, isWater]

    if CheckBitExists(sideBitDown) and sideBitDown.GetName() in bitsToFallThrough:
        if CheckBitExists(sideBit) and sideBit.GetName() in bitsToFallThrough:
            canMove = True
            isWater = True
            return [canMove, isWater]

    return [canMove, isWater]

def CheckCanMoveWaterSide(sideBit, bitsToFallThrough):
    canMove = False
    isWater = False

    if sideBit == -1:
        canMove = True
        return [canMove, isWater]

    if CheckBitExists(sideBit) and sideBit.GetName() in bitsToFallThrough:
        canMove = True
        isWater = True
        return [canMove, isWater]

    return [canMove, isWater]

def CheckBitExists(bit):
    if bit != -1 and bit != -2:
        return True
    else:
        return False

def SwapBits(bitOnePos, bitTwoPos, grid):
    bitOne = GetBit(bitOnePos[0], bitOnePos[1], grid)
    bitTwo = GetBit(bitTwoPos[0], bitTwoPos[1], grid)

    bitOne.SetPos(bitTwoPos[0], bitTwoPos[1])
    bitTwo.SetPos(bitOnePos[0], bitOnePos[1])

    return [bitTwoPos[0], bitTwoPos[1], bitTwo]