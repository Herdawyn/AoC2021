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

cavern = ([list(map(int, list(line))) for line in data])

@timing
def find_lowest_cost(cave):
    costs = np.asarray(cave)
    for i in range(len(cave)):
        for j in range(len(cave)):
            left = costs[i-1, j] if i > 0 else 0
            up = costs[i, j-1] if j > 0 else 0
            best_cost = max(
                left, up) if left == 0 or up == 0 else min(left, up)
            costs[i, j] = costs[i, j] + best_cost
    return costs[-1, -1] - costs[0, 0]

def build_full_map(cave, multiplier):
    single_map = np.asarray(cave)
    single_size = len(single_map)
    full_size = single_size * multiplier
    full_map = np.zeros((full_size, full_size), dtype=int)
    for i in range(multiplier):
        for j in range(multiplier):
            full_map[i*single_size:(i+1)*single_size, j*single_size:(j+1)*single_size] = single_map + i + j
    # max(i + j) = 8 no need to apply %10 //10 more than once
    full_map = np.where(full_map >= 10, full_map % 10 + full_map // 10, full_map)
    return full_map

def find_lowest_cost_full_cave(cave, multiplier):
    full_cave = build_full_map(cave, multiplier)
    return find_lowest_cost(full_cave)


# Part 1
lowest_cost = find_lowest_cost(cavern)
print("Part 1: Lowest path costs {}".format(lowest_cost))

# # Part 2
lowest_cost_full_map = find_lowest_cost_full_cave(cavern, 5)
print("Part 1: Lowest path costs fo full cave {}".format(lowest_cost_full_map))
