from queue import PriorityQueue


class Graph:
    def __init__(self, map: list):
        # Holds the map, will be used for height / width and potentially cost of tiles
        self.map = map
        # A dictionary that holds the edges for each given vertex / point on the map
        self.edges: dict = {}
        self.generateGraph(self.map)

    # Loops through the map and adds the neighbours the to the respective key / vertex
    def generateGraph(self, map):
        for y in range(0, len(map)):
            for x in range(0, len(map[0])):
                if not map[y][x].isCollidable():
                    self.edges[(y, x)] = self.neighbours([y, x])

    # Returns the neighbours of a given vertex (in 4 directions)
    def neighbours(self, vertex: list) -> list:
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for dir in dirs:
            neighbour = [vertex[0] + dir[0], vertex[1] + dir[1]]
            # Bounds the edges to within the map
            if 0 <= neighbour[0] < len(self.map) and 0 <= neighbour[1] < len(self.map[0]):
                if not self.map[vertex[0] + dir[0]][vertex[1] + dir[1]].isCollidable():
                    result.append((vertex[0] + dir[0], vertex[1] + dir[1]))
        return tuple(result)

    # Calculates the Manhattan distance
    def heuristic(self, source, target):
        y1, x1 = source
        y2, x2 = target
        return abs(x1 - x2) + abs(y1 - y2)

    def Astar(self, source, target):
        # This implementation uses a priority queue to determine the next
        # vertex to visit
        frontier = PriorityQueue()
        # Source is the first visited vertex
        frontier.put(source, 0)
        # Came_from holds the previously visited vertex to current
        came_from = {}
        # Cost_so_far is used alongside the heuristic to determine
        # The next vertex to visit
        cost_so_far = {}
        came_from[source] = None
        cost_so_far[source] = 0

        # While there are no more verticies to visit
        while not frontier.empty():
            current = frontier.get()
            if current == target:
                break

            for next in self.edges[current]:
                # No cost associated with tiles yet, to be implemented
                # later (so at the moment the function
                # performs more like Dijkstra than proper a*)
                new_cost = cost_so_far[current] + self.getCost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    # f(x) = g(x) + h(x)
                    priority = new_cost + self.heuristic(target, next)
                    frontier.put(next, priority)
                    came_from[next] = current
        return self.constructPath(came_from, source, target)

    def constructPath(self, came_from, source, target):
        current = target
        path = []
        # Once current is source the path has been reconstructed
        while current != source:
            path.append(current)
            current = came_from[current]
        # Path is constructed backwards
        path.reverse()
        return path

    def getCost(self, current, next):
        return abs(current[0] - next[0]) + abs(current[1] - next[1])
