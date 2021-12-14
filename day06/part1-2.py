from os import read


day = "06"
# source = input or example
source = "input"
input_file = "./day{}/{}".format(day, source)
fishes = []
with open(input_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        fishes = [int(f) for f in line.strip().split(",")]


def pass_one_day(fishes):
    aged_fishes = []
    new_fishes = []
    for fish in fishes:
        if fish != 0:
            aged_fishes.append(fish-1)
        else:
            aged_fishes.append(6)
            new_fishes.append(8)
    return aged_fishes + new_fishes

def convert(fishes):
    convert_fishes = {}
    for fish in fishes:
        convert_fishes[fish] = convert_fishes.get(fish, 0) + 1
    return convert_fishes

def age_one_day(fishes):
    aged_fishes = {}
    for life, number in fishes.items():
        if life==0:
            aged_fishes[6] = aged_fishes.get(6,0) +number
            aged_fishes[8] = number
        else:
            aged_fishes[life-1] = aged_fishes.get(life-1,0) +number
    return aged_fishes    

# Part 1
days = 80
initial_fishes = fishes
print(initial_fishes)
# for day in range(days):
#     fishes = pass_one_day(fishes)

# print("After {} days, there are {} fishes".format(day, len(fishes)))

# Part 2
days2 = 256
fishes = convert(initial_fishes)
print(fishes)
for day in range(days2):
     fishes = age_one_day(fishes)

print("After {} days, there are {} fishes".format(days2, sum(fishes.values())))
