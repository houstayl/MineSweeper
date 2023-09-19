from sympy import *

#class Simplify:

def xor(term, term2):
    expression = "((~(" + term + ") & (" + term2 + ")) | " + "((" + term + ") & ~(" + term2 + ")))"
    return expression


x1y1, x2y2 = symbols("x1y1, x2y2")
b = x1y1 | (x2y2 & x1y1)
print(b)
print(simplify_logic(b))
A, B, C = symbols("A, B, C")
c = ()

term = "A & B"
term2 = "B & C"
e = xor(xor(term, term2), "A and C") + " & ~(A & B & C)"
print(e)
print(simplify_logic(e))

c = xor(term, term2) + " & ~(A & B & C)"
print(c)
print(simplify_logic(c))


d = ((((A & B) & ~(B & C)) | (~(A & B) & (B & C))) & ~(A & C) | (~((A & B) & ~(B & C)) | (~(A & B) & (B & C))) & (A & C)) & ~(A & B & C)
print(d)
print(simplify_logic(d))
print(simplify_logic(simplify_logic(d)))


