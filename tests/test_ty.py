from msc import Writer
from msc.ty import U8, UNIT, Array, Pointer, write


def assert_write(ty, content):
    w = Writer()
    write(w, ty)
    assert w.content == content


def test_write_base():
    assert_write(UNIT, "void")


def test_write_pointer():
    assert_write(Pointer(U8), "uint8_t (*)")


def test_array():
    assert_write(Array(U8, 32), "uint8_t ([32])")


def assert_write_typed(ty, content):
    w = Writer()
    write(w, ty, "foo")
    assert w.content == content


def test_typed():
    assert_write_typed(U8, "uint8_t foo")
    assert_write_typed(Pointer(U8), "uint8_t (*foo)")
    assert_write_typed(Array(U8, 32), "uint8_t (foo[32])")


def test_compound():
    assert_write_typed(Pointer(Pointer(U8)), "uint8_t (*(*foo))")
    assert_write_typed(Array(Array(U8, 32), 32), "uint8_t ((foo[32])[32])")
    assert_write_typed(Pointer(Array(U8, 32)), "uint8_t (*(foo[32]))")
    assert_write_typed(Array(Pointer(U8), 32), "uint8_t ((*foo)[32])")
    assert_write(Pointer(Pointer(U8)), "uint8_t (*(*))")
    assert_write(Array(Array(U8, 32), 32), "uint8_t (([32])[32])")
    assert_write(Pointer(Array(U8, 32)), "uint8_t (*([32]))")
    assert_write(Array(Pointer(U8), 32), "uint8_t ((*)[32])")
