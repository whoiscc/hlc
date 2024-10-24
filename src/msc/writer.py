from contextlib import contextmanager


class Writer:
    def __init__(self, buf=None, level_space=2):
        self.buf = buf or []
        self.level = 0

        self.level_space = level_space

    def append(self, content):
        if self.buf and self.buf[-1].endswith("\n"):
            self.buf.append(" " * (self.level * self.level_space))
        self.buf.append(content)

    def space(self):
        self.buf.append(" ")

    def newline(self):
        self.buf.append("\n")

    @contextmanager
    def indent(self):
        self.level += 1
        try:
            yield
        finally:
            self.level -= 1

    @contextmanager
    def surround(self, pair):
        prefix, suffix = pair
        self.append(prefix)
        try:
            yield
        finally:
            self.append(suffix)

    # TODO: suffix punctuation if multiline
    def delimit(self, punc):
        while True:
            yield
            self.append(punc)

    @property
    def content(self):
        return "".join(self.buf)

    # utils
    def __ilshift__(self, other):
        self.append(other)
        return self

    def parens(self):
        return self.surround(("(", ")"))

    def brackets(self):
        return self.surround(("[", "]"))

    @contextmanager
    def braces(self):
        with self.surround(("{", "}")), self.indent():
            yield

    def lines(self):
        return self.delimit("\n")

    def commas(self):
        return self.delimit(",")
