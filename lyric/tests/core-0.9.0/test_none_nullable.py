# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for None as a first-class nullable value for all types."""

import sys
import io

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


def parse(source: str):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
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
        ast = parse(code)
        evaluate(ast)
    finally:
        sys.stdout = old_stdout
    return captured.getvalue().strip()


class TestNoneDeclarations:
    """Test that all typed variables can be assigned None."""

    def test_int_none(self):
        out = run_code_capture('int x = None\nprint(x)')
        assert out == "None"

    def test_str_none(self):
        out = run_code_capture('str s = None\nprint(s)')
        assert out == "None"

    def test_flt_none(self):
        out = run_code_capture('flt f = None\nprint(f)')
        assert out == "None"

    def test_arr_none(self):
        out = run_code_capture('arr a = None\nprint(a)')
        assert out == "None"

    def test_map_none(self):
        out = run_code_capture('map m = None\nprint(m)')
        assert out == "None"

    def test_tup_none(self):
        out = run_code_capture('tup t = None\nprint(t)')
        assert out == "None"

    def test_god_none(self):
        out = run_code_capture('god g = None\nprint(g)')
        assert out == "None"

    def test_bin_none(self):
        out = run_code_capture('bin b = None\nprint(b)')
        assert out == "None"


class TestNoneReassignment:
    """Test reassignment between None and typed values."""

    def test_none_to_typed_value(self):
        """Declare as None, then assign a proper typed value."""
        out = run_code_capture('int x = None\nx = 42\nprint(x)')
        assert out == "42"

    def test_typed_value_to_none(self):
        """Declare with a value, then assign None."""
        out = run_code_capture('int x = 5\nx = None\nprint(x)')
        assert out == "None"

    def test_str_none_to_value(self):
        out = run_code_capture('str s = None\ns = "hello"\nprint(s)')
        assert out == "hello"

    def test_arr_none_to_value(self):
        out = run_code_capture('arr a = None\na = [1, 2, 3]\nprint(a)')
        assert out == "[1, 2, 3]"

    def test_map_none_to_value(self):
        out = run_code_capture('map m = None\nm = {"key": "val"}\nprint(m["key"])')
        assert out == "val"


class TestNoneComparison:
    """Test None equality and inequality comparisons."""

    def test_none_equals_none(self):
        out = run_code_capture('int x = None\nprint(x == None)')
        assert out == "True"

    def test_value_not_equals_none(self):
        out = run_code_capture('int x = 5\nprint(x != None)')
        assert out == "True"

    def test_value_equals_none_false(self):
        out = run_code_capture('str s = "hello"\nprint(s == None)')
        assert out == "False"

    def test_none_conditional(self):
        """Test if/else branching on None check."""
        code = 'map items = None\nif items == None:\n    print("is null")\nelse:\n    print("has value")\nend'
        assert run_code_capture(code) == "is null"

    def test_not_none_conditional(self):
        code = 'map items = {"a": 1}\nif items == None:\n    print("is null")\nelse:\n    print("has value")\nend'
        assert run_code_capture(code) == "has value"


class TestNoneFunctionParams:
    """Test that typed function parameters accept None."""

    def test_typed_param_accepts_none(self):
        code = 'def show(str msg) {\nif msg == None:\n    print("no message")\nelse:\n    print(msg)\nend\n}\nshow(None)'
        assert run_code_capture(code) == "no message"

    def test_typed_param_accepts_value(self):
        code = 'def show(str msg) {\nif msg == None:\n    print("no message")\nelse:\n    print(msg)\nend\n}\nshow("hello")'
        assert run_code_capture(code) == "hello"


class TestNoneFunctionReturns:
    """Test that typed functions can return None."""

    def test_explicit_none_return(self):
        code = 'str find_item(str name) {\nif name == "missing":\n    return None\nend\nreturn "found: " + name\n}\nprint(find_item("missing"))\nprint(find_item("apple"))'
        assert run_code_capture(code) == "None\nfound: apple"

    def test_implicit_none_return(self):
        """Function with typed return that doesn't explicitly return gives None."""
        code = 'int maybe_compute(god flag) {\nif flag:\n    return 42\nend\n}\nvar result = maybe_compute(false)\nprint(result)'
        assert run_code_capture(code) == "None"


class TestNoneOperationErrors:
    """Test that operations on None fail gracefully."""

    def test_arithmetic_on_none_fails(self):
        code = 'int x = None\nint y = x + 1'
        with pytest.raises(RuntimeErrorLyric):
            ast = parse(code)
            evaluate(ast)

    def test_none_is_falsy(self):
        """None should be falsy in boolean context."""
        code = 'var x = None\nif x:\n    print("truthy")\nelse:\n    print("falsy")\nend'
        assert run_code_capture(code) == "falsy"
