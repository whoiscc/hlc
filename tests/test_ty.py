from msc import Writer
from msc.ty import U8, UNIT, Array, Pointer, write


def test_base():
    w = Writer()
    write(UNIT, w)
    assert w.content == "void"


def test_pointer():
    w = Writer()
    write(Pointer(U8), w)
    assert w.content == "uint8_t *"


def test_array():
    w = Writer()
    write(Array(U8, 32), w)
    assert w.content == "uint8_t[32]"
