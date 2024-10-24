from msc import Writer
from msc.ty import U8, UNIT, Array, Pointer, write, write_typed


def test_base():
    w = Writer()
    write(w, UNIT)
    assert w.content == "void"


def test_pointer():
    w = Writer()
    write(w, Pointer(U8))
    assert w.content == "uint8_t (*)"


def test_array():
    w = Writer()
    write(w, Array(U8, 32))
    assert w.content == "uint8_t ([32])"


def test_typed():
    w = Writer()
    write_typed(w, "foo", U8)
    assert w.content == "uint8_t foo"
    w = Writer()
    write_typed(w, "foo", Pointer(U8))
    assert w.content == "uint8_t (*foo)"
    w = Writer()
    write_typed(w, "foo", Array(U8, 32))
    assert w.content == "uint8_t (foo[32])"
