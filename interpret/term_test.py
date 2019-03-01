from host.simple_call import sqrt
from host.value import PI
from interpret.term import interpret_identifier_term
from interpret.term import interpret_number_term
from interpret.term import next_term
from interpret.test import init_test_frame_stack
from interpret.test import test_environment
from numpy import int32
from stack_machine import ExpressionStack
from stack_machine import Frame
from stack_machine import FrameStack
from stack_machine import InstructionPointer
from stack_machine import NumberValue
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import IdentifierTerm
from syntax_tree import NumberTerm
from syntax_tree import Term


def init_term_block(term: Term) -> Block:
    return Block(
        [
            ExpressionStatement(
                Expression([term], comment=None, block=None)
            )
        ]
    )


def test_interpret_number_term():
    term = NumberTerm(int32(100))
    expression_stack = ExpressionStack([])
    frame_stack = init_test_frame_stack(
        init_term_block(term), expression_stack
    )
    interpret_number_term(frame_stack, term)
    assert frame_stack == FrameStack([])
    assert expression_stack == ExpressionStack(
        [NumberValue(int32(100))]
    )


def test_interpret_identifier_value_term():
    term = IdentifierTerm(PI.name)
    expression_stack = ExpressionStack([])
    frame_stack = init_test_frame_stack(
        init_term_block(term), expression_stack
    )
    print(frame_stack.current.environment)
    interpret_identifier_term(frame_stack, term)
    assert frame_stack == FrameStack([])
    assert expression_stack == ExpressionStack([PI.value])


def test_interpret_identifier_call_term():
    term = IdentifierTerm(sqrt.name)
    expression_stack = ExpressionStack(
        [NumberValue(int32(16))]
    )
    frame_stack = init_test_frame_stack(
        init_term_block(term), expression_stack
    )
    interpret_identifier_term(frame_stack, term)
    assert frame_stack == FrameStack([])
    assert expression_stack == ExpressionStack(
        [NumberValue(int32(4))]
    )


def test_interpret_next_term_base():
    block = Block(
        [
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(1)),
                        NumberTerm(int32(2)),
                        NumberTerm(int32(3)),
                    ],
                    comment=None,
                    block=None,
                )
            )
        ]
    )
    frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=1,
                ),
                ExpressionStack([]),
                test_environment(),
            )
        ]
    )
    next_term(frame_stack)
    expected_frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=2,
                ),
                ExpressionStack([]),
                test_environment(),
            )
        ]
    )
    assert frame_stack == expected_frame_stack


def test_interpret_next_term_end_expression():
    block = Block(
        [
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(1)),
                        NumberTerm(int32(2)),
                        NumberTerm(int32(3)),
                    ],
                    comment=None,
                    block=None,
                )
            ),
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(4)),
                        NumberTerm(int32(5)),
                        NumberTerm(int32(6)),
                    ],
                    comment=None,
                    block=None,
                )
            ),
        ]
    )
    frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=2,
                ),
                ExpressionStack([]),
                test_environment(),
            )
        ]
    )
    next_term(frame_stack)
    expected_frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=1,
                    expression_term_index=0,
                ),
                ExpressionStack([]),
                test_environment(),
            )
        ]
    )
    assert frame_stack == expected_frame_stack


def test_interpret_next_term_end_comment_expression():
    block = Block(
        [
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(1)),
                        NumberTerm(int32(2)),
                        NumberTerm(int32(3)),
                    ],
                    comment="abc",
                    block=None,
                )
            ),
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(4)),
                        NumberTerm(int32(5)),
                        NumberTerm(int32(6)),
                    ],
                    comment=None,
                    block=None,
                )
            ),
        ]
    )
    frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=2,
                ),
                ExpressionStack([]),
                test_environment(),
            )
        ]
    )
    next_term(frame_stack)
    expected_frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=1,
                    expression_term_index=0,
                ),
                ExpressionStack([]),
                test_environment(),
            )
        ]
    )
    assert frame_stack == expected_frame_stack


def test_interpret_next_term_empty_expression():
    block = Block(
        [
            ExpressionStatement(
                Expression([], comment=None, block=None)
            ),
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(4)),
                        NumberTerm(int32(5)),
                        NumberTerm(int32(6)),
                    ],
                    comment=None,
                    block=None,
                )
            ),
        ]
    )
    frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=0,
                ),
                ExpressionStack([]),
                test_environment(),
            )
        ]
    )
    next_term(frame_stack)
    expected_frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=1,
                    expression_term_index=0,
                ),
                ExpressionStack([]),
                test_environment(),
            )
        ]
    )
    assert frame_stack == expected_frame_stack


def test_interpret_next_term_end_block():
    block = Block(
        [
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(1)),
                        NumberTerm(int32(2)),
                        NumberTerm(int32(3)),
                    ],
                    comment=None,
                    block=None,
                )
            )
        ]
    )
    frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=1,
                ),
                ExpressionStack([]),
                test_environment(),
            ),
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=2,
                ),
                ExpressionStack([]),
                test_environment(),
            ),
        ]
    )
    next_term(frame_stack)
    expected_frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=1,
                ),
                ExpressionStack([]),
                test_environment(),
            )
        ]
    )
    assert frame_stack == expected_frame_stack


def test_interpret_next_term_end_last_block():
    block = Block(
        [
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(1)),
                        NumberTerm(int32(2)),
                        NumberTerm(int32(3)),
                    ],
                    comment=None,
                    block=None,
                )
            )
        ]
    )
    frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=2,
                ),
                ExpressionStack([]),
                test_environment(),
            )
        ]
    )
    next_term(frame_stack)
    expected_frame_stack = FrameStack([])
    assert frame_stack == expected_frame_stack
