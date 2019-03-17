from numpy import int32
from parse.group import Group
from parse.group import GroupComment
from parse.group import GroupIdentifier
from parse.group import GroupLine
from parse.group import GroupNumber
from parse.group import parse_group
from parse.word import WordComment
from parse.word import WordIdentifier
from parse.word import WordLine
from parse.word import WordNumber
from test import params


def params_group():
    yield [], Group([])
    yield [WordLine(indent=0, terms=[])], Group(
        [GroupLine([])]
    )
    yield [
        WordLine(indent=0, terms=[WordIdentifier("abc")])
    ], Group([GroupLine([GroupIdentifier("abc")])])
    yield [
        WordLine(indent=0, terms=[WordNumber(int32(1))]),
        WordLine(indent=0, terms=[WordNumber(int32(2))]),
        WordLine(indent=2, terms=[WordNumber(int32(3))]),
    ], Group(
        [
            GroupLine([GroupNumber(int32(1))]),
            GroupLine(
                [
                    GroupNumber(int32(2)),
                    Group(
                        [GroupLine([GroupNumber(int32(3))])]
                    ),
                ]
            ),
        ]
    )
    yield [
        WordLine(indent=0, terms=[WordIdentifier("a")]),
        WordLine(indent=2, terms=[WordIdentifier("b")]),
        WordLine(indent=2, terms=[WordIdentifier("c")]),
        WordLine(indent=0, terms=[]),
        WordLine(indent=2, terms=[]),
        WordLine(indent=3, terms=[]),
    ], Group(
        [
            GroupLine(
                [
                    GroupIdentifier("a"),
                    Group(
                        [
                            GroupLine(
                                [GroupIdentifier("b")]
                            ),
                            GroupLine(
                                [GroupIdentifier("c")]
                            ),
                            GroupLine([]),
                            GroupLine([]),
                            GroupLine([]),
                        ]
                    ),
                ]
            )
        ]
    )
    yield [
        WordLine(indent=0, terms=[WordIdentifier("x")]),
        WordLine(indent=2, terms=[WordIdentifier("y")]),
        WordLine(indent=2, terms=[WordComment("0")]),
        WordLine(indent=3, terms=[WordComment("1")]),
        WordLine(indent=1, terms=[WordComment("2")]),
        WordLine(indent=0, terms=[WordIdentifier("z")]),
    ], Group(
        [
            GroupLine(
                [
                    GroupIdentifier("x"),
                    Group(
                        [
                            GroupLine(
                                [GroupIdentifier("y")]
                            ),
                            GroupLine([GroupComment("0")]),
                            GroupLine([GroupComment("1")]),
                        ]
                    ),
                ]
            ),
            GroupLine([GroupComment("2")]),
            GroupLine([GroupIdentifier("z")]),
        ]
    )


@params(params_group)
def test_group(lines, expected_result):
    assert parse_group(lines) == expected_result
