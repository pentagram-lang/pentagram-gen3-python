from host.simple_call import sqrt
from host.value import PI
from interpret.term import interpret_term
from interpret.test import init_test_frame_stack
from numpy import int32
from stack_machine import ExpressionStack
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
    frame_stack = init_test_frame_stack(
        init_term_block(term), ExpressionStack([])
    )
    interpret_term(frame_stack)
    assert frame_stack == init_test_frame_stack(
        init_term_block(term),
        ExpressionStack([NumberValue(int32(100))]),
        expression_term_index=1,
    )


def test_interpret_identifier_value_term():
    term = IdentifierTerm(PI.name)
    expression_stack = ExpressionStack([])
    frame_stack = init_test_frame_stack(
        init_term_block(term), expression_stack
    )
    interpret_term(frame_stack)
    assert frame_stack == init_test_frame_stack(
        init_term_block(term),
        ExpressionStack([PI.value]),
        expression_term_index=1,
    )


def test_interpret_identifier_call_term():
    term = IdentifierTerm(sqrt.name)
    expression_stack = ExpressionStack(
        [NumberValue(int32(16))]
    )
    frame_stack = init_test_frame_stack(
        init_term_block(term), expression_stack
    )
    interpret_term(frame_stack)
    assert frame_stack == init_test_frame_stack(
        init_term_block(term),
        ExpressionStack([NumberValue(int32(4))]),
        expression_term_index=1,
    )
