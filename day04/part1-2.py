from os import read

day = "04"
# source = input or example
source = "input"
input_file = "./day{}/{}".format(day, source)
draws = []
boards = []
board_size = 5

def check_board(board, number):
    board_size = len(board[0])
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == number:
                return i, j

def check_bingo(board):
    board_size = len(board[0])
    col_sum =  [ sum(x) for x in zip(*board) ]
    for i in range(board_size):
        if sum(board[i]) == board_size:
            return [0, i]
        elif col_sum[i] == board_size:
            return [1, i]

def get_unmarked_sum(board, checked):
    sum = 0
    for i in range(len(checked[0])):
        for j in range(len(checked)):
            if checked[i][j] == 0:
                # print("add ", board[i][j])
                sum += int(board[i][j])
    return(sum)

with open(input_file, 'r') as file:
    # draws line
    line = file.readline()
    draws = line.strip().split(",")
    # first blank line
    line = file.readline()
    # first line to read
    line = file.readline().replace("  ", " ")
    board = []
    while line:
        newline = line.strip()
        if line.strip() == "":
            boards.append(board)
            board = []
        else:
            board.append(newline.split(" "))
        line = file.readline().replace("  ", " ")
    boards.append(board)        

# Part 1
print("---- Part 1 ----")
boards_check = []
for b in boards:
    boards_check.append([ [0] * len(boards[0]) for _ in range(len(boards[0]))])
print(boards_check)

for draw in draws:
    print("Draw: ", draw)
    for i, board in enumerate(boards):
        in_board = check_board(board, draw)
        if in_board:
            boards_check[i][in_board[0]][in_board[1]] = 1
            is_bingo = check_bingo(boards_check[i])
            if is_bingo:
                print("Bingo ! ", i+1, board, boards_check[i], is_bingo)
                unmarked = get_unmarked_sum(board, boards_check[i])
                print("Unmarked values {}, last draw {}, multiply: {}".format(unmarked, draw, unmarked * int(draw)))
                break

# Part 2
print("---- Part 2 -----")
boards_check = []
for b in boards:
    boards_check.append([ [0] * len(boards[0]) for _ in range(len(boards[0]))])

win_boards = []
last_draw = 0
for draw in draws:
    print("Draw: ", draw)
    for i, board in enumerate(boards):
        if i not in win_boards:
            in_board = check_board(board, draw)
            if in_board:
                boards_check[i][in_board[0]][in_board[1]] = 1
                is_bingo = check_bingo(boards_check[i])
                if is_bingo:
                    win_boards.append(i)
                    print("Bingo ! ", i+1, board, boards_check[i], is_bingo)
                    print("Board {} won".format(i+1))
                    if len(win_boards) == len(boards):
                        print("All boards have won, last board is ", i+1)
                        last_draw = draw
                        break

last_to_win = win_boards[-1]
unmarked = get_unmarked_sum(boards[last_to_win], boards_check[last_to_win])
print("Unmarked values {}, last draw {}, multiply: {}".format(unmarked, last_draw, unmarked * int(last_draw)))
