import sys
from pycaboose import marshal
from pycaboose.tailwriter import TailWriter

FLAG = b'# pycaboose #\n'


class Database:
    def __init__(self):
        self._writer = TailWriter(sys.argv[0], FLAG)
        self._db = {}
        for pos, s in self._writer.read():
            key, value = marshal.decode(s)
            self._db[key] = CacheLine(pos, value, s)

    def read(self, key):
        cl = self._db.get(key)
        return cl and cl.value

    def write(self, key, value):
        if key in self._db:
            self._writer.shrink(self._db[key].pos)
            for k in self._db:
                if self._db[k].pos > self._db[key].pos:
                    self._db[k].pos = self._writer.write(self._db[k].comment)
        comment = marshal.encode((key, value))
        pos = self._writer.write(comment)
        self._db[key] = CacheLine(pos, value, comment)


class CacheLine:
    def __init__(self, pos, value, comment):
        self.pos = pos
        self.value = value
        self.comment = comment
