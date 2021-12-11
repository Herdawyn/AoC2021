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


def trigger_flashes(cave):
    cave = cave + 1
    accounted_flashes = np.full(cave.shape, False, dtype=bool)
    count_flashes = np.count_nonzero(cave > 9)
    new_flashes_count = 0
    xmax = len(cave[0])
    ymax = len(cave)
    while count_flashes != new_flashes_count:
        count_flashes = np.count_nonzero(cave > 9)
        for (x, y), octopus in np.ndenumerate(cave):
            if octopus > 9 and not accounted_flashes[x][y]:
                accounted_flashes[x][y]=True
                # Avoid stepping out of cave
                xrange = np.arange(max(0, x-1), min(xmax, x+2), 1)
                yrange = np.arange(max(0, y-1), min(ymax, y+2), 1)
                for x2, y2 in np.array(np.meshgrid(xrange, yrange)).T.reshape(-1, 2):
                    cave[x2][y2] += 1
        new_flashes_count = np.count_nonzero(cave > 9)
    return cave, new_flashes_count

@timing
def do_steps(cave, n_steps):
    flash_counter = []
    for i in range(n_steps):
        new_cave, count_flashes = trigger_flashes(cave)
        new_cave = np.where(new_cave > 9, 0, new_cave)
        cave = new_cave
        flash_counter.append(count_flashes)
    return new_cave, flash_counter

@timing
def get_simultaneous_flash(cave, max_steps):
    total_flash = np.count_nonzero(cave > -1)
    for i in range(max_steps):
        new_cave, count_flashes = trigger_flashes(cave)
        if count_flashes == total_flash:
            return i+1
        new_cave = np.where(new_cave > 9, 0, new_cave)
        cave = new_cave
    return None


day = "11"
# source = input or example
source = "example2"
source = "input"
input_file = "./day{}/{}".format(day, source)
lines = []
coords = None

with open(input_file, 'r') as file:
    data = file.read().splitlines()
    cave = np.array([], np.int32)
    w, h = len(data[0]), len(data)
    for row in data:
        row = np.array(list(row)).astype(int)
        cave = np.concatenate((cave, row), axis=0)
cave = cave.reshape(w, h)

# Part 1
steps = 100
final_cave, flashes = do_steps(cave, steps)
print("Part 1: Flashes for {} steps are {}".format(steps, sum(flashes)))

# Part 2
time_full_flash = get_simultaneous_flash(cave, 500)
print("Part 2: Full flash happens after step {}".format(time_full_flash))
