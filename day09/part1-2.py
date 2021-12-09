from os import read
import numpy as np
import time

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

class Cave:
    def __init__(self, length):
        self.data = []
        self.cave = np.array([])
        self.horizontal = np.array([])
        self.vertical = np.array([])
        self.low_points = np.array([])
        self.limits = np.array([])

    def add_row(self, row):
        self.data.append(row)
        self.cave = np.array(self.data, dtype=int)

    def find_limits(self):
        lava_cave = np.hstack((self.cave, np.full((self.cave.shape[0], 2), 9)))
        lava_cave = np.vstack((lava_cave, np.full((2, lava_cave.shape[1]), 9)))
        lava_cave = np.roll(lava_cave, shift=1, axis=1)
        lava_cave = np.roll(lava_cave, shift=1, axis=0)
        self.limits = lava_cave < 9

    def compare_positions(self):
        horizontal_right = self.cave < np.roll(self.cave, shift=-1, axis=1)
        horizontal_right[:, -1] = True
        horizontal_left = self.cave < np.roll(self.cave, shift=+1, axis=1)
        horizontal_left[:, -0] = True
        horizontal = np.logical_and(horizontal_left, horizontal_right)
        vertical_down= self.cave < np.roll(self.cave, shift=-1, axis=0)
        vertical_down[-1, :] = True        
        vertical_up = self.cave < np.roll(self.cave, shift=+1, axis=0)
        vertical_up[0, :] = True        
        vertical = np.logical_and(vertical_down, vertical_up)
        self.low_points = np.logical_and(horizontal, vertical)

    def find_neighbors(self, i, j):
        neighbors = []
        size = 0
        for k, l in ([-1, 0], [1, 0], [0, -1], [0, 1]):
            if self.limits[i+k,j+l]:
                size += 1
                neighbors.append([i+k,j+l])
                self.limits[i+k,j+l] = False
        for x, y in neighbors:
            size += self.find_neighbors(x,y)
        return size

    @timing    
    def sum_risks(self):
        self.compare_positions()
        return sum(self.cave[np.where(self.low_points)]+1)

    @timing
    def count_basins(self):
        basins = []
        self.find_limits()
        lowest_points = zip(*np.where(self.low_points))
        for i, j in lowest_points:
            # print(self.limits)
            self.limits[i+1,j+1] = False
            basin_size = 1 + self.find_neighbors(i+1, j+1)
            basins.append(basin_size)
        return np.prod(sorted(basins, reverse=True)[0:3])

day = "09"
# source = input or example
source = "example"
source = "input"
input_file = "./day{}/{}".format(day, source)
digits = []

with open(input_file, 'r') as file:
    data = file.read().splitlines()
    cave = Cave(len(data[0]))
    for row in data:
        row = list(map(int,list(row)))
        cave.add_row(row)

# Part 1
risks = cave.sum_risks()
print("Part 1: Sum of risks is {}".format(risks))

# Part 2
large_basins = cave.count_basins()
print("Part 2: Product of largest basins {}".format(large_basins))