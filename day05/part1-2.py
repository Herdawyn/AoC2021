from os import read


day = "05"
# source = input or example
source = "input"
input_file = "./day{}/{}".format(day, source)
vents = []
max_i = 0
max_j = 0
with open(input_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        points = [str(r) for r in line.strip().split(" -> ")]
        vent = []
        for p in points:
            p = p.split(",")
            max_i = max(max_i, int(p[0]))
            max_j = max(max_j, int(p[1]))
            vent.append([int(x) for x in p])
        vents.append(vent)

# Part 1
currents = [[0 for col in range(max_j + 1)] for row in range(max_i + 1)]
# print(len(currents[0]),len(currents))
print("maxi: {}, maxj: {}".format(max_i,max_j))

for ends in vents:
    [x1, y1], [x2, y2] = ends
    if (y1 == y2):
        # print(ends)
        start_x = min(x1, x2)
        end_x = max(x1, x2)
        for i in range(start_x, end_x + 1):
            # print(len(currents[0]),len(currents))
            # print(i, y1)
            currents[i][y1] += 1
    elif (x1 == x2):
        # print(ends)
        start_y = min(y1, y2)
        end_y = max(y1, y2)        
        for j in range(start_y, end_y + 1):
            # print(x1 ,j)
            currents[x1][j] += 1

sum_crossings = 0
for row in currents:
    sum_crossings += len(row) - row.count(0) - row.count(1)
print("There are {} crossings".format(sum_crossings))

# Part 2
for ends in vents:
    [x1, y1], [x2, y2] = ends
    if (abs(x1 - x2) == abs(y1 - y2)):
        # print(ends)
        if (x1 < x2):
            step_x = 1
            x2 += 1
        else:
            step_x = -1
            x2 -= 1
        if (y1 < y2):
            step_y = 1
            y2 +=1
        else:
            step_y = -1
            y2 -= 1    
        x_values = [*range(x1, x2, step_x)]
        y_values = [*range(y1, y2, step_y)]
        # print(x_values, y_values)
        for x, y in zip(x_values, y_values):
            # print(x ,y)
            currents[x][y] += 1

sum_crossings = 0
for row in currents:
    sum_crossings += len(row) - row.count(0) - row.count(1)
print("There are {} crossings".format(sum_crossings))

# for c in currents:
#     print(c)
