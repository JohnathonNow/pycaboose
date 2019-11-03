import inspect
from .database import Database
_db = Database()


class Value:
    def __init__(self, value, line=None):
        global _db
        self._line = line or inspect.currentframe().f_back.f_lineno
        self._value = _db.read(self._line) or value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        global _db
        self._value = value
        _db.write(self._line, value)
