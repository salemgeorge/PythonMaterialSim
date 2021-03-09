import pygame
import random
import math
import time

from classes import SandBit
from classes import DirtBit
from classes import SmokeBit
from classes import WaterBit
from classes import WallBit
from classes import WoodBit
from classes import GasBit
from classes import LavaBit
from classes import GlassBit

from functions import *
from colors import *

pygame.init()

screen_width = 500
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])

block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

done = False
clock = pygame.time.Clock()
score = 0

grid_width = 50
grid_height = 50
grid = [[-1 for i in range(grid_width)] for j in range(grid_height)]

bit_width = screen_width / grid_width
bit_height = screen_height / grid_height

mouseX = 0
mouseY = 0

cur_bit_selection = SandBit

font = pygame.font.SysFont('Calibri', 25, True, False)

while not done:
    # Event Logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                if not CheckBitExists(GetBit(mouseX, mouseY, grid)):
                    grid[mouseX][mouseY] = cur_bit_selection(mouseX, mouseY)
            elif pygame.mouse.get_pressed()[2]:
                grid[mouseX][mouseY] = -1
            elif pygame.mouse.get_pressed()[1]:
                bitBelowCursor = GetBit(mouseX, mouseY, grid)
                if CheckBitExists(bitBelowCursor) and bitBelowCursor.canBurn and not bitBelowCursor.GetSmokeCover():
                    bitBelowCursor.Ignite(grid)


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not CheckBitExists(GetBit(mouseX, mouseY, grid)):
                    grid[mouseX][mouseY] = cur_bit_selection(mouseX, mouseY)
            elif event.button == 2:
                bitBelowCursor = GetBit(mouseX, mouseY, grid)
                if CheckBitExists(bitBelowCursor) and bitBelowCursor.canBurn and not bitBelowCursor.GetSmokeCover():
                    bitBelowCursor.Ignite(grid)
            elif event.button == 3:
                grid[mouseX][mouseY] = -1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                cur_bit_selection = SandBit
            elif event.key == pygame.K_2:
                cur_bit_selection = DirtBit
            elif event.key == pygame.K_3:
                cur_bit_selection = SmokeBit
            elif event.key == pygame.K_4:
                cur_bit_selection = WaterBit
            elif event.key == pygame.K_5:
                cur_bit_selection = WallBit
            elif event.key == pygame.K_6:
                cur_bit_selection = WoodBit
            elif event.key == pygame.K_7:
                cur_bit_selection = GasBit
            elif event.key == pygame.K_8:
                cur_bit_selection = LavaBit
            elif event.key == pygame.K_9:
                cur_bit_selection = GlassBit

            if event.key == pygame.K_c:
                grid = [[-1 for i in range(grid_width)] for j in range(grid_height)]

    screen.fill(BLACK)

    # Game Logic
    mouseToGridCoords = MouseToGridCoords(pygame.mouse.get_pos(), bit_width, bit_height)

    mouseX = mouseToGridCoords[0]
    mouseY = mouseToGridCoords[1]

    for y in range(grid_width):
        for x in range(grid_height):
            if grid[x][y] != -1:

                bitToUpdate = grid[x][y]

                bitToUpdate.UpdateBitClock()
                new_pos = bitToUpdate.HandleBehaviour(grid, grid_width, grid_height)
                bitToUpdate.HandleSmokeCover(grid)

                if new_pos[0] != x or new_pos[1] != y:
                    if "MovedMultipleBits" in new_pos:
                        otherBitPos = new_pos[3].GetPos()
                        grid[otherBitPos[0]][otherBitPos[1]] = new_pos[3]

                        grid[new_pos[0]][new_pos[1]] = bitToUpdate
                    elif "BitDied" in new_pos:
                        if "ProduceSmoke" in new_pos:
                            grid[new_pos[0]][new_pos[1]] = SmokeBit(new_pos[0], new_pos[1])
                        else:
                            grid[new_pos[0]][new_pos[1]] = -1
                    else:
                        grid[new_pos[0]][new_pos[1]] = bitToUpdate
                        grid[x][y] = -1

                    bitToUpdate = grid[new_pos[0]][new_pos[1]]
                elif "BitDied" in new_pos:
                    if "ProduceSmoke" in new_pos:
                        grid[new_pos[0]][new_pos[1]] = SmokeBit(new_pos[0], new_pos[1])
                    else:
                        grid[new_pos[0]][new_pos[1]] = -1

                    bitToUpdate = -1

                if bitToUpdate != -1:
                    bitToUpdate.DrawSelf(bit_width, bit_height)


    selectedBitText = font.render(cur_bit_selection.name, True, WHITE)
    screen.blit(selectedBitText, [0, 0])

    pygame.draw.rect(screen, RED, [mouseX * bit_width, mouseY * bit_height, bit_width, bit_height])

    clock.tick(60)
    pygame.display.flip()