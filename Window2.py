import pygame
from MineGrid import Grid
from Block import *
#import multiprocessing


class TextWindow:

    def __init__(self, rows, columns, cell, bombs, square_thickness, *square_color):
        pygame.init()
        self.rows = rows
        self.columns = columns
        self.cell = cell
        self.square_thickness = square_thickness
        self.square_color = square_color
        self.win = pygame.display.set_mode((cell * columns, cell * rows))
        pygame.display.set_caption("Minesweeper")
        self.numbers = [pygame.image.load("zero.png"), pygame.image.load("one.png"), pygame.image.load("two.png"), pygame.image.load("three.png"), pygame.image.load("four.png"), pygame.image.load("five.png"), pygame.image.load("six.png"), pygame.image.load("seven.png"), pygame.image.load("eight.png")]
        self.flag = pygame.image.load("flag.png")
        self.unknown = pygame.image.load("hidden2.png")
        self.mine = pygame.image.load("mine.png")

        for i in range(self.rows):
            for j in range(self.columns):
                self.win.blit(self.unknown, (j * self.cell, i * self.cell))
                pygame.draw.rect(self.win, self.square_color, (j * self.cell, i * self.cell, self.cell, self.cell), self.square_thickness)
        pygame.display.update()


        r = True
        while r:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = pos[1] // cell
                    y = pos[0] // cell
                    self.g = Grid(rows, columns, bombs, y, x)
                    print(self.g.bombs)
                    self.g.recursive_reveal(x, y)
                    self.g.print_grid()
                    self.draw_from_text_file("grid.txt")
                   # print(self.g.print_grid())
                    r = False



    def run(self):
        run = True
        while run:
            self.draw_from_text_file("grid.txt")
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    #self.g.grid[pos[1] // self.cell][pos[0] // self.cell].reveal()
                    #self.g.grid[pos[1] // self.cell][pos[0] // self.cell]
                    if pygame.mouse.get_pressed()[0]:
                        if self.g.grid[pos[1] // self.cell][pos[0] // self.cell].flagged == False:
                            self.g.grid[pos[1] // self.cell][pos[0] // self.cell].reveal()
                        if self.g.grid[pos[1] // self.cell][pos[0] // self.cell].get_type() == str("*") and self.g.grid[pos[1] // self.cell][pos[0] // self.cell].flagged == False:
                            #self.g.grid[pos[1] // self.cell][pos[0] // self.cell].flagged = True
                            self.g.reveal_all()
                            print("You lose")
                            #pygame.time.delay(1000)
                        else:
                            if self.g.grid[pos[1] // self.cell][pos[0] // self.cell].get_type() == 0:
                                self.g.grid[pos[1] // self.cell][pos[0] // self.cell].hidden = True
                                self.g.recursive_reveal(pos[1] // self.cell, pos[0] // self.cell)

                    elif pygame.mouse.get_pressed()[2]:

                        if self.g.bombs >= 1:
                            if self.g.grid[pos[1] // self.cell][pos[0] // self.cell].hidden == True:
                                self.g.grid[pos[1] // self.cell][pos[0] // self.cell].flagged = not self.g.grid[pos[1] // self.cell][pos[0] // self.cell].flagged
                                if self.g.grid[pos[1] // self.cell][pos[0] // self.cell].flagged == True:
                                    self.g.bombs -= 1
                                else:
                                    self.g.bombs += 1
                                if self.g.bombs == 0:
                                    if self.g.is_game_won() == True:
                                        print("Game won")
                                        self.g.reveal_all()
                                    else:
                                        self.g.grid[pos[1] // self.cell][pos[0] // self.cell].flagged = False
                                        self.g.bombs += 1


                        print("Bombs: " + str(self.g.bombs))
                    elif pygame.mouse.get_pressed()[1]:
                        #pass
                        #self.g.get_move(pos[1] // self.cell, pos[0] // self.cell)
                        self.recursive_solve()




                   # elif pygame.mouse.get_pressed()[1]:
                        #if self.g.grid[pos[1] // self.cell][pos[0] // self.cell].hidden ==:
                           # self.g.grid[pos[1] // self.cell][pos[0] // self.cell].hidden = True

                    self.g.print_grid()
                    self.draw_from_text_file("grid.txt")

            pygame.display.update()
        pygame.quit()

    def draw_from_text_file(self, file_name):
        file = open(file_name, "r")
        text = []
        for k in range(self.rows):
            text.append(file.readline())  #2D list
        for i in range(self.rows):
            for j in range(self.columns):
                letter = text[i][j]
                if self.g.grid[i][j].flagged == True:
                    self.win.blit(self.flag, (j * self.cell, i * self.cell))
                elif letter == "*":
                    self.win.blit(self.mine, (j * self.cell, i * self.cell))
                elif letter == "?":
                    self.win.blit(self.unknown, (j * self.cell, i * self.cell))
                elif letter == "f":
                    self.win.blit(self.flag, (j * self.cell, i * self.cell))
                else:
                    self.win.blit(self.numbers[int(letter)], (j * self.cell, i * self.cell))
                pygame.draw.rect(self.win, self.square_color, (j * self.cell, i * self.cell, self.cell, self.cell), self.square_thickness)
        pygame.display.update()
        file.close()

    def recursive_solve(self, hidden=99, flagged=0):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        #TODO stop from checking from numbers that have already been solved and numbers that have already been checked but nothing changed within its perimeter   could create a set containing all solved numbers   see if change made by keeping track of flagged and hidden
        if self.g.is_game_won() == True:
            return
        nums = self.g.find_border_numbers()
        if len(nums) == 0:
            return
        for block in nums:
            if self.g.get_move(int(block.x), int(block.y)) == True:
                self.g.print_grid()
        hid, flag = self.g.get_num_hidden_and_flagged()
        if hid == hidden and flag == flagged:  # no move was made: might cause trouble off the start
            self.recursive_unknown_solve(hid, flag)
        self.draw_from_text_file("grid.txt")
        pygame.display.update()
        self.recursive_solve(hid, flag)


    def recursive_unknown_solve(self, hidden, flagged):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        if self.g.is_game_won() == True:
            return
        last = self.g.find_border_unknowns() #sort list in order of least number of numbers surrounding unknown
        for block in last:
            if self.g.get_move_for_unknown(int(block.x), int(block.y)) == True:
                self.g.print_grid()
                self.recursive_solve(self.g.get_num_hidden_and_flagged())
        hid, flag = self.g.get_num_hidden_and_flagged()
        if hid == hidden and flag == flagged:
            self.recursive_solve(hid, flag)
        #self.print_grid()
        self.draw_from_text_file("grid.txt")
        pygame.display.update()
        self.g.recursive_unknown_solve(hid, flag)