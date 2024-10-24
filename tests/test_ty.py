from msc import Writer
from msc.ty import U8, UNIT, Array, Pointer, write, writer_declare


def assert_write(ty, content):
    w = Writer()
    write(w, ty)
    assert w.content == content


def test_write_base():
    assert_write(UNIT, "void")


def test_write_pointer():
    assert_write(Pointer(U8), "uint8_t (*)")


def test_write_array():
    assert_write(Array(U8, 32), "uint8_t ([32])")


def assert_write_declare(ty, content):
    w = Writer()
    writer_declare(w, ty, "foo")
    assert w.content == content


def test_write_typed():
    assert_write_declare(U8, "uint8_t foo")
    assert_write_declare(Pointer(U8), "uint8_t (*foo)")
    assert_write_declare(Array(U8, 32), "uint8_t (foo[32])")


def test_write_compound():
    assert_write_declare(Pointer(Pointer(U8)), "uint8_t (*(*foo))")
    assert_write_declare(Array(Array(U8, 32), 32), "uint8_t ((foo[32])[32])")
    assert_write_declare(Pointer(Array(U8, 32)), "uint8_t (*(foo[32]))")
    assert_write_declare(Array(Pointer(U8), 32), "uint8_t ((*foo)[32])")
    assert_write(Pointer(Pointer(U8)), "uint8_t (*(*))")
    assert_write(Array(Array(U8, 32), 32), "uint8_t (([32])[32])")
    assert_write(Pointer(Array(U8, 32)), "uint8_t (*([32]))")
    assert_write(Array(Pointer(U8), 32), "uint8_t ((*)[32])")
