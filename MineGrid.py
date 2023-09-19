import random
#import pygame
from BooleanGrid import BooleanSimplifier
from Block import *
from operator import itemgetter

class Grid:

    def __init__(self, rows, columns, bombs, x_click, y_click):
        self.rows = rows
        self.columns = columns
        self.bombs = bombs
        self.grid = self.create_grid(x_click, y_click)
        self.bombs = bombs # bombs gets changed to zero in the create_grid method

    def create_grid(self, x_click, y_click):
        blocks = []
        grid = []
        for row in range(self.rows):
            for col in range(self.columns):
                if row == y_click and col == x_click:
                    blocks.append(Number(row, col, 0))
                # play around with random tolerance
                elif random.random() <= .1 and self.bombs > 0 and (abs(y_click - row) > 1 or abs(x_click - col) > 1):
                    blocks.append(Mine(row, col))
                    self.bombs -= 1
                else:
                    blocks.append(Number(row, col, "?"))

            grid.append(blocks)
            blocks = []

        # 99 / 30*16 = .20625
        while self.bombs >= 1:
            rand_row = int(random.random() * float(self.rows))  # 0-29
            rand_col = int(random.random() * float(self.columns))  # 0 - 16
            if isinstance(grid[rand_row][rand_col], Number) and (
                    abs(y_click - rand_row) > 1 or abs(x_click - rand_col) > 1):
                grid[rand_row][rand_col] = Mine(rand_row, rand_col)
                self.bombs -= 1

        # temp = ""
        # for row in range(16):
        #    for col in range(30):
        #        temp += str(grid[row][col].get_type())
        #    temp += "\n"
        # print(temp)

        for row in range(self.rows):
            for col in range(self.columns):
                if isinstance(grid[row][col], Number):
                    grid[row][col].number = self.get_number(row, col, grid)

        temp = ""
        for row in range(self.rows):
            for col in range(self.columns):
                temp += str(grid[row][col].get_type())
            temp += "\n"
       # print(temp)

        #file = open("grid.txt", "w")
        #file.write(self.print_grid())
        #file.close()

        return grid

    def print_grid(self):
        temp = ""
        for y in range(self.rows):
            for x in range(self.columns):
                if not self.grid[y][x].hidden:
                    temp += str(self.grid[y][x].get_type())
                else:
                    temp += "?"
            temp += "\n"
        file = open("grid.txt", "w")
        file.write(temp)
        file.close()
        return temp

    def recursive_reveal(self, row, col):
        if isinstance(self.grid[row][col], Number) and self.grid[row][col].get_type() == 0 and self.grid[row][col].hidden == True:
            self.grid[row][col].reveal()
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if row + i <= self.rows - 1 and row + i >= 0 and col + j <= self.columns - 1 and col + j >= 0:
                        self.recursive_reveal(row + i, col + j)
                        self.grid[row + i][col + j].reveal()

    def is_game_won(self):
        for row in self.grid:
            for block in row:
                if isinstance(block, Mine) and block.hidden != block.flagged:
                    return False
        return True

    def get_all_combos_unsimplified(self, letters, number):
        #TODO Havent checked to see if 5 6 or 7 work properly
        combos = "("
        ampersand = " & "
        or_operator = " | "
        length = len(letters)
        if number == 0:
            return "solved" #letters""
        elif number == length:
            self.flag_surrounding(letters)
            for index, value in enumerate(letters):
                combos += "~" + value
                if index < length - 1:
                    combos += ampersand
        elif number == 1:
            for i in range(length):
                combos += "("
                for index, value in enumerate(letters):
                    if index == i:
                        combos += "~" + value
                    else:
                        combos += value
                    if index != length - 1:
                        combos += ampersand
                combos += ")"
                if i != length - 1:
                    combos += or_operator
        elif number == 2:
            for i in range(length):
                for j in range(i + 1, length):
                    combos += "("
                    for index, value in enumerate(letters):
                        if index == i or index == j:
                            combos += "~" + value
                        else:
                            combos += value
                        if index != length - 1:
                            combos += ampersand
                    combos += ")"
                    if j < length - 1:#subtract the number of for in range loops
                        combos += or_operator
                if i < length - 2:  #subtract the number of for in range loops
                    combos += or_operator
        elif number == 3:
            for i in range(length):
                for j in range(i + 1, length):
                    for k in range(j + 1, length):
                        combos += "("
                        for index, value in enumerate(letters):
                            if index == i or index == j or index == k:
                                combos += "~" + value
                            else:
                                combos += value
                            if index != length - 1:
                                combos += ampersand
                        combos += ")"
                        if k < length - 1:  # subtract the number of for in range loops
                            combos += or_operator
                    if j < length - 2:  # subtract the number of for in range loops
                        combos += or_operator
                if i < length - 3:  # subtract the number of for in range loops
                    combos += or_operator
        elif number == 4:
            for i in range(length):
                for j in range(i + 1, length):
                    for k in range(j + 1, length):
                        for l in range(k + 1, length):
                            combos += "("
                            for index, value in enumerate(letters):
                                if index == i or index == j or index == k or index == l:
                                    combos += "~" + value
                                else:
                                    combos += value
                                if index != length - 1:
                                    combos += ampersand
                            combos += ")"
                            if l < length - 1:  # subtract the number of for in range loops
                                combos += or_operator
                        if k < length - 2:  # subtract the number of for in range loops
                            combos += or_operator
                    if j < length - 3:  # subtract the number of for in range loops
                        combos += or_operator
                if i < length - 4:  # subtract the number of for in range loops
                    combos += or_operator
        elif number == 5:
            for i in range(length):
                for j in range(i + 1, length):
                    for k in range(j + 1, length):
                        for l in range(k + 1, length):
                            for m in range(l + 1, length):
                                combos += "("
                                for index, value in enumerate(letters):
                                    if index == i or index == j or index == k or index == l or index == m:
                                        combos += "~" + value
                                    else:
                                        combos += value
                                    if index != length - 1:
                                        combos += ampersand
                                combos += ")"
                                if m < length - 1:  # subtract the number of for in range loops
                                    combos += or_operator
                            if l < length - 2:  # subtract the number of for in range loops
                                combos += or_operator
                        if k < length - 3:  # subtract the number of for in range loops
                            combos += or_operator
                    if j < length - 4:  # subtract the number of for in range loops
                        combos += or_operator
                if i < length - 5:  # subtract the number of for in range loops
                    combos += or_operator
        elif number == 6:
            for i in range(length):
                for j in range(i + 1, length):
                    for k in range(j + 1, length):
                        for l in range(k + 1, length):
                            for m in range(l + 1, length):
                                for n in range(m + 1, length):
                                    combos += "("
                                    for index, value in enumerate(letters):
                                        if index == i or index == j or index == k or index == l or index == m or index == n:
                                            combos += "~" + value
                                        else:
                                            combos += value
                                        if index != length - 1:
                                            combos += ampersand
                                    combos += ")"
                                    if n < length - 1:  # subtract the number of for in range loops
                                        combos += or_operator
                                if m < length - 2:  # subtract the number of for in range loops
                                    combos += or_operator
                            if l < length - 3:  # subtract the number of for in range loops
                                combos += or_operator
                        if k < length - 4:  # subtract the number of for in range loops
                            combos += or_operator
                    if j < length - 5:  # subtract the number of for in range loops
                        combos += or_operator
                if i < length - 6:  # subtract the number of for in range loops
                    combos += or_operator
        elif number == 7:
            for i in range(length):
                for j in range(i + 1, length):
                    for k in range(j + 1, length):
                        for l in range(k + 1, length):
                            for m in range(l + 1, length):
                                for n in range(m + 1, length):
                                    for o in range(n + 1, length):
                                        combos += "("
                                        for index, value in enumerate(letters):
                                            if index == i or index == j or index == k or index == l or index == m or index == n or index == 0:
                                                combos += "~" + value
                                            else:
                                                combos += value
                                            if index != length - 1:
                                                combos += ampersand
                                        combos += ")"
                                        if o < length - 1:  # subtract the number of for in range loops
                                            combos += or_operator
                                    if n < length - 2:  # subtract the number of for in range loops
                                        combos += or_operator
                                if m < length - 3:  # subtract the number of for in range loops
                                    combos += or_operator
                            if l < length - 4:  # subtract the number of for in range loops
                                combos += or_operator
                        if k < length - 5:  # subtract the number of for in range loops
                            combos += or_operator
                    if j < length - 6:  # subtract the number of for in range loops
                        combos += or_operator
                if i < length - 7:  # subtract the number of for in range loops
                    combos += or_operator
        elif number == 8:
            for char in letters:
                combos += char + ampersand
            combos = combos + ")"
        combos += ")"
        return combos

    def get_number(self, row, col, grid):
        '''Returns the number of mines surrounding a question mark  '''
        count = 0;
        for x in range(-1, 2):
            for y in range(-1, 2):
                if row + y <= self.rows - 1 and row + y >= 0 and col + x <= self.columns - 1 and col + x >= 0:
                    if isinstance(grid[row + y][col + x], Mine):
                        count += 1
        return count

    def surround(self, row, col):
        '''Returns a list of coordinates that surround the the given input and the number of mines surrounding the given input'''
        temp = []
        num = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if row + i <= self.rows - 1 and row + i >= 0 and col + j <= self.columns - 1 and col + j >= 0:
                    if self.grid[row + i][col + j].hidden == True and self.grid[row + i][col + j].flagged == False:
                        temp.append(self.grid[row + i][col + j].name)
                    if self.grid[row + i][col + j].flagged == True:  # could cause a problem if a number is flagged instead of a mine
                        num += 1
        if self.grid[row][col] in temp:
            temp.remove(self.grid[row][col].name)
        return (temp, num)

    def get_move(self, row, col):
        moved = False
        if self.is_get_movable(row, col):
            surround, n_mines = self.surround(row, col)[0], self.surround(row, col)[1]
            #print("surround: " + str(surround) + " mines placed: " + str(n_mines))
            t = self.get_all_combos_unsimplified(surround, self.grid[row][col].get_type() - n_mines)
            print(t)
            if t == "solved":
                moved = True
                self.solved(row, col)
        elif self.is_unknown_next_to_number(row, col):
            self.get_move_for_unknown(row, col)
        else:
            print("no numbers around")
        return moved

    def get_move_for_unknown(self, row, col):
        moved = False
        expressions = []
        all_surround = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if row + i <= self.rows - 1 and row + i >= 0 and col + j <= self.columns - 1 and col + j >= 0 and isinstance(self.grid[row + i][col + j], Number) == True and self.grid[row + i][col + j].hidden == False:
                    surround, n_mines = self.surround(row + i, col + j)
                    for item in surround:
                        all_surround.add(item)
                    #print("type - mines " + str(self.grid[row + i][col + j].get_type() - n_mines))
                    t = self.get_all_combos_unsimplified(surround, self.grid[row + i][col + j].get_type() - n_mines)
                    if t == "solved":
                        self.solved(row + i, col + j)
                    else:
                       expressions.append(t)
        mines, numbers = BooleanSimplifier.simplify(expressions, all_surround)
        self.solve_by_name(mines, numbers)
        if len(mines) > 0 or len(numbers) > 0:
            moved = True
        return moved

    def solve_by_name(self, mines, numbers):
        print("solve: Mines " + str(mines) + " Numbers: " + str(numbers))
        for m in mines:
            if self.grid[int(m[4:])][int(m[1:3])].flagged == False:
                self.grid[int(m[4:])][int(m[1:3])].flagged = True
                self.bombs -= 1
                print("solved bombs decreased: " + str(self.bombs))
        for n in numbers:
            if self.grid[int(n[4:])][int(n[1:3])].get_type() == 0:
                self.recursive_reveal(int(n[4:]), int(n[1:3]))
            self.grid[int(n[4:])][int(n[1:3])].reveal()

    def solved(self, row, col):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if row + i <= self.rows - 1 and row + i >= 0 and col + j <= self.columns - 1 and col + j >= 0:
                    self.recursive_reveal(row + i, col + j)
                    if self.grid[row + i][col + j].flagged == False:
                        self.grid[row + i][col + j].reveal()

    def flag_surrounding(self, surrounding):
        """#TODO might mess up with number of bombs and knowing when the game is lost and stuff"""
        for point in surrounding:
            col = int(point[1:3])
            row = int(point[4:6])
            if self.grid[row][col].flagged == False:
                self.grid[row][col].flagged = True
                self.bombs -= 1
        print(self.bombs)

    def is_get_movable(self, row, col):
        if self.grid[row][col].hidden is False and isinstance(self.grid[row][col], Number):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if row + i <= self.rows - 1 and row + i >= 0 and col + j <= self.columns - 1 and col + j >= 0 and self.grid[row + i][col + j].hidden == True:
                        return True
        else:
            return False

    def is_unknown_next_to_number(self, row, col):
        if self.grid[row][col].hidden is True:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if row + i <= self.rows - 1 and row + i >= 0 and col + j <= self.columns - 1 and col + j >= 0 and isinstance(self.grid[row + i][col + j], Number) == True and self.grid[row + i][col + j].hidden == False:
                        return True
        else:
            return False

    def reveal_all(self):
        for row in self.grid:
            for col in row:
                if not (isinstance(col, Mine) and col.flagged == True):
                    col.flagged = False    #could add in a wrong flag(flag placed on a number) indicator instead of just showing the number
                    col.reveal()
        self.print_grid()

    def recursive_solve(self, hidden=99, flagged=0):
        #TODO stop from checking from numbers that have already been solved   could create a set containing all solved numbers   see if change made by keeping track of flagged and hidden
        if self.is_game_won() == True:
            return
        nums = self.find_border_numbers()
        if len(nums) == 0:
            return
        for block in nums:
            if self.get_move(int(block.x), int(block.y)) == True:
                self.print_grid()
        hid, flag = self.get_num_hidden_and_flagged()
        if hid == hidden and flag == flagged:  # no move was made: might cause trouble off the start
            self.recursive_unknown_solve(hid, flag)
        self.recursive_solve(hid, flag)


    def recursive_unknown_solve(self, hidden, flagged):
        last = self.find_border_unknowns()
        if len(last) > 0:  #might not be needed
            for block in last:
                if self.get_move_for_unknown(int(last[0].x), int(last[0].y)) == True:
                   self.print_grid()
        hid, flag = self.get_num_hidden_and_flagged()
        if hid == hidden and flag == flagged:
            return False
        #self.print_grid()
        self.recursive_unknown_solve(hid, flag)



    def find_border_numbers(self):
        nums = []
        for row in self.grid:
            for col in row:
                if self.is_get_movable(int(col.x), int(col.y)):  #finds numbers that border
                    nums.append(col)
        return nums
        '''
        moved = 0
        for row in self.grid:
            for col in row:
                if self.get_move(int(col.x), int(col.y)) == True:
                    moved +=1
        return moved > 0
        '''

    def find_border_unknowns(self):
        unknowns = []
        for row in self.grid:
            for col in row:
                if self.is_unknown_next_to_number(int(col.x), int(col.y)):
                    unknowns.append(col)
        return self.sort_border_unknows(unknowns)

    def sort_border_unknows(self, unknowns):
        unknowns_and_number = []
        for unknown in unknowns:
            unknowns_and_number.append([unknown, self.get_number_of_nums_surrounding(unknown)])
        unknowns_and_number = sorted(unknowns_and_number, key=itemgetter(1))
        for index in range(len(unknowns_and_number)):
            unknowns_and_number[index] = unknowns_and_number[index][0]
        return unknowns_and_number

    def get_number_of_nums_surrounding(self, block):
        #TODO could sort better if instead of sorting by number of nums surrounding the unkown, sorting by the number of unkowns surrounding the nums that surround the unkown
        count = 0;
        for x in range(-1, 2):
            for y in range(-1, 2):
                if int(block.x) + y <= self.rows - 1 and int(block.x) + y >= 0 and int(block.y) + x <= self.columns - 1 and int(block.y) + x >= 0:
                    if isinstance(self.grid[int(block.x) + y][int(block.y) + x], Number) and self.grid[int(block.x) + y][int(block.y) + x].hidden == False:
                        count += 1
        return count

    def remove_solved_from_unknown(self, unknowns):
        reduced = unknowns
        for block in unknowns:
            if block.hidden == False or block.flagged == True:
                reduced.remove(block)
        return reduced

    def get_num_hidden_and_flagged(self):
        hidden = 0
        flagged = 0
        for row in self.grid:
            for col in row:
                if col.hidden == True:
                    hidden += 1
                if col.flagged == True:
                    flagged += 1
        return (hidden, flagged)



