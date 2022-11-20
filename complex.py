import math

class complexNumber:
    def __init__(self, r, i):
        self.r = r
        self.i = i
    
    def length(self):
        return math.sqrt(math.pow(self.r, 2) + math.pow(self.i, 2))

    def squared(self):
        return complexNumber(math.pow(self.r, 2) - (math.pow(self.i, 2)), 2 * self.r * self.i)

    def cubed(self):#a^3(r) +  3a^2b(i) +  3ab^2(r) +  b^3(i)
        return complexNumber(math.pow(self.r, 3) + 3 * self.r * self.i, 3 * math.pow(self.r, 2) * self.i + math.pow(self.i, 3))

    def multiply(self, other):
        return complexNumber(self.r * other.r - self.i * other.i, self.r * other.i + self.i * other.r)

    def divide(self, other):
        if type(other) == complexNumber:
            multi = complexNumber(other.r, -other.i)

            numerator = self.multiply(multi)
            denominator = math.pow(other.r, 2) + math.pow(other.i, 2)
            if denominator == 0:
                return None
            return complexNumber(numerator.r / denominator, numerator.i / denominator)
        else:
            complexNumber(self.r / other, self.i / other)

    def abs(self):
        return complexNumber(abs(self.r), abs(self.i))

    def __add__(self, other):
        return complexNumber(self.r + other.r, self.i + other.i)
    
    def __sub__(self, other):
        if type(other) == complexNumber:
            return complexNumber(self.r - other.r, self.i - other.i)
        else:
            return complexNumber(self.r - other, self.i)

    def __mul__(self, other):
        return complexNumber(self.r * other, self.i * other)

    def __eq__(self, other):
        return (self.r == self.r and self.i == other.i)

    def __str__(self):
        if self.i == 0:
            return f"{self.r} + 0i"
        else:
            oper = "-" if self.i < 0 else "+"
            return f"{self.r} {oper} {abs(self.i)}i"
    
    def __repr__(self):
        return f"{self.r},{self.i}"