from os import read
import time
import statistics

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap


def check_line_closings(one_line):
    command = []
    for input in one_line:
        if input in opening:
            command.append(input)
        else:
            last_opening = command.pop()
            if input != closing[last_opening]:
                return [closing[last_opening], input]

def auto_complete(one_line):
    command = []
    auto_complete = []
    for input in one_line:
        if input in opening:
            command.append(input)
        else:
            command.pop()
    for remaining in reversed(command):
        auto_complete.append(closing[remaining])
    return auto_complete

def compute_auto_score(auto_completion):
    score = 0
    for auto_c in auto_completion:
        score = (score * 5) + auto_complete_point[auto_c]
    return score

@timing
def get_illegal_score(lines):
    score = 0
    incomplete_lines = []
    for line in lines:
        syntax_error = check_line_closings(line)
        if syntax_error:
            score += illegal_points[syntax_error[1]]
        else:
            incomplete_lines.append(line)
        #     print("Expected {}, but found {} instead".format(a[0], a[1]))
    return score, incomplete_lines

@timing
def get_complete_score(lines):
    scores = set()
    for line in lines:
        auto_c = auto_complete(line)
        if auto_c:
            scores.add(compute_auto_score(auto_c))
    return sorted(scores)[(int)(len(scores)/2)]

day = "10"
# source = input or example
source = "example"
source = "input"
input_file = "./day{}/{}".format(day, source)
lines = []
opening = {"[", "(", "{", "<"}
closing = {
    "[": "]",
    "(": ")",
    "{": "}",
    "<": ">"
    }
illegal_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137    
}
auto_complete_point = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4    
}

with open(input_file, 'r') as file:
    data = file.read().splitlines()
    for line in data:
        lines.append(list(line))

# Part 1

illegal_score, incomplete_lines = get_illegal_score(lines)
print("Part 1: Syntax error score is {}".format(illegal_score))

# Part 2
complete_score = get_complete_score(incomplete_lines)
print("Part 2: Auto complete score is {}".format(complete_score))
