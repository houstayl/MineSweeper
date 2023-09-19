class Block:
    def __init__(self, x, y, hidden=True, flagged=False):
        self.x = str(x)
        self.y = str(y)
        if x < 10:
            self.x = "0" + self.x
        if y < 10:
            self.y = "0" + self.y
        self.name = "x" + self.y + "y" + self.x
        self.hidden = hidden
        self.flagged = flagged

    def reveal(self):
        self.hidden = False

    def get_block(self, x, y, type):
        return Block(x, y, type)

    def get_type(self):
        if isinstance(self, Mine):
            return "*"
        else:
            return self.number


class Mine(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "*"

class Number(Block):
    def __init__(self, x, y, number):
        super().__init__(x, y)
        self.number = number
