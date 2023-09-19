#from sympy import *
from sympy.abc import *
from sympy import S
from sympy.logic import simplify_logic

class BooleanSimplifier:

    @staticmethod
    def expression_symbols_converter(expression, variables):  #pass in surround() as a set
        symbols_list = [b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z] #for some reason a doesn't work
        diction = {}
        for index, var in enumerate(variables):
            diction.update({(var, str(symbols_list[index]))})
        for index in range(len(expression)):
            for key in diction:
                expression[index] = expression[index].replace(key, diction[key])
        ret = ""
        for index in range(len(expression)):
            ret += expression[index]
            if index < len(expression) - 1:
                ret += "&"
        print("converted to symbols: " + ret)
        return (ret, diction)



    @staticmethod
    def simplify(expression, variables):
        if expression == []:  #if expression is []
            print("Expression is empty")
            return ([], [])
        print(expression)
        exp, diction = BooleanSimplifier.expression_symbols_converter(expression, variables)
        sim = simplify_logic(exp)
        print("simplified: " + str(sim))
        return BooleanSimplifier.letter_to_coordinate(str(sim), diction)

    @staticmethod
    def letter_to_coordinate(expression, diction):
        mines = []
        numbers = []
        knowns = ""
        paren_index = expression.find("(")
        if paren_index == 0:
            return (mines, numbers)
        elif paren_index == - 1:
            knowns = expression.split(" & ")
        else:
            knowns = expression[:expression.find("(") - 3].split(" & ")
        print("knowns " + str(knowns))

        for val in knowns:
            if val[0] == "~":
                mines.append(val[1])
            else:
                numbers.append(val)

        print("Mines " + str(mines) + " Numbers: " + str(numbers))
        for key, value in diction.items():
            print("Key: " + key + ( " Value: " + value))
            if value in mines:
                mines.remove(value)
                mines.append(key)
            if value in numbers:
                numbers.remove(value)
                numbers.append(key)
        print("Mines " + str(mines) + " Numbers: " + str(numbers))
        return (mines, numbers)


