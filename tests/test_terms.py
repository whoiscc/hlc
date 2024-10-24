from textwrap import dedent

from msc import Writer
from msc.terms import Function, Interp, Literal, Variable, write
from msc.ty import U8, UNIT, Pointer


def test_empty_function():
    f = Function("f", "void")
    assert f.block.stmts == []


def test_loop():
    f = Function("f", "void")
    with f.block.loop("loop check") as b:
        b <<= "loop stmt"
    assert len(f.block.stmts) == 1
    stmt = f.block.stmts[0]
    assert stmt.check == "loop check"
    assert stmt.block.stmts == ["loop stmt"]


def test_if():
    f = Function("f", "void")
    with f.block.cases().when("if check") as b:
        b <<= "if stmt"
    assert len(f.block.stmts) == 1
    stmt = f.block.stmts[0]
    assert stmt.check == "if check"
    assert stmt.pos.stmts == ["if stmt"]
    assert stmt.neg.stmts == []


def test_cases():
    f = Function("f", "void")
    cases = f.block.cases()
    with cases.when("if check") as b:
        b <<= "if stmt"
    with cases.when("else if check") as b:
        b <<= "else if stmt"
    with cases.otherwise() as b:
        b <<= "else stmt"
    assert len(f.block.stmts) == 1
    stmt = f.block.stmts[0]
    assert stmt.check == "if check"
    assert stmt.pos.stmts == ["if stmt"]
    assert len(stmt.neg.stmts) == 1
    stmt = stmt.neg.stmts[0]
    assert stmt.check == "else if check"
    assert stmt.pos.stmts == ["else if stmt"]
    assert stmt.neg.stmts == ["else stmt"]


def test_multiple_cases():
    f = Function("f", "void")
    with f.block.cases().when("if check") as b:
        b <<= "if stmt"
    with f.block.cases().when("another if check") as b:
        b <<= "another if stmt"
    assert len(f.block.stmts) == 2
    stmt = f.block.stmts[0]
    assert stmt.check == "if check"
    assert stmt.pos.stmts == ["if stmt"]
    assert stmt.neg.stmts == []
    stmt = f.block.stmts[1]
    assert stmt.check == "another if check"
    assert stmt.pos.stmts == ["another if stmt"]
    assert stmt.neg.stmts == []


def assert_write(term, content):
    w = Writer()
    write(w, term)
    assert w.content == dedent(content)


def test_write_empty_function():
    assert_write(Function("foo", UNIT), "void foo() {}")


def test_write_function_return_type():
    assert_write(Function("foo", Pointer(UNIT)), "void (*foo()) {}")


def test_write_param():
    f = Function("foo", UNIT)
    f += Variable(U8)
    assert_write(f, "void foo(uint8_t v0) {}")


def test_write_declare():
    f = Function("foo", UNIT)
    f.block += Variable(U8)
    assert_write(
        f,
        """\
        void foo() {
          uint8_t v0;
        }""",
    )


def test_write_loop():
    f = Function("foo", UNIT)
    with f.block.loop(Literal(1)) as b:
        b <<= Literal(0)
    assert_write(
        f,
        """\
        void foo() {
          while (1) {
            0;
          }
        }""",
    )


def test_write_branch():
    f = Function("foo", UNIT)
    with f.block.cases().when(Literal(1)) as b:
        b <<= Literal(0)
    assert_write(
        f,
        """\
        void foo() {
          if (1) {
            0;
          } else {}
        }""",
    )


def test_write_interpolate():
    f = Function("foo", U8)
    v = Variable(U8)
    f.block += v
    f.block <<= Interp("return {x}", x=v)
    assert_write(
        f,
        """\
        uint8_t foo() {
          uint8_t v0;
          return v0;
        }""",
    )
