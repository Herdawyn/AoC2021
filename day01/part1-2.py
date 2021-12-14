input_file = "input"

def count_increasing(measures):
    increasing = []
    previous_measure = measures[0]
    for measure in measures:
        increasing.append(previous_measure < measure)
        previous_measure = measure
    return sum((p == True) for p in increasing), increasing

with open(input_file, 'r') as file:
    lines = file.readlines()
    depths = [int(line.rstrip()) for line in lines]

# Part 1
increasing_count, tests = count_increasing(depths)
print("There are {} times depth is increasing".format(increasing_count))

# Part 2
slices = []
for i in range(len(depths)-2):
    slices.append(sum(depths[i:i+3]))

slices_inc_count, tests = count_increasing(slices)
print("There are {} times slice depth is increasing".format(slices_inc_count))