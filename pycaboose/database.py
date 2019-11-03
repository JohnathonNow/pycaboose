import sys
import base64
import pickle
import mmap
import atexit

CHECKSUM = b"# pycaboose #\n"


class Database:
    def __init__(self):
        with open(sys.argv[0], "r+b") as f:
            self._mm = mmap.mmap(f.fileno(), 0)
            self._mapping = {}
            self.seek()

        def exit_handler():
            self._mm.close()

        atexit.register(exit_handler)

    def seek(self):
        checksum = True
        line = 0
        while checksum and checksum != CHECKSUM:
            line += 1
            checksum = self._mm.readline()
        if not checksum:
            statesize = len(CHECKSUM)
            self._mm.resize(self._mm.size()+statesize)
            self._mm.write(CHECKSUM)
        else:
            s = True
            while s:
                tell = self._mm.tell()
                s = self._mm.readline()
                if not s:
                    break
                line, value = pickle.loads(base64.b64decode(s[2:]))
                self._mapping[line] = (tell, s, value)

    def read(self, line):
        return self._mapping.get(line, (None, None, None))[2]

    def _write_mapping(self, line, data):
        self._mm.seek(0, 2)
        tell = self._mm.tell()
        self._mapping[line] = (tell,) + data
        self._mm.resize(self._mm.size()+len(data[0]))
        self._mm.write(data[0])

    def _write_obj(self, line):
        y = self._mapping[line]
        self._write_mapping(line, (y[1], y[2]))

    def _write_new(self, line, value):
        x = base64.b64encode(pickle.dumps((line, value)))
        x = b'# ' + x + b'\n'
        self._write_mapping(line, (x, value))

    def write(self, line, value):
        if line in self._mapping:
            pos = self._mapping[line][0]
            self._mm.resize(pos)
            for l in self._mapping:
                if self._mapping[l][0] > pos:
                    self._write_obj(l)

        self._write_new(line, value)
