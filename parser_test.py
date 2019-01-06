import parsita

from parser import (
    Identifier,
    Number,
    Parsers,
)
from test import params

def lines_tests():
    yield '123', [
        [Number(123)]
    ]
    yield '1 2 3', [
        [Number(1), Number(2), Number(3)]
    ]
    yield '123.0', None
    yield 'a-b-c', [
        [Identifier('a-b-c')]
    ]
    yield 'abc d e', [
        [
            Identifier('abc'),
            Identifier('d'),
            Identifier('e'),
        ]
    ]
    yield '123 abc', [
        [
            Number(123),
            Identifier('abc'),
        ]
    ]
    yield '123 abc\n456 def', [
        [
            Number(123),
            Identifier('abc'),
        ],
        [
            Number(456),
            Identifier('def'),
        ]
    ]

@params(lines_tests)
def test_lines(input, output):
    result = Parsers.lines.parse(input)
    if output is not None:
        assert result == parsita.Success(output)
    else:
        assert type(result) == parsita.Failure
