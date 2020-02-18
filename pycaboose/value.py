import inspect
from .database import Database


class Value:
    _db = None
    def __init__(self, value, key=None):
        type(self)._db = self._db or Database()
        self._key = key or inspect.currentframe().f_back.f_lineno
        self._value = self._db.read(self._key) or value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._db.write(self._key, value)
        
    def __call__(self, value=None):
        if value:
            self.value = value
        return self.value

    def __add__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __mul__(self, other):
        return self.value * other

    def __truediv__(self, other):
        return self.value / other

    def __floordiv__(self, other):
        return self.value // other

    def __mod__(self, other):
        return self.value % other

    def __pow__(self, other):
        return self.value ** other

    def __lt__(self, other):
        return self.value < other

    def __gt__(self, other):
        return self.value > other

    def __le__(self, other):
        return self.value <= other

    def __ge__(self, other):
        return self.value >= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __isub__(self, other):
        self.value -= other
        return self

    def __iadd__(self, other):
        self.value += other
        return self

    def __imul__(self, other):
        self.value *= other
        return self

    def __idiv__(self, other):
        self.value /= other
        return self

    def __ifloordiv__(self, other):
        self.value //= other
        return self

    def __imod__(self, other):
        self.value %= other
        return self

    def __ipow__(self, other):
        self.value **= other
        return self

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value

    def __invert__(self):
        return ~self.value
