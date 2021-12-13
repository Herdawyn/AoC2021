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


day = "13"
# source = input or example
source = "example"
source = "input"
input_file = "./day{}/{}".format(day, source)
data = []
folds = []

def make_paper(points):
    points_shape = []
    points_shape.append(list(max(points, key=lambda point: point[0]))[0] + 1)
    points_shape.append(list(max(points, key=lambda point: point[1]))[1] + 1)
    paper = np.full(points_shape, False, dtype=bool)
    [paper.itemset(point, True) for point in points]
    return paper

@timing
def points_after_one_fold(points, folds):
    paper = make_paper(points)
    paper = folding(paper, folds[0])
    return paper

def folding(paper, one_fold):
    direction, number = one_fold
    if direction == "y":
        half_fold = np.flip(paper[number+1:,], 0)
        paper = paper[:number,:] | half_fold
    elif direction == "x":
        half_fold = np.flip(paper[:,number+1:], 1)
        paper = paper[:,:number] | half_fold        
    return paper

@timing
def complete_folding(points, folds):
    paper = make_paper(points)
    for fold in folds:
        paper = folding(paper, fold)
    return paper

with open(input_file, 'r') as file:
    for line in file:
        data.append(line.strip().split(','))

fold_index = data.index([''])

folds = [fold.split("=") for fold in [str(i[0]).replace('fold along ', '') for i in data[fold_index+1:]]]
folds = [tuple((a,int(b))) for a,b in folds]
points = frozenset([tuple((int(b), int(a))) for a,b in data[:fold_index]])


# Part 1
point_onefold = np.count_nonzero(points_after_one_fold(points, folds))
print("Part 1: There are {} points after first fold".format(point_onefold))

# Part 2
finished_paper = complete_folding(points, folds)
print("Part 2: folded paper is: ")
print(finished_paper.astype(int))
