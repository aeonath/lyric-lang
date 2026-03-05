# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for variable redeclaration as reassignment.

Redeclaring a variable in the same scope now acts as reassignment
instead of raising a "Variable already declared" error. This is
essential for patterns like `var x = expr` inside loop bodies.

Tests:
- Simple redeclaration at top level
- Redeclaration inside a loop body
- Typed redeclaration respects type checks
- Multi-variable redeclaration
- Redeclaration preserves latest value
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


class TestSimpleRedeclaration:
    def test_var_redeclare_same_scope(self):
        """var x = 1 then var x = 2 should work."""
        code = 'var x = 1\nvar x = 2\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "2"

    def test_int_redeclare_same_scope(self):
        """int x = 1 then int x = 5 should work."""
        code = 'int x = 1\nint x = 5\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "5"

    def test_str_redeclare_same_scope(self):
        """str s = 'a' then str s = 'b' should work."""
        code = 'str s = "hello"\nstr s = "world"\nprint(s)'
        output = run_code_capture(code)
        assert output.strip() == "world"


class TestRedeclarationInLoop:
    def test_var_redeclare_in_loop(self):
        """var x = expr inside a loop should not fail on iteration 2+."""
        code = '''var result = ""
var i
for i in [1, 2, 3]
    var x = i * 10
    result += str(x) + " "
done
print(result)'''
        output = run_code_capture(code)
        assert output.strip() == "10 20 30"

    def test_int_redeclare_in_loop(self):
        """int x = expr inside a loop should not fail on iteration 2+."""
        code = '''int total = 0
var i
for i in [5, 10, 15]
    int x = i + 1
    total += x
done
print(total)'''
        output = run_code_capture(code)
        assert output.strip() == "33"

    def test_str_redeclare_in_loop(self):
        """str s = expr inside a loop should not fail on iteration 2+."""
        code = '''var result = ""
var word
for word in ["hello", "world"]
    str greeting = word + "!"
    result += greeting + " "
done
print(result)'''
        output = run_code_capture(code)
        assert output.strip() == "hello! world!"


class TestRedeclarationTypeChecks:
    def test_typed_redeclare_type_mismatch(self):
        """Redeclaring int x then assigning a string should still fail."""
        code = 'int x = 1\nint x = "hello"'
        with pytest.raises(RuntimeErrorLyric):
            ast = parse(code, interactive=True)
            evaluate(ast)

    def test_var_redeclare_allows_type_change(self):
        """var allows redeclaration with a different type."""
        code = 'var x = 1\nvar x = "hello"\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "hello"


class TestMultiDeclarationRedeclare:
    def test_multi_var_redeclare(self):
        """Multi-variable redeclaration should work."""
        code = 'var a, var b\nvar a, var b\nprint("ok")'
        output = run_code_capture(code)
        assert output.strip() == "ok"


class TestRedeclarationPreservesValue:
    def test_latest_value_wins(self):
        """After multiple redeclarations, the last value should persist."""
        code = 'var x = 10\nvar x = 20\nvar x = 30\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "30"
