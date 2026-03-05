# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for the .len() method on str type.

Tests:
- .len() on string literals and variables
- Empty string .len()
- Existing Python string methods still work (.upper(), .split())
"""

import pytest
import sys
import io
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


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
    return captured.getvalue()


class TestStrLen:
    def test_str_len_variable(self):
        code = 'str s = "hello"\nprint(s.len())'
        output = run_code_capture(code)
        assert output.strip() == "5"

    def test_str_len_empty(self):
        code = 'str s = ""\nprint(s.len())'
        output = run_code_capture(code)
        assert output.strip() == "0"

    def test_str_len_with_spaces(self):
        code = 'str s = "hello world"\nprint(s.len())'
        output = run_code_capture(code)
        assert output.strip() == "11"

    def test_str_len_single_char(self):
        code = 'str s = "a"\nprint(s.len())'
        output = run_code_capture(code)
        assert output.strip() == "1"


class TestStrExistingMethods:
    def test_str_upper(self):
        code = 'str s = "hello"\nprint(s.upper())'
        output = run_code_capture(code)
        assert output.strip() == "HELLO"

    def test_str_lower(self):
        code = 'str s = "HELLO"\nprint(s.lower())'
        output = run_code_capture(code)
        assert output.strip() == "hello"

    def test_str_strip(self):
        code = 'str s = "  hello  "\nprint(s.strip())'
        output = run_code_capture(code)
        assert output.strip() == "hello"

    def test_str_replace(self):
        code = 'str s = "hello world"\nprint(s.replace("world", "lyric"))'
        output = run_code_capture(code)
        assert output.strip() == "hello lyric"


class TestStrLenErrors:
    def test_str_invalid_method(self):
        code = 'str s = "hello"\ns.nonexistent()'
        with pytest.raises(RuntimeErrorLyric):
            ast = parse(code, interactive=True)
            evaluate(ast)
