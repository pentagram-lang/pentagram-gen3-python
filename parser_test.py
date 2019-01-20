import parsita

from parser import Identifier
from parser import Number
from parser import Parsers
from test import params


def lines_tests():
    yield "123", [[Number(123)]]
    yield "1 2 3", [[Number(1), Number(2), Number(3)]]
    yield "123.0", None
    yield "a-b-c", [[Identifier("a-b-c")]]
    yield "abc d e", [
        [Identifier("abc"), Identifier("d"), Identifier("e")]
    ]
    yield "123 abc", [[Number(123), Identifier("abc")]]
    yield "123 abc\n456 def", [
        [Number(123), Identifier("abc")],
        [Number(456), Identifier("def")],
    ]


@params(lines_tests)
def test_lines(text, expected_result):
    result = Parsers.lines.parse(text)
    if expected_result is not None:
        assert result == parsita.Success(expected_result)
    else:
        assert type(result) == parsita.Failure
