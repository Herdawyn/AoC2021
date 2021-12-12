from os import read
import time
import numpy as np
from collections import Counter

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap


day = "12"
# source = input or example
source = "example2"
source = "input"
input_file = "./day{}/{}".format(day, source)
data = []
caves = {}
small_caves = set()
starter = set(['start'])

with open(input_file, 'r') as file:
    for line in file:
        a, b = line.strip().split('-')
        caves[a] = caves.get(a, set())
        caves[a].add(b)
        caves[b] = caves.get(b, set())
        caves[b].add(a)
        for c in [a, b]:
            if c.islower():
                small_caves.add(c)

def flatten(A):
    rt = []
    for i in A:
        if isinstance(i,list): rt.extend(flatten(i))
        else: rt.append(i)
    return rt

def check_small_one_execption_max(path):
    counters = Counter(path)
    exception = Counter({k: c for k, c in counters.items() if (c > 1 and k.islower())})
    return exception == Counter()

def explore_further(current_place, caves, path, twice_one_small):
    more_paths = []
    path.append(current_place)
    path_set= set(path)
    if twice_one_small and check_small_one_execption_max(path):
        next_caves = caves[current_place] - starter
    else:
        next_caves = caves[current_place] - (small_caves & path_set) - starter
    for next_cave in next_caves:
        extra_path = path.copy()
        if next_cave == "end":
            extra_path.append(next_cave)
            more_paths.append(extra_path)
        else:
            recuriv_path = explore_further(next_cave, caves, extra_path, twice_one_small)
            if recuriv_path: more_paths= more_paths + recuriv_path
    if more_paths:
        return more_paths

@timing
def find_paths(caves, small_caves, twice_one_small=False):
    return explore_further("start", caves, [], twice_one_small)


# # Part 1
all_paths = find_paths(caves, small_caves)
print("Part 1: There are {} paths going throught small caves at most once".format(len(all_paths)))

# # Part 2
all_paths_allow_one_twice = find_paths(caves, small_caves, True)
print("Part 2: There are {} paths going throught small caves at most once with one may be twice".format(len(all_paths_allow_one_twice)))
