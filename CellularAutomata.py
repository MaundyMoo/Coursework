from random import random, choice
import queue
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

def countCaverns(map: list):
    caverns = []
    for y in range(0, len(map)):
        for x in range(0, len(map[0])):
            # Checks if the cell is True and not already in a cavern
            if map[y][x] and not any((y,x) in cavern for cavern in caverns):
                # Perform the flood fill / BFS
                caverns.append(IterativeBFS((y, x), map))
            else:
                # Already counted cell so ignore or the cell is 'dead'
                continue
    return caverns

def IterativeBFS(point: tuple, map: list):
    q = queue.Queue()
    q.put(point)
    cavern = []
    while not q.empty():
        (y, x) = q.get()
        if not (y, x) in cavern:
            cavern.append((y, x))

            if not y == len(map)-1:
                if map[y + 1][x] and not (y + 1, x) in cavern:
                    q.put((y + 1, x))

            if not y == 0:
                if map[y - 1][x] and not (y - 1, x) in cavern:
                    q.put((y - 1, x))

            if not x == len(map[0])-1:
                if map[y][x + 1] and not (y, x + 1) in cavern:
                    q.put((y, x + 1))

            if not x == 0:
                if map[y][x - 1] and not (y, x - 1) in cavern:
                    q.put((y, x - 1))
    return cavern

def placeCorridors(map: list, caverns: list):
    if len(caverns) > 1:
        for i in range(0, len(caverns)-1):
            y1, x1 = choice(caverns[i])
            y2, x2 = choice(caverns[i+1])
            # Connect on x axis
            if x1 < x2:
                for i in range(x1, x2 + 1):
                    map[y1][i] = 'corridoor'
            elif x1 > x2:
                for i in range(x2, x1 + 1):
                    map[y1][i] = 'corridoor'
            if y1 < y2:
                for i in range(y1, y2 + 1):
                    map[i][x2] = 'corridoor'
            elif y1 > y2:
                for i in range(y2, y1 + 1):
                    map[i][x2] = 'corridoor'
    return map

def driver(width: int, height: int,
           chance: float, steps: int,
           birthLimit: int, deathLimit: int) -> list:
    map = generateRandomList(width, height, chance)
    for i in range(0, steps):
        map = stepSimulation(map, birthLimit, deathLimit).copy()
    caverns = countCaverns(map)
    print(caverns)
    print(len(caverns))
    map = placeCorridors(map, caverns)
    return map