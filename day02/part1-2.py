def process(commands):
    horizontal = 0
    vertical = 0
    aim = 0
    depth = 0
    for command in commands:
        if command[0] == "forward":
            horizontal += command[1]
            depth += command[1] * aim
        elif command[0] == "up":
            vertical -= command[1]
            aim -= command[1]
        elif command[0] == "down":
            vertical += command[1]
            aim += command[1]
        else:
            print("Erreur commande non comprise ",command)
    return horizontal, vertical, depth

input_file = "input"
commands = []
with open(input_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        move = str(line.strip()).split(" ")
        commands.append([move[0], int(move[1])])

# Part 1
h, v, d = process(commands)
print("New position is {} ".format(h*v))

# Part 2
print("New position with aim is {} ".format(h*d))