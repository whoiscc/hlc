class Base:
    pass


UNIT = Base()
I32 = Base()
U8 = Base()
BOOL = Base()


class Pointer:
    def __init__(self, inner):
        self.inner = inner

    def __eq__(self, other):
        return isinstance(other, Pointer) and self.inner == other.inner

    def __hash__(self):
        return hash(self.inner)


class Array:
    def __init__(self, inner, size):
        self.inner = inner
        self.size = size

    def __eq__(self, other):
        return isinstance(other, Array) and (self.inner, self.size) == (other.inner, other.size)

    def __hash__(self):
        return hash((self.inner, self.size))


def write_typed(ty, write_term, writer):
    if isinstance(ty, Base):
        names = {UNIT: "void", I32: "int32_t", U8: "uint8_t", BOOL: "int"}
        writer <<= names[ty]
        write_term(writer)
        return
    if isinstance(ty, Pointer):
        write(ty.inner, writer)
        if isinstance(ty.inner, Pointer):
            writer <<= "*"
        else:
            writer <<= " *"
        write_term(writer)
        return
    if isinstance(ty, Array):
        write_typed(ty.inner, write_term, writer)
        with writer.brackets():
            writer <<= str(ty.size)
        return
    raise TypeError(ty)


def write(ty, writer):
    # TODO: caution on this
    write_typed(ty, lambda _: None, writer)
