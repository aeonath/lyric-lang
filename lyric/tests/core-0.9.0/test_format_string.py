# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for string format operator (%)."""

import sys
import io

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter


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


class TestFormatStringOperator:
    """Tests for the % string format operator."""

    def test_format_string_single_string(self):
        """Test %s with a single string value."""
        code = '''\
str name = "World"
str s = "Hello %s" % name
print(s)
'''
        assert run_code_capture(code) == "Hello World"

    def test_format_string_single_int(self):
        """Test %d with a single integer value."""
        code = '''\
int x = 42
str s = "Value: %d" % x
print(s)
'''
        assert run_code_capture(code) == "Value: 42"

    def test_format_string_tuple_multiple(self):
        """Test % with a tuple of multiple values."""
        code = '''\
str name = "Alice"
int score = 100
str s = "Player %s has %d points" % (name, score)
print(s)
'''
        assert run_code_capture(code) == "Player Alice has 100 points"

    def test_format_string_float(self):
        """Test %f with a float value."""
        code = '''\
flt pi = 3.14159
str s = "Pi is %.2f" % pi
print(s)
'''
        assert run_code_capture(code) == "Pi is 3.14"

    def test_format_string_hex(self):
        """Test %x for hexadecimal formatting."""
        code = '''\
int val = 255
str s = "Hex: %x" % val
print(s)
'''
        assert run_code_capture(code) == "Hex: ff"

    def test_format_string_mixed_tuple(self):
        """Test % with mixed types in a tuple."""
        code = '''\
str s = "%s is %d years old and %.1f meters tall" % ("Bob", 25, 1.8)
print(s)
'''
        assert run_code_capture(code) == "Bob is 25 years old and 1.8 meters tall"

    def test_format_string_percent_literal(self):
        """Test %% to produce a literal percent sign."""
        code = '''\
int pct = 95
str s = "Score: %d%%" % pct
print(s)
'''
        assert run_code_capture(code) == "Score: 95%"

    def test_modulo_still_works(self):
        """Ensure integer modulo still works after adding format strings."""
        code = '''\
int x = 10 % 3
print(x)
'''
        assert run_code_capture(code) == "1"

    def test_modulo_assignment_still_works(self):
        """Ensure %= still works for integer modulo assignment."""
        code = '''\
int x = 10
x %= 3
print(x)
'''
        assert run_code_capture(code) == "1"

    def test_format_string_in_print(self):
        """Test format string used directly in print()."""
        code = '''\
print("Hello %s!" % "World")
'''
        assert run_code_capture(code) == "Hello World!"

    def test_format_string_padding(self):
        """Test %10s for right-aligned padding."""
        code = '''\
str s = "[%10s]" % "hi"
print(s)
'''
        assert run_code_capture(code) == "[        hi]"
