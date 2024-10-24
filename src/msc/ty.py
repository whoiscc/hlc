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


def write(writer, ty, then=None):
    match ty:
        case Base():
            type_names = {UNIT: "void", I32: "int32_t", U8: "uint8_t", BOOL: "int"}
            writer <<= type_names[ty]
            if then is not None:
                writer.space()
                then(writer)
        case Pointer():

            def inner(writer):
                with writer.parens():
                    writer <<= "*"
                    if then is not None:
                        then(writer)

            write(writer, ty.inner, inner)
        case Array():

            def inner(writer):
                with writer.parens():
                    if then is not None:
                        then(writer)
                    with writer.brackets():
                        writer <<= str(ty.size)

            write(writer, ty.inner, inner)
        case _:
            raise TypeError(ty)


def write_typed(writer, name, ty):
    def then(writer):
        writer <<= name

    write(writer, ty, then)
