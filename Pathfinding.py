import math
class Graph:
    def __init__(self, map: list):
        #Holds the map, will be used for height / width and potentially cost of tiles
        self.map = map
        #A dictionary that holds the edges for each given vertex / point on the map
        self.edges: dict = {}

    #Loops through the map and adds the neighbours the to the respective key / vertex
    def generateGraph(self, map):
        for y in range(0, len(map)):
            for x in range(0, len(map[0])):
                self.edges[(y,x)] = self.neighbours([y,x])

    #Returns the neighbours of a given vertex (in 4 directions)
    def neighbours(self, vertex: list) -> list:
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for dir in dirs:
            neighbour = [vertex[0] + dir[0], vertex[1] + dir[1]]
            # Bounds the edges to within the map
            if 0 <= neighbour[0] < len(self.map) and 0 <= neighbour[1] < len(self.map[0]):
                result.append([vertex[0] + dir[0], vertex[1] + dir[1]])
        return tuple(result)

    # Calculates the Manhattan distance
    def heuristic(self, source, target):
        y1, x1 = source
        y2, x2 = target
        return abs(x1 - x2) + abs(y1 - y2)

    def Astar(self):
        pass

test = [['.', '.', '.'],
        ['.', '.', '.'],
        ['.', '.', '.'],
        ['.', '.', '.']]

testg = Graph(test)
testg.generateGraph(test)
for each in testg.edges:
    print(each, ':', testg.edges[each])