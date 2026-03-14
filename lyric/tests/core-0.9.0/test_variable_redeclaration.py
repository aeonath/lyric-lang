# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for variable redeclaration rejection.

Redeclaring a variable in the same scope is now an error.
Variables must be declared once, then reassigned without a type keyword.
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


class TestRedeclarationRejected:
    def test_var_redeclare_same_scope(self):
        """var x = 1 then var x = 2 should fail."""
        code = 'var x = 1\nvar x = 2'
        with pytest.raises(RuntimeErrorLyric, match="already declared"):
            ast = parse(code, interactive=True)
            evaluate(ast)

    def test_int_redeclare_same_scope(self):
        """int x = 1 then int x = 5 should fail."""
        code = 'int x = 1\nint x = 5'
        with pytest.raises(RuntimeErrorLyric, match="already declared"):
            ast = parse(code, interactive=True)
            evaluate(ast)

    def test_str_redeclare_same_scope(self):
        """str s = 'a' then str s = 'b' should fail."""
        code = 'str s = "hello"\nstr s = "world"'
        with pytest.raises(RuntimeErrorLyric, match="already declared"):
            ast = parse(code, interactive=True)
            evaluate(ast)

    def test_var_then_int_redeclare(self):
        """var x then int x should fail."""
        code = 'var x = 1\nint x = 5'
        with pytest.raises(RuntimeErrorLyric, match="already declared"):
            ast = parse(code, interactive=True)
            evaluate(ast)

    def test_int_then_str_redeclare(self):
        """int x then str x should fail."""
        code = 'int x = 1\nstr x = "hello"'
        with pytest.raises(RuntimeErrorLyric, match="already declared"):
            ast = parse(code, interactive=True)
            evaluate(ast)


class TestReassignmentWorks:
    def test_var_reassign(self):
        """var x = 1 then x = 2 should work."""
        code = 'var x = 1\nx = 2\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "2"

    def test_int_reassign(self):
        """int x = 1 then x = 5 should work."""
        code = 'int x = 1\nx = 5\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "5"

    def test_str_reassign(self):
        """str s = 'a' then s = 'b' should work."""
        code = 'str s = "hello"\ns = "world"\nprint(s)'
        output = run_code_capture(code)
        assert output.strip() == "world"


class TestLoopWithDeclaration:
    def test_declare_before_loop(self):
        """Declare variable before loop, reassign inside."""
        code = '''var result = ""
var x
var i
for i in [1, 2, 3]
    x = i * 10
    result = result + str(x) + " "
done
print(result)'''
        output = run_code_capture(code)
        assert output.strip() == "10 20 30"

    def test_typed_declare_before_loop(self):
        """Typed declaration before loop, reassign inside."""
        code = '''int total = 0
int x
var i
for i in [5, 10, 15]
    x = i + 1
    total = total + x
done
print(total)'''
        output = run_code_capture(code)
        assert output.strip() == "33"


class TestUndeclaredVariableRejected:
    def test_bare_assignment_fails(self):
        """x = 5 without declaration should fail."""
        code = 'x = 5'
        with pytest.raises(RuntimeErrorLyric, match="not declared"):
            ast = parse(code, interactive=True)
            evaluate(ast)

    def test_bare_assignment_in_function_fails(self):
        """Bare assignment inside a function should fail."""
        code = '''def main() {
    x = 5
}'''
        with pytest.raises(RuntimeErrorLyric, match="not declared"):
            ast = parse(code)
            evaluate(ast)
