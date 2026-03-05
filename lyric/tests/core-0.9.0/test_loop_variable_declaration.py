# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for loop variable declaration requirement in Lyric.

Tests that for...in iterator loops require the loop variable to be
declared before use, and that type compatibility is enforced.
"""

import pytest
import sys
import io
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


def parse(source: str):
    """Helper to parse source code in interactive mode."""
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
    return captured.getvalue()


# --- Test 1: Undeclared loop variable with range errors ---
def test_undeclared_loop_var_range():
    """for x in range(5) without declaring x should raise RuntimeErrorLyric."""
    code = """
for x in range(5)
    print(x)
done
"""
    with pytest.raises(RuntimeErrorLyric, match="Loop variable 'x' must be declared"):
        ast = parse(code)
        evaluate(ast)


# --- Test 2: Undeclared loop variable with .items() errors ---
def test_undeclared_loop_var_items():
    """for pair in prices.items() without declaring pair should error."""
    code = """
map prices = {"apple": 1, "banana": 2}
for pair in prices.items()
    print(pair)
done
"""
    with pytest.raises(RuntimeErrorLyric, match="Loop variable 'pair' must be declared"):
        ast = parse(code)
        evaluate(ast)


# --- Test 3: Declared arr with .items() works ---
def test_declared_arr_with_items():
    """arr pair then for pair in prices.items() should succeed, pair is a list."""
    code = """
map prices = {"apple": 1, "banana": 2}
arr pair
for pair in prices.items()
    print(pair[0], "costs", pair[1])
done
"""
    output = run_code_capture(code)
    assert "apple costs 1" in output
    assert "banana costs 2" in output


# --- Test 4: Declared var with .items() works ---
def test_declared_var_with_items():
    """var pair then for pair in iterate should succeed."""
    code = """
map prices = {"apple": 1, "banana": 2}
var pair
for pair in prices.items()
    print(pair)
done
"""
    output = run_code_capture(code)
    assert output.strip() != ""


# --- Test 5: Declared int with range works ---
def test_declared_int_with_range():
    """int i then for i in range(5) should succeed."""
    code = """
int i
for i in range(5)
    print(i)
done
"""
    output = run_code_capture(code)
    lines = output.strip().split("\n")
    assert len(lines) == 5
    assert lines[0].strip() == "0"
    assert lines[4].strip() == "4"


# --- Test 6: Type mismatch int with .items() ---
def test_type_mismatch_int_with_items():
    """int x then for x in prices.items() should raise type mismatch."""
    code = """
map prices = {"apple": 1, "banana": 2}
int x
for x in prices.items()
    print(x)
done
"""
    with pytest.raises(RuntimeErrorLyric, match="Type mismatch in loop"):
        ast = parse(code)
        evaluate(ast)


# --- Test 7: Type mismatch str with range ---
def test_type_mismatch_str_with_range():
    """str s then for s in range(5) should raise type mismatch."""
    code = """
str s
for s in range(5)
    print(s)
done
"""
    with pytest.raises(RuntimeErrorLyric, match="Type mismatch in loop"):
        ast = parse(code)
        evaluate(ast)


# --- Test 8: Declared var with range works ---
def test_declared_var_with_range():
    """var i then for i in range(3) should succeed."""
    code = """
var i
for i in range(3)
    print(i)
done
"""
    output = run_code_capture(code)
    lines = output.strip().split("\n")
    assert len(lines) == 3
    assert lines[0].strip() == "0"
    assert lines[2].strip() == "2"


# --- Test 9: Declared arr iterating over list of lists ---
def test_declared_arr_iterating_list_of_lists():
    """arr row iterating over list of lists should work correctly."""
    code = """
arr matrix = [[1, 2], [3, 4], [5, 6]]
arr row
for row in matrix
    print(row[0], row[1])
done
"""
    output = run_code_capture(code)
    assert "1 2" in output
    assert "3 4" in output
    assert "5 6" in output


# --- Test 10: Declared int iterating over list of ints ---
def test_declared_int_iterating_list_of_ints():
    """int n iterating over list of ints should work correctly."""
    code = """
arr numbers = [10, 20, 30]
int n
for n in numbers
    print(n)
done
"""
    output = run_code_capture(code)
    lines = output.strip().split("\n")
    assert len(lines) == 3
    assert lines[0].strip() == "10"
    assert lines[1].strip() == "20"
    assert lines[2].strip() == "30"
