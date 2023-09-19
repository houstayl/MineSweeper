from MineGrid import Grid
from Block import *



class PlayGame:
    rows = 16
    columns = 30
    bombs = 99
    x = int(input("Select a x value between 0 and " + str(columns - 1) + ": "))
    y = int(input("Select a y value between 0 and " + str(rows - 1) + ": "))
    g = Grid(rows, columns, bombs, x, y)
    g.recursive_reveal(y, x)
    print(g.print_grid())
    print(g.surround(y, x))
    #algebra = boolean.BooleanAlgebra()

    while bombs >= 1:
        inp = input("Would you like to select a mine: '*' or a number: '#': ")
        x = int(input("Select a x value between 0 and " + str(columns - 1) + ": "))
        y = int(input("Select a y value between 0 and " + str(rows - 1) + ": "))
        if inp == "*":
            if isinstance(g.grid[y][x], Mine):
                g.grid[y][x].reveal()
                bombs -= 1
            else:
                print("Game over")
                bombs = -1
        else:
            if isinstance(g.grid[y][x], Number):
                if(g.grid[y][x].get_type() == 0):
                    g.recursive_reveal(y, x)
                else:
                    g.grid[y][x].reveal()
            else:
                print("Game over")
                bombs = -1
        print(g.print_grid())

