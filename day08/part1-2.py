from os import read
import time

day = "08"
# source = input or example
source = "example"
source = "input"
input_file = "./day{}/{}".format(day, source)
digits = []
with open(input_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        ten_digits, code = [str(s) for s in line.strip().split(" | ")]
        ten_digits = [str(s) for s in ten_digits.split(" ")]
        code = [str(s) for s in code.split(" ")]
        digits.append([ten_digits, code])

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

@timing
def count_easy(digits):
    count = 0
    for line in digits:
        ten_digits, code = line
        for digit in code:
            if len(digit) in length_for_easy_digit.keys():
                count += 1
    return count

def sub_segments(segment, exclude):
    return sorted(list(set(segment) - set(exclude)))

def find_zero(digits):
    # 0 is the only digit that has not d seg in uneasy digits
    subs = {}
    for digit in digits:
        subs["".join(digit)] = True
        for to_be_subbed in digits:
            if not (digit == to_be_subbed):
                if len(sub_segments(to_be_subbed, digit)) != 1:
                    subs["".join(digit)] = False
    for sub, is_zero in subs.items():
        if is_zero:
            return sorted(list(sub))


def find_six_nine(digits, zero, four, a):
    # 6 is 6 length remove 0 then if - 4 -a - 2 segs left
    six_nine = ["", ""]
    for digit in digits:
        if digit == zero:
            continue
        if len(digit) == 6:
            step_1 = sub_segments(digit, four)
            step_2 = sub_segments(step_1, a)
            if len(step_2) == 2:
                six_nine[0] = digit
            elif len(step_2) == 1:
                six_nine[1] = digit
    return six_nine


def find_digits(ten_digits):
    wire = {}
    uneasy_digits = []
    for segment in ten_digits:
        if len(segment) in length_for_easy_digit.keys():
            wire[length_for_easy_digit[len(segment)]] = sorted(segment)
        else:
            uneasy_digits.append(sorted(segment))

    wire[0] = find_zero(uneasy_digits)

    seg_a = sub_segments(wire[7], wire[1])
    seg_d = sub_segments(wire[8], wire[0])
    seg_b = sub_segments(sub_segments(wire[4], wire[1]), seg_d)
    wire[6], wire[9] = find_six_nine(uneasy_digits, wire[0], wire[4], seg_a)

    seg_c = sub_segments(wire[0], wire[6])
    seg_f = sub_segments(wire[1], seg_c)
    seg_e = sub_segments(wire[0], wire[9])

    wire[5] = sub_segments(wire[6], seg_e)
    wire[3] = sub_segments(sub_segments(wire[8], seg_b), seg_e)
    wire[2] = sub_segments(sub_segments(wire[8], seg_b), seg_f)

    return wire


def digit_decode(codes, signals):
    sum = ""
    for signal in signals:
        for key, value in codes.items():
            if value == sorted(list(signal)):
                # print(key, value)
                sum += str(key)
    return int(sum)

@timing
def sum_codes(lines):
    sum_code = 0
    for line in lines:
        codex = find_digits(line[0])
        sum_code += digit_decode(codex, line[1])
    return sum_code


length_for_easy_digit = {
    2: 1,
    3: 7,
    4: 4,
    7: 8
}

# Part 1
easy_digit_occurence = count_easy(digits)
print("Counted {} easy digits (1, 7, 4, 8)".format(easy_digit_occurence))

# Part 2
sum_code = sum_codes(digits)
print("Summed codes value is {}".format(sum_code))
