import mmap
import atexit


class TailWriter:
    def __init__(self, fname, flag):
        with open(fname, "r+b") as f:
            self._mm = mmap.mmap(f.fileno(), 0)
            self.flag = flag
            cs = self.seek()
            if not cs:
                self.write(self.flag)

        def exit_handler():
            self._mm.close()

        atexit.register(exit_handler)

    def seek(self):
        flag = True
        line = 0
        while flag and flag != self.flag:
            line += 1
            flag = self._mm.readline()
        return flag

    def read(self):
        s = True
        while s:
            tell = self._mm.tell()
            s = self._mm.readline()
            if not s:
                return
            yield (tell, s)

    def write(self, data):
        self._mm.seek(0, 2)
        tell = self._mm.tell()
        self._mm.resize(self._mm.size()+len(data))
        self._mm.write(data)
        return tell

    def shrink(self, tell):
        self._mm.resize(tell)
