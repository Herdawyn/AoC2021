from os import read


def get_gama_rate(readings):
    bins = len(readings[0])
    values = [0] * bins
    for reading in readings:
        for i in range(bins):
            values[i] += reading[i]
    for i in range(bins):
        values[i] = round(values[i] / len(readings))        
    return values

def get_oxygen(readings, index):
    return get_life_support(readings, index, 1)

def get_dioxygen(readings, index):
    return get_life_support(readings, index, 0)

def get_life_support(readings, index, keep_equal):
    values = {
        0: [],
        1: []
    }
    if len(readings) == 1:
        return readings[0]
    
    for reading in readings:
        values[int(reading[index])].append(reading)
    
    zero_count = len(values[0])
    one_count = len(values[1])
    result = 0
    if (one_count > zero_count):
        result = 1
    else:
        result = 0
    if zero_count == one_count:
        result = keep_equal        
    elif keep_equal == 0:
        result = abs(result - 1)

    return get_life_support(values[result], index + 1, keep_equal)        

def get_beta(gamma):
    return [abs(int(b)-1) for b in gamma]

def list2dec(value):
    decimal = 0
    for digit in value:
        decimal = (decimal * 2) + digit
    return decimal

day = "03"
# source = input or example
source = "input"
input_file = "./day{}/{}".format(day, source)
readings = []
with open(input_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        readings.append([int(r) for r in line.strip()])

# Part 1
gamma = get_gama_rate(readings)
beta = list2dec(get_beta(gamma))
gamma = list2dec(gamma)
power = gamma * beta
print("gamma: {} beta: {} power: {}".format(gamma, beta, power))

# Part 2
o2 = get_oxygen(readings, 0)
co2 = list2dec(get_dioxygen(readings, 0))
o2 = list2dec(o2)
lf_rating = o2 * co2
print("o2: {} co2: {} life_rating: {}".format(o2,co2,lf_rating))