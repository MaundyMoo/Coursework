'''
Interfaces with map generation algorithms to produce tilemaps
'''
from random import choice

import CellularAutomata
import Image
import Tiles

spritesheet = Image.SpriteSheet(path="res/testSheet.png", spriteSize=32)


def generateCellularAutomata(width: int = 40,
                             height: int = 30,
                             chance: float = 0.65,
                             steps: int = 2,
                             birthLimit: int = 3,
                             deathLimit: int = 4) -> list:
    '''Returns a tilemap from the CellularAutomata method'''
    arr, caverns = CellularAutomata.driver(width, height, chance, steps, birthLimit, deathLimit)

    tileMap = []
    # Iterates over the 2D list returned by the cellauto algorithm
    # and places a non collidable tile at a true value, and a collidable
    # tile at the false values
    for y in range(0, len(arr)):
        row = []
        for x in range(0, len(arr[0])):
            if arr[y][x] == True:
                row.append(Tiles.Tile(gridPos=(x, y),
                                      collision=False,
                                      sprite=spritesheet.returnSprite(0, 0)))
            elif arr[y][x] == False:
                row.append(Tiles.Tile(gridPos=(x, y),
                                      collision=True,
                                      sprite=spritesheet.returnSprite(1, 0)))
            '''
            elif arr[y][x] == 'corridoor':
                row.append(Tiles.Tile(gridPos=(x, y),
                                      collision=False,
                                      sprite=spritesheet.returnSprite(0, 2)))
            '''
        tileMap.append(row)
    y, x = choice(caverns[-1])
    tileMap[y][x] = Tiles.LevelTile(gridPos = (x, y), sprite = spritesheet.returnSprite(0, 2))
    return tileMap, caverns


def placeEnemiesCellular(caverns) -> list:
    positions = []
    for cavern in caverns:
        for i in range(0, len(cavern) // 30):
            location = choice(cavern)
            if not location in positions:
                positions.append(location)
    return positions