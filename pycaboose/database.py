import sys
import pycaboose.marshal as marshal
from .tailwriter import TailWriter

FLAG = b'# pycaboose #\n'


class Database:
    def __init__(self):
        self.writer = TailWriter(sys.argv[0], FLAG)
        self._db = {}
        for tell, s in self.writer.read():
            key, value = marshal.decode(s)
            self._db[key] = CacheLine(tell, value, s)

    def read(self, line):
        cl = self._db.get(line)
        return cl and cl.value

    def write(self, key, value):
        if key in self._db:
            self.writer.shrink(self._db[key].tell)
            for k in self._db:
                if self._db[k].tell > self._db[key].tell:
                    self._db[k].tell = self.writer.write(self._db[k].comment)
        comment = marshal.encode((key, value))
        tell = self.writer.write(comment)
        self._db[key] = CacheLine(tell, value, comment)


class CacheLine:
    def __init__(self, tell, value, comment):
        self.tell = tell
        self.value = value
        self.comment = comment
