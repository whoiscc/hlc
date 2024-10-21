from hlc import Writer


def test_empty():
    w = Writer()
    assert w.content == ""


def test_content():
    w = Writer()
    w <<= "hello"
    assert w.content == "hello"


def test_newline():
    w = Writer()
    w <<= "hello"
    w.newline()
    assert w.content == "hello\n"


def test_lines():
    w = Writer()
    for i, _ in zip(range(3), w.lines()):
        w <<= f"line{i}"
    assert w.content == "line0\nline1\nline2"


def test_parens():
    w = Writer()
    with w.parens():
        w <<= "hello"
    assert w.content == "(hello)"


def test_braces():
    w = Writer()
    with w.braces():
        w <<= "hello"
    assert w.content == "{\n  hello\n}"
