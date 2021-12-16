from os import read
import time
import numpy as np

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap


day = "15"
# source = input or example
source = "example"
source = "input"
input_file = "./day{}/{}".format(day, source)
data = []

with open(input_file, 'r') as file:
    data = file.read().splitlines()

cavern = np.asarray([list(map(int, list(line))) for line in data])

class Position():
    def __init__(self, x, y, cost=None, best_cost=None):
        self.neighbors = set()
        self.x = x
        self.y = y
        self.cost = cost
        self.best_cost = best_cost
        self.received = set()

    def get_cost(self):
        return self.cost

    def add_neighbor(self, n):
        self.neighbors.add(n)
    
    def add_received(self, received_cost):
        self.received.add(received_cost)

    def inform_neighbors(self, best_cost):
        for n in self.neighbors:
            n.add_received(best_cost)

    def update_costs(self):
        while self.received:
            received_cost = self.received.pop()
            if not(self.best_cost) or self.best_cost > self.cost + received_cost:
                self.best_cost = self.cost + received_cost
                self.inform_neighbors(self.best_cost)

def build_map(cave):
    cave_size = len(cave)
    cave_map = [ [ None for y in range(cave_size) ] for x in range(cave_size) ]

    for x in range(cave_size):
        for y in range(cave_size):
            cave_map[x][y] = Position(x, y, cave[x, y])

    for x in range(cave_size):
        for y in range(cave_size):
            for sx, sy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                dx, dy = x + sx, y + sy
                if dx >= 0 and dx < cave_size and dy >= 0 and dy < cave_size:
                    cave_map[x][y].add_neighbor(cave_map[dx][dy])
    return cave_map

def propagate(cave, steps):
    map = build_map(cave)
    map[-1][-1].add_received(0)
    map[-1][-1].update_costs()
    for a in range(steps):
        for x in reversed(range(len(map))):
            for y in reversed(range(len(map))):
                map[x][y].update_costs()
    return map

def build_full_map(cave, multiplier):
    single_size = len(cave)
    full_size = single_size * multiplier
    full_map = np.zeros((full_size, full_size), dtype=int)
    for i in range(multiplier):
        for j in range(multiplier):
            full_map[i*single_size:(i+1)*single_size, j *
                     single_size:(j+1)*single_size] = cave + i + j
    # max(i + j) = 8 no need to apply %10 //10 more than once
    full_map = np.where(full_map >= 10, full_map %
                        10 + full_map // 10, full_map)
    return full_map

@timing
def find_lowest_cost(cave):
    cave_map = propagate(cave, 5)
    return cave_map[0][0].best_cost - cave_map[0][0].get_cost()    

@timing
def find_lowest_cost_full_cave(cave, multiplier):
    full_cave = build_full_map(cave, multiplier)
    cave_map = propagate(full_cave, 10)
    return cave_map[0][0].best_cost - cave_map[0][0].get_cost()

# Part 1
lowest_cost = find_lowest_cost(cavern)
print("Part 1: Lowest path costs {}".format(lowest_cost))

# Part 2
lowest_cost_full_map = find_lowest_cost_full_cave(cavern, 5)
print("Part 1: Lowest path costs fo full cave {}".format(lowest_cost_full_map))
