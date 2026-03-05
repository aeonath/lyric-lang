# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for updated function definition syntax (Sprint 10 Task 3).

Valid forms:
  - int funcname(...)  — typed function (no 'def' keyword)
  - def funcname(...)  — untyped function

Invalid form (must be rejected):
  - int def funcname(...)  — old redundant syntax
"""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import ParseError


def parse(source: str, interactive: bool = False):
    tokens = tokenize(source)
    parser = Parser(tokens)
    if interactive:
        parser._interactive_mode = True
        parser.is_top_level = False
    return parser.parse()


def run(source: str):
    ast = parse(source, interactive=True)
    interp = Interpreter()
    interp.evaluate(ast)
    return interp


# ---------------------------------------------------------------------------
# Positive tests — valid syntax must parse and execute correctly
# ---------------------------------------------------------------------------

class TestValidFunctionSyntax:

    def test_typed_int_function(self):
        """int funcname() must parse and return the correct value."""
        code = """
int add(int a, int b) {
    return a + b
}
int result = add(3, 4)
"""
        interp = run(code)
        assert interp.global_scope.get('result') == 7

    def test_typed_str_function(self):
        """str funcname() must parse and return a string."""
        code = """
str greet(str name) {
    return "Hello, " + name
}
str msg = greet("World")
"""
        interp = run(code)
        assert interp.global_scope.get('msg') == "Hello, World"

    def test_typed_flt_function(self):
        """flt funcname() must parse and return a float."""
        code = """
flt half(int n) {
    return n / 2
}
flt result = half(10)
"""
        interp = run(code)
        assert interp.global_scope.get('result') == 5.0

    def test_untyped_def_function(self):
        """def funcname() must parse and execute correctly."""
        code = """
def square(int n) {
    return n * n
}
var result = square(6)
"""
        interp = run(code)
        assert interp.global_scope.get('result') == 36

    def test_typed_function_no_params(self):
        """Typed function with no parameters must work."""
        code = """
int get_answer() {
    return 42
}
int answer = get_answer()
"""
        interp = run(code)
        assert interp.global_scope.get('answer') == 42

    def test_def_function_no_params(self):
        """def function with no parameters must work."""
        code = """
def get_greeting() {
    return "hi"
}
var msg = get_greeting()
"""
        interp = run(code)
        assert interp.global_scope.get('msg') == "hi"

    def test_typed_map_function(self):
        """map funcname() must parse correctly."""
        code = """
map make_entry(str k, int v) {
    return {k: v}
}
map entry = make_entry("x", 99)
"""
        interp = run(code)
        entry = interp.global_scope.get('entry')
        assert entry is not None
        assert entry['x'] == 99

    def test_typed_var_function(self):
        """var funcname() must parse correctly."""
        code = """
var identity(var x) {
    return x
}
var a = identity(123)
"""
        interp = run(code)
        assert interp.global_scope.get('a') == 123

    def test_typed_arr_function(self):
        """arr funcname() must parse correctly."""
        code = """
arr get_list() {
    return [1, 2, 3]
}
arr result = get_list()
"""
        interp = run(code)
        assert list(interp.global_scope.get('result')) == [1, 2, 3]


# ---------------------------------------------------------------------------
# Negative tests — old 'TYPE def funcname()' syntax must be rejected
# ---------------------------------------------------------------------------

class TestInvalidOldFunctionSyntax:

    def test_int_def_rejected(self):
        """'int def funcname()' must raise ParseError."""
        code = """
int def add(int a, int b) {
    return a + b
}
"""
        with pytest.raises(ParseError):
            parse(code, interactive=True)

    def test_str_def_rejected(self):
        """'str def funcname()' must raise ParseError."""
        code = """
str def greet(str name) {
    return "Hi " + name
}
"""
        with pytest.raises(ParseError):
            parse(code, interactive=True)

    def test_flt_def_rejected(self):
        """'flt def funcname()' must raise ParseError."""
        code = """
flt def average(flt a, flt b) {
    return (a + b) / 2
}
"""
        with pytest.raises(ParseError):
            parse(code, interactive=True)

    def test_var_def_rejected(self):
        """'var def funcname()' must raise ParseError."""
        code = """
var def get_val() {
    return 0
}
"""
        with pytest.raises(ParseError):
            parse(code, interactive=True)

    def test_map_def_rejected(self):
        """'map def funcname()' must raise ParseError."""
        code = """
map def make_map() {
    return {}
}
"""
        with pytest.raises(ParseError):
            parse(code, interactive=True)

    def test_arr_def_rejected(self):
        """'arr def funcname()' must raise ParseError."""
        code = """
arr def get_list() {
    return [1, 2, 3]
}
"""
        with pytest.raises(ParseError):
            parse(code, interactive=True)

    def test_error_message_is_helpful(self):
        """ParseError message must mention valid alternatives."""
        code = """
int def bad(int x) {
    return x
}
"""
        with pytest.raises(ParseError) as exc_info:
            parse(code, interactive=True)
        msg = str(exc_info.value)
        assert "int def" in msg or "funcname()" in msg or "typed function" in msg or "def funcname()" in msg


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
