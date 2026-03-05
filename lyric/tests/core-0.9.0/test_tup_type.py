# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for the native tup (tuple) type in Lyric.

Tests:
- tup type declarations and tuple literals
- Indexing operations
- Immutability (no mutation methods)
- Iteration over tup
- 'in' membership operator
- tup methods: len, count, index, sum, min, max
- Empty tuple and single-element tuple
- Type checking with tup keyword
- pyproxy conversion (TupObject -> Python tuple)
"""

import pytest
import sys
import io
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter, TupObject
from lyric.errors import TypeErrorLyric, IndexErrorLyric, RuntimeErrorLyric, ValueErrorLyric


def parse(source: str, interactive: bool = False):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    if interactive:
        parser._interactive_mode = True
        parser.is_top_level = False
    return parser.parse()


def evaluate(ast):
    """Helper to evaluate an AST."""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


def run_code_capture(code: str) -> str:
    """Run code and capture stdout output."""
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        ast = parse(code, interactive=True)
        evaluate(ast)
    finally:
        sys.stdout = old_stdout
    return captured.getvalue().strip()


class TestTupType:
    """Test the native tup type in Lyric."""

    def _run_code(self, code: str):
        """Helper function to tokenize, parse, and run code."""
        ast = parse(code, interactive=True)
        return evaluate(ast)

    # --- Declaration and literal ---

    def test_tup_declaration_multi_element(self):
        """tup type declaration with multiple elements."""
        code = """
tup t = (10, 11, 12)
print t
"""
        output = run_code_capture(code)
        assert '10' in output and '11' in output and '12' in output

    def test_tup_declaration_empty(self):
        """tup declaration with an empty tuple ()."""
        code = """
tup empty = ()
print empty
"""
        output = run_code_capture(code)
        assert output == '()'

    def test_tup_single_element_trailing_comma(self):
        """Single-element tuple via trailing comma (expr,)."""
        code = """
var single = ("only",)
print single
"""
        output = run_code_capture(code)
        assert 'only' in output

    def test_tup_mixed_types(self):
        """Tuple holding mixed types."""
        code = """
var mixed = ("hello", 42, True)
print mixed
"""
        output = run_code_capture(code)
        assert 'hello' in output and '42' in output

    def test_tup_var_inference(self):
        """Tuple literal assigned to var infers TupObject."""
        ast = parse("var pair = (1, 2)", interactive=True)
        interp = Interpreter()
        interp.evaluate(ast)
        assert isinstance(interp.global_scope['pair'], TupObject)

    def test_tup_keyword_declaration(self):
        """tup keyword declaration creates TupObject."""
        ast = parse("tup t = (7, 8, 9)", interactive=True)
        interp = Interpreter()
        interp.evaluate(ast)
        assert isinstance(interp.global_scope['t'], TupObject)

    # --- Indexing ---

    def test_tup_index_first(self):
        """Access first element by index."""
        code = """
tup t = (10, 20, 30)
print t[0]
"""
        assert run_code_capture(code) == '10'

    def test_tup_index_last(self):
        """Access last element by index."""
        code = """
tup t = (10, 20, 30)
print t[2]
"""
        assert run_code_capture(code) == '30'

    def test_tup_index_out_of_range(self):
        """IndexError on out-of-range access."""
        code = "tup t = (1, 2, 3)\nvar x = t[5]"
        with pytest.raises(IndexErrorLyric):
            self._run_code(code)

    # --- Membership ---

    def test_tup_in_operator_true(self):
        """'in' returns True for present element."""
        code = """
tup t = (10, 11, 12)
print 11 in t
"""
        assert run_code_capture(code) == 'True'

    def test_tup_in_operator_false(self):
        """'in' returns False for absent element."""
        code = """
tup t = (10, 11, 12)
print 99 in t
"""
        assert run_code_capture(code) == 'False'

    # --- Iteration ---

    def test_tup_for_iteration(self):
        """for loop iterates over tup elements."""
        code = """
tup t = (1, 2, 3)
var item
for item in t
    print item
done
"""
        output = run_code_capture(code)
        assert output == '1\n2\n3'

    # --- Methods ---

    def test_tup_len(self):
        """len() returns element count."""
        code = "tup t = (1, 2, 3)\nprint t.len()"
        assert run_code_capture(code) == '3'

    def test_tup_count(self):
        """count() counts occurrences."""
        code = "tup t = (1, 2, 2, 3)\nprint t.count(2)"
        assert run_code_capture(code) == '2'

    def test_tup_index_method(self):
        """index() returns position of first occurrence."""
        code = "tup t = (10, 20, 30)\nprint t.index(30)"
        assert run_code_capture(code) == '2'

    def test_tup_sum(self):
        """sum() returns sum of numeric elements."""
        code = "tup t = (10, 11, 12)\nprint t.sum()"
        assert run_code_capture(code) == '33'

    def test_tup_min(self):
        """min() returns smallest element."""
        code = "tup t = (5, 3, 9)\nprint t.min()"
        assert run_code_capture(code) == '3'

    def test_tup_max(self):
        """max() returns largest element."""
        code = "tup t = (5, 3, 9)\nprint t.max()"
        assert run_code_capture(code) == '9'

    def test_tup_len_empty(self):
        """len() on empty tuple returns 0."""
        code = "tup t = ()\nprint t.len()"
        assert run_code_capture(code) == '0'

    # --- Immutability ---

    def test_tup_no_append_method(self):
        """TupObject has no append method (immutable)."""
        t = TupObject([1, 2, 3])
        assert not hasattr(t, 'append')

    def test_tup_no_remove_method(self):
        """TupObject has no remove method (immutable)."""
        t = TupObject([1, 2, 3])
        assert not hasattr(t, 'remove')

    def test_tup_elements_are_tuple(self):
        """TupObject.elements is a Python tuple (immutable backing store)."""
        t = TupObject([1, 2, 3])
        assert isinstance(t.elements, tuple)

    # --- tup() builtin conversion ---

    def test_tup_builtin_from_arr(self):
        """tup() builtin converts arr to TupObject."""
        code = """
arr mylist = [1, 2, 3]
var t = tup(mylist)
print t
"""
        output = run_code_capture(code)
        assert '1' in output and '2' in output and '3' in output

    # --- pyproxy conversion ---

    def test_tupobject_converts_to_python_tuple_in_lyric_to_python(self):
        """_lyric_to_python() converts TupObject to Python tuple."""
        interp = Interpreter()
        t = TupObject([1, 2, 3])
        result = interp._lyric_to_python(t)
        assert isinstance(result, tuple)
        assert result == (1, 2, 3)
