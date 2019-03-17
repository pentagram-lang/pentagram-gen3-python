from numpy import int32
from parse.group import Group
from parse.group import GroupComment
from parse.group import GroupIdentifier
from parse.group import GroupLine
from parse.group import GroupNumber
from parse.statement import parse_statements_block
from syntax import SyntaxAssignment
from syntax import SyntaxBlock
from syntax import SyntaxComment
from syntax import SyntaxExpression
from syntax import SyntaxIdentifier
from syntax import SyntaxNumber
from test import params


def params_statements():
    yield Group(
        [GroupLine([GroupIdentifier("abc")])]
    ), SyntaxBlock(
        [SyntaxExpression([SyntaxIdentifier("abc")])]
    )
    yield Group(
        [
            GroupLine(
                [
                    GroupComment(" txt"),
                    Group(
                        [GroupLine([GroupNumber(int32(0))])]
                    ),
                ]
            )
        ]
    ), SyntaxBlock(
        [
            SyntaxExpression(
                [
                    SyntaxComment(" txt"),
                    SyntaxBlock(
                        [
                            SyntaxExpression(
                                [SyntaxNumber(int32(0))]
                            )
                        ]
                    ),
                ]
            )
        ]
    )
    yield Group(
        [
            GroupLine(
                [
                    GroupIdentifier("x"),
                    GroupIdentifier("="),
                    GroupIdentifier("y"),
                ]
            )
        ]
    ), SyntaxBlock(
        [
            SyntaxAssignment(
                terms=[SyntaxIdentifier("y")],
                bindings=[SyntaxIdentifier("x")],
            )
        ]
    )
    yield Group(
        [
            GroupLine(
                [
                    GroupIdentifier("a"),
                    GroupIdentifier("b"),
                    GroupIdentifier("="),
                    GroupIdentifier("c"),
                    Group(
                        [
                            GroupLine(
                                [
                                    GroupIdentifier("d"),
                                    GroupIdentifier("="),
                                    GroupIdentifier("e"),
                                ]
                            ),
                            GroupLine(
                                [
                                    GroupIdentifier("f"),
                                    GroupIdentifier("g"),
                                ]
                            ),
                        ]
                    ),
                ]
            )
        ]
    ), SyntaxBlock(
        [
            SyntaxAssignment(
                terms=[
                    SyntaxIdentifier("c"),
                    SyntaxBlock(
                        [
                            SyntaxAssignment(
                                terms=[
                                    SyntaxIdentifier("e")
                                ],
                                bindings=[
                                    SyntaxIdentifier("d")
                                ],
                            ),
                            SyntaxExpression(
                                [
                                    SyntaxIdentifier("f"),
                                    SyntaxIdentifier("g"),
                                ]
                            ),
                        ]
                    ),
                ],
                bindings=[
                    SyntaxIdentifier("a"),
                    SyntaxIdentifier("b"),
                ],
            )
        ]
    )


@params(params_statements)
def test_statements(group, expected_result):
    assert parse_statements_block(group) == expected_result
