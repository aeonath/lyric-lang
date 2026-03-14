# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for runtime enhancements in Lyric language."""

from lyric.parser import parse
from lyric.interpreter import evaluate
import pytest
import io
import sys


def test_isinstance_function_a15():
    """Test isinstance built-in function (A15)."""
    source = """class Person
    var name = "Guest"
+++

def main() {
    var person = Person()

    print("isinstance(person, Person):", isinstance(person, Person))
    print("isinstance(person, str):", isinstance(person, str))
    print("isinstance(5, int):", isinstance(5, int))
    print("isinstance(5, str):", isinstance(5, str))
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "isinstance(person, Person): True" in output
        assert "isinstance(person, str): False" in output
        assert "isinstance(5, int): True" in output
        assert "isinstance(5, str): False" in output
    finally:
        sys.stdout = old_stdout


def test_type_function_a15():
    """Test type built-in function (A15)."""
    source = """class Person
    var name = "Guest"
+++

def main() {
    var person = Person()

    print("type(person):", type(person))
    print("type(5):", type(5))
    print("type(3.14):", type(3.14))
    print("type(hello):", type("hello"))
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "type(person): Person" in output
        assert "type(5): int" in output
        assert "type(3.14): float" in output
        assert "type(hello): str" in output
    finally:
        sys.stdout = old_stdout


def test_range_start_stop_a16():
    """Test range(start, stop) function (A16)."""
    source = """def main() {
    print("range(2, 5):", range(2, 5))
    print("range(0, 3):", range(0, 3))
    print("range(1, 1):", range(1, 1))
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "range(2, 5): [2, 3, 4]" in output
        assert "range(0, 3): [0, 1, 2]" in output
        assert "range(1, 1): []" in output
    finally:
        sys.stdout = old_stdout


def test_safe_print_none_a17():
    """Test safe print for None (A17)."""
    source = """def main() {
    var x = None
    print("x is:", x)
    print("None value:", None)
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "x is: None" in output
        assert "None value: None" in output
    finally:
        sys.stdout = old_stdout


def test_safe_print_lists_a17():
    """Test safe print for lists (A17)."""
    source = """def main() {
    var numbers = range(3)
    print("numbers:", numbers)

    var mixed = [1, "hello", 3.14]
    print("mixed:", mixed)
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "numbers: [0, 1, 2]" in output
        assert "mixed: [1, 'hello', 3.14]" in output
    finally:
        sys.stdout = old_stdout


def test_range_single_argument():
    """Test range with single argument still works."""
    source = """def main() {
    print("range(3):", range(3))
    print("range(0):", range(0))
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "range(3): [0, 1, 2]" in output
        assert "range(0): []" in output
    finally:
        sys.stdout = old_stdout


def test_range_three_arguments():
    """Test range with three arguments."""
    source = """def main() {
    print("range(1, 5, 2):", range(1, 5, 2))
    print("range(0, 10, 3):", range(0, 10, 3))
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "range(1, 5, 2): [1, 3]" in output
        assert "range(0, 10, 3): [0, 3, 6, 9]" in output
    finally:
        sys.stdout = old_stdout
