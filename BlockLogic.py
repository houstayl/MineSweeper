import random
from Block import Number
from Block import Block
from Block import Mine

grid = []
rows = 16
columns = 30


def surround(x, y):
    '''Returns a 3 by 3 grid that surround the the given input'''
    temp = []
    str = ""
    for i in range(-1, 2):
        for j in range(-1, 2):
            if y + i <= rows - 1 and y + i >= 0 and x + j <= columns - 1 and x + j >= 0:
                str += grid[x + i][y + j].type
        temp.append(str)
        str = ""
    return temp


def get_number(row, col):
    '''Returns the number of mines surrounding a question mark  '''
    count = 0;
    for x in range(-1, 2):
        for y in range(-1, 2):
            if row + y <= rows - 1 and row + y >= 0 and col + x <= columns - 1 and col + x >= 0:
                if grid[row + y][col + x].type == "*":
                    count += 1
    return count


def get_letters(grid):
    '''Takes the grid returned by surround and returns the letters'''
    str = ""
    for i in range(3):
        for j in range(3):
            if "ABCDEFGHIJKLMNOPQRSTUVWXYZ".__contains__(grid[i][j]):
                str += grid[i][j]
    return str


def get_all_combos(letters, number):
    str = ""
    if number == len(letters):
        return letters
    elif number == 1:
        for char in letters:
            str += char
            str += " XOR "
        str = str[: -5]
        return str
    elif number == 2:
        i = 0
        j = i + 1
        while i < len(letters):
            j = i + 1
            while j < len(letters):
                str += letters[i] + letters[j] + " XOR "
                j += 1
            i += 1
        str = str[:-5]
        return str
    elif number == 3:
        i = 0
        j = i + 1
        k = j + 1
        while i < len(letters):
            j = i + 1
            while j < len(letters):
                k = j + 1
                while k < len(letters):
                    str += letters[i] + letters[j] + letters[k] + " XOR "
                    k += 1
                j += 1
            i += 1
        str = str[:-5]
        return str


def create_grid(x_click, y_click):
    blocks = []
    bombs = 99
    for row in range(rows):
        for col in range(columns):
            if row == y_click and col == x_click:
                blocks.append(Number(row, col, "0"))
                # play around with random tolerance
            elif random.random() <= .1 and bombs > 0 and (abs(y_click - row) > 1 or abs(x_click - col) > 1):
                blocks.append(Mine(row, col))
                bombs -= 1
            else:
                blocks.append(Number(row, col, "?"))

        grid.append(blocks)
        blocks = []

    # 99 / 30*16 = .20625
    while bombs >= 1:
        rand_row = int(random.random() * float(rows))  # 0-29
        rand_col = int(random.random() * float(columns))  # 0 - 16
        if isinstance(grid[rand_row][rand_col], Number) and (abs(y_click - rand_row) > 1 or abs(x_click - rand_col) > 1):
            grid[rand_row][rand_col] = Mine(rand_row, rand_col)
            bombs -= 1
    temp = ""
    for row in range(16):
        for col in range(30):
            temp += grid[row][col].type
        temp += "\n"
    print(temp)

    for row in range(rows):
        for col in range(columns):
            if grid[row][col].type == "?":
                grid[row][col].type = str(get_number(row, col))

    return grid


g = create_grid(0, 0)
temp = ""

for row in range(rows):
    for col in range(columns):
        temp += g[row][col].type
    temp += "\n"

print(temp)
file = open("grid.txt", "w")
file.write(temp)
file.close()
# print(g)


# for i in range(len(grid)):
#   for j in range(len(grid[i])):
#      if grid[i][j] == "1" or grid[i][j] == "2" or grid[i][j] == "3" or grid[i][j] == "4" or grid[i][j] == "5" or grid[i][j] == "6":
# surround(i,j)
