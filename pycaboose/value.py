import inspect
from .database import Database


class Value:
    _db = None
    def __init__(self, value, key=None):
        self._db = self._db or Database()
        self._key = key or inspect.currentframe().f_back.f_lineno
        self._value = self._db.read(self._key) or value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._db.write(self._key, value)
