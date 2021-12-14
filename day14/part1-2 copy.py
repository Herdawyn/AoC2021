from os import read
import time
from collections import Counter
from numpy.core.numeric import count_nonzero

from numpy.lib.polynomial import poly

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap


day = "14"
# source = input or example
source = "example"
source = "input"
input_file = "./day{}/{}".format(day, source)
data = []

with open(input_file, 'r') as file:
    data = file.read().splitlines()

template = data[0]
base_rules = [a.split(" -> ") for a in data[2:]]
rules = {rule[0]: "".join((rule[0][0], rule[1])) for rule in base_rules}
complement_rules = {rule[0]: "".join((rule[1], rule[0][1])) for rule in base_rules}
first_letter, last_letter = template[0], template[-1]

@timing
def get_result(polymer, steps):
    for step in range(steps):
        polymer = grow_polymer(polymer)
    counters = Counter(polymer)
    score = counters.most_common()[0][1]-counters.most_common()[-1][1]
    return score

def grow_polymer(polymer):
    new_polymers = []
    polymer_pairs = [polymer[i:i+2] for i in range(len(polymer)-1)]
    for pair in polymer_pairs:
        new_polymers.append(rules[pair])
    new_polymers.append(polymer[-1])
    return "".join(new_polymers)

def grow_polymer_fast(poly_counter):
    new_poly_counter = Counter()
    for k, v in poly_counter.items():
        new_poly_counter[rules[k]] = new_poly_counter.get(rules[k], 0) + v
        new_poly_counter[complement_rules[k]] = new_poly_counter.get(complement_rules[k], 0) + v
    return new_poly_counter

@timing
def get_result_fast(template, steps):
    base_polymer = []
    polymer_pairs = [template[i:i+2] for i in range(len(template)-1)]
    for pair in polymer_pairs:
        base_polymer.append(pair)
    p_counter = Counter(base_polymer)
    for step in range(steps):
        p_counter = grow_polymer_fast(p_counter)
    p_counter = atomize(p_counter)
    score = p_counter.most_common()[0][1]-p_counter.most_common()[-1][1]
    return score   

def atomize(pair_counter):
    atom = Counter()
    for k, v in pair_counter.items():
        for a,b in k.split():
            atom[a] += v
            atom[b] += v
    atom[first_letter] += 1
    atom[last_letter] += 1
    for k, v in atom.items():
        atom[k] = int(atom[k] / 2)
    return atom

# Part 1
steps = 10
polymer_result = get_result(template, steps)
print("Part 1: Polymer score is {}".format(polymer_result))

# Part 2
steps = 40
polymer_result2 = get_result_fast(template, steps)
print("Part 2: Strong Polymer score is {}".format(polymer_result2))