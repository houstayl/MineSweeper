import pygame
from MineGrid import Grid
from Block import *





class Window:

    def __init__(self, rows, columns, cell, bombs, square_thickness, *square_color):
        pygame.init()
        self.rows = rows
        self.columns = columns
        self.cell = cell
        self.bombs = bombs
        self.square_thickness = square_thickness
        self.square_color = square_color
        self.win = pygame.display.set_mode((cell * columns, cell * rows))
        pygame.display.set_caption("Jeffsweeper")
        self.numbers = [pygame.image.load("zero.png"), pygame.image.load("one.png"), pygame.image.load("two.png"), pygame.image.load("three.png"), pygame.image.load("four.png"), pygame.image.load("five.png"), pygame.image.load("six.png"), pygame.image.load("seven.png"), pygame.image.load("eight.png")]
        self.flag = pygame.image.load("flag.png")
        self.unknown = pygame.image.load("hidden.png")
        self.mine = pygame.image.load("mine.png")

        x = int(input("Select a x value between 0 and " + str(self.columns - 1) + ": "))
        y = int(input("Select a y value between 0 and " + str(self.rows - 1) + ": "))
        self.g = Grid(self.rows, self.columns, self.bombs, x, y)
        self.g.recursive_reveal(y, x)
        print(self.g.print_grid())

    def run(self):


        for i in range(self.rows):
            for j in range(self.columns):
                block = self.g.grid[i][j]
                if block.hidden:
                    self.win.blit(self.unknown, (j * self.cell, i * self.cell))
                    pygame.draw.rect(self.win, self.square_color, (j * self.cell, i * self.cell, self.cell, self.cell), self.square_thickness)

                else:
                    if isinstance(block, Number):
                        self.win.blit(self.numbers[block.get_type()], (j * self.cell, i * self.cell))
                        pygame.draw.rect(self.win, self.square_color, (j * self.cell, i * self.cell, self.cell, self.cell), self.square_thickness)
                    else:
                        self.win.blit(self.mine, (j * self.cell, i * self.cell))
                        pygame.draw.rect(self.win, self.square_color, (j * self.cell, i * self.cell, self.cell, self.cell), self.square_thickness)


        run = True
        while run:
            pygame.time.delay(100)
            if self.bombs < 1:
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.g.grid[pos[1] // self.cell][pos[0] // self.cell].reveal()
                    temp = self.g.grid[pos[1] // self.cell][pos[0] // self.cell]
                    if pygame.mouse.get_pressed()[0]:
                        if temp.get_type() == str("*"):
                            self. win.blit(self.mine, ((pos[0] // self.cell) * self.cell, (pos[1] // self.cell) * self.cell))
                            pygame.draw.rect(self.win, self.square_color, ((pos[0] // self.cell) * self.cell, (pos[1] // self.cell) * self.cell, self.cell, self.cell), self.square_thickness)
                        else:
                            if temp.get_type() == 0:
                                self.g.grid[pos[1] // self.cell][pos[0] // self.cell].hidden == True
                                self.recursive_reveal(pos[1] // self.cell, pos[0] // self.cell)
                            self.win.blit(self.numbers[temp.get_type()], ((pos[0] // self.cell) * self.cell, (pos[1] // self.cell) * self.cell))
                            pygame.draw.rect(self.win, self.square_color, ((pos[0] // self.cell) * self.cell, (pos[1] // self.cell) * self.cell, self.cell, self.cell), self.square_thickness)

                    elif pygame.mouse.get_pressed()[2]:
                        self.win.blit(self.flag, ((pos[0] // self.cell) * self.cell, (pos[1] // self.cell) * self.cell))
                        pygame.draw.rect(self.win, self.square_color, ((pos[0] // self.cell) * self.cell, (pos[1] // self.cell) * self.cell, self.cell, self.cell), self.square_thickness)
                        self.bombs -= 1

                    elif pygame.mouse.get_pressed()[1]:
                        g.grid[pos[1] // self.cell][pos[0] // self.cell].hidden = True
                        self.win.blit(self.unknown, ((pos[0] // self.cell) * self.cell, (pos[1] // self.cell) * self.cell))
                        pygame.draw.rect(self.win, self.square_color, ((pos[0] // self.cell) * self.cell, (pos[1] // self.cell) * self.cell, self.cell, self.cell), self.square_thickness)

            pygame.display.update()

        pygame.quit()

    def recursive_reveal(self, row, col):
        print("recursive reveal")
        print(str(self.g.grid[row][col].get_type()) == "0")
        print(self.g.grid[row][col].hidden == True)
        if str(self.g.grid[row][col].get_type()) == "0" and self.g.grid[row][col].hidden == True:
            print("TRUE")
            self.g.grid[row][col].reveal()
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if row + i <= self.rows - 1 and row + i >= 0 and col + j <= self.columns - 1 and col + j >= 0:
                        self.recursive_reveal(row + i, col + j)
                        self.g.grid[row + i][col + j].reveal()
                        self.win.blit(self.numbers[self.g.grid[row][col].get_type()], (j * self.cell, i * self.cell))
                        pygame.draw.rect(self.win, self.square_color, (j * self.cell, i * self.cell, self.cell, self.cell), self.square_thickness)



