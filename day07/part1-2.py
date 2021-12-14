from os import read
import statistics

day = "07"
# source = input or example
source = "example"
source = "input"
input_file = "./day{}/{}".format(day, source)
crabs = []
with open(input_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        crabs = [int(f) for f in line.strip().split(",")]

def needed_fuel(positions, destination):
    fuel = 0
    for pos in positions:
        fuel += abs(destination - pos)
    return fuel

def needed_fuel_part2(positions, destination):
    fuel = 0
    for pos in positions:
        moves = abs(destination - pos)
        fuel += (moves + 1) * moves / 2 
    return fuel

def compute_fuels(positions):
    max_pos = max(positions)
    costs = []
    for i in range(max_pos + 1):
        costs.append(needed_fuel_part2(positions, i))
    return costs


# Part 1
med_pos = round(statistics.median(crabs))
print("Mediane position: ", med_pos)
fuel = needed_fuel(crabs, med_pos)
print("Needed fuel: ", fuel)

# Part 2
mean_pos = statistics.mean(crabs)
print("Mean position: ", mean_pos)
fuels = compute_fuels(crabs)
print("Best position: {} Needed fuel: {}".format(fuels.index(min(fuels)), min(fuels)))
