from random import random

# Creates/Seeds a random 2D array with true or false values for alive or dead cells
def generateRandomList(width: int, height: int, chance: float) -> list:
    map = []
    for y in range(0, height):
        row = []
        for x in range(0, width):
            if random() < chance:
                tile = False
            else:
                tile = True
            row.append(tile)
        map.append(row)
    return map

# Iterates through each cell and determines whether it lives or dies and creates a new map based on this
def stepSimulation(map: list, deathLimit: int, birthLimit: int):
    newMap = map.copy()
    for y in range(0, len(map)):
        for x in range(0, len(map[0])):
            neighbours = countLivingNeighbours(map, x, y)
            if map[y][x]:
                if neighbours < deathLimit:
                    newMap[y][x] = False
                else:
                    newMap[y][x] = True
            else:
                if neighbours > birthLimit:
                    newMap[y][x] = True
                else:
                    newMap[y][x] = False
    return newMap
#Returns the number of neighbours a cell has, used for calculating whether a cell lives or dies
def countLivingNeighbours(map: list, x: int, y: int):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbourX = x + i
            neighbourY = y + j
            if i == 0 and j == 0:
                pass
            elif neighbourX < 0 or neighbourY < 0 or neighbourX >= len(map[0]) or neighbourY >= len(map):
                count += 1
            elif map[neighbourY][neighbourX]:
                count += 1
    return count

def generateCellMap(width: int = 50, height: int = 50,
                    chance: float = 0.6, steps: int = 6,
                    birthLimit: int = 3, deathLimit: int = 4) -> list:
    map = generateRandomList(width, height, chance)
    for i in range(0, steps+1):
        map = stepSimulation(map, birthLimit, deathLimit).copy()
    for each in map:
        print(each)

generateCellMap()