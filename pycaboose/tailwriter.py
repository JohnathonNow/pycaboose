import atexit


class TailWriter:
    def __init__(self, fname, flag):
        self._file = open(fname, "a+b")
        self._flag = flag
        cs = self.seek()
        if not cs:
            self.write(self._flag)

        def exit_handler():
            self._file.close()

        atexit.register(exit_handler)

    def seek(self):
        flag = True
        line = 0
        self._file.seek(0)
        while flag and flag != self._flag:
            line += 1
            flag = self._file.readline()
        return flag

    def read(self):
        s = True
        while s:
            tell = self._file.tell()
            s = self._file.readline()
            if not s:
                return
            yield (tell, s)

    def write(self, data):
        self._file.seek(0, 2)
        tell = self._file.tell()
        self._file.write(data)
        return tell

    def shrink(self, tell):
        self._file.seek(tell, 0)
        self._file.truncate()
