import inspect
from .database import Database
_db = Database()


class Value:
    def __init__(self, value, key=None):
        global _db
        self._key = key or inspect.currentframe().f_back.f_lineno
        self._value = _db.read(self._key) or value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        global _db
        self._value = value
        _db.write(self._key, value)
