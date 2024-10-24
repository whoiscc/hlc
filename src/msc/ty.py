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


def write(writer, ty, typed=None):
    def transform(ty, typed):
        match ty:
            case Base():
                type_names = {UNIT: "void", I32: "int32_t", U8: "uint8_t", BOOL: "int"}
                return type_names[ty], [("__call__", typed)]
            case Pointer():
                base_ty, inner = transform(ty.inner, typed)
                return base_ty, [("parens", [("<<=", "*"), *inner])]
            case Array():
                base_ty, inner = transform(ty.inner, typed)
                return base_ty, [("parens", [*inner, ("brackets", [("<<=", str(ty.size))])])]
            case _:
                raise TypeError(ty)

    base_ty, commands = transform(ty, typed)
    writer <<= base_ty
    if commands == [("__call__", None)]:
        return
    writer.space()

    def execute(writer, command):
        match command:
            case ("__call__", typed):
                if typed is not None:
                    typed(writer)
            case ("<<=", content):
                writer <<= content
            case ("parens", commands):
                with writer.parens():
                    for command in commands:
                        execute(writer, command)
            case ("brackets", commands):
                with writer.brackets():
                    for command in commands:
                        execute(writer, command)
            case _:  # no cov
                raise ValueError(command)

    for command in commands:
        execute(writer, command)


def writer_declare(writer, ty, name):
    def typed(writer):
        writer <<= name

    write(writer, ty, typed)
