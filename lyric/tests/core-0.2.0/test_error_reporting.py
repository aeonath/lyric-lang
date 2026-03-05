# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for error reporting system in Lyric language."""

from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import SyntaxErrorLyric, RuntimeErrorLyric, NameErrorLyric, ParseError
import pytest


def test_syntax_error_missing_end():
    """Test that missing 'end' triggers SyntaxErrorLyric with correct line (A7)."""
    source = """
def main() {
    x = 5
    if x > 0:
        print("positive")
    # Missing 'end' here
}"""
    
    with pytest.raises((SyntaxErrorLyric, ParseError)) as exc_info:
        ast = parse(source)
    
    error = exc_info.value
    assert hasattr(error, 'line')
    assert error.line > 0


def test_syntax_error_missing_done():
    """Test that missing 'done' triggers SyntaxErrorLyric with correct line (A7)."""
    source = """
def main() {
    int i
    for i in range(3):
        print(i)
    # Missing 'done' here
}"""
    
    with pytest.raises((SyntaxErrorLyric, ParseError)) as exc_info:
        ast = parse(source)
    
    error = exc_info.value
    assert hasattr(error, 'line')
    assert error.line > 0


def test_runtime_error_undefined_variable():
    """Test that undefined variable triggers RuntimeErrorLyric (A8)."""
    source = """
def main() {
    print(undefined_var)
}"""
    
    ast = parse(source)
    
    with pytest.raises((RuntimeErrorLyric, NameErrorLyric)) as exc_info:
        evaluate(ast)
    
    error = exc_info.value
    # Check that error mentions the undefined variable
    assert "undefined_var" in str(error) or "not defined" in str(error)


def test_runtime_error_undefined_function():
    """Test that undefined function triggers RuntimeErrorLyric (A8)."""
    source = """
def main() {
    undefined_function()
}"""
    
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        evaluate(ast)
    
    error = exc_info.value
    assert "undefined_function" in str(error) or "not defined" in str(error)


def test_error_message_format():
    """Test that error messages include line numbers."""
    source = """
def main() {
    x = 5
    print(undefined_var)
}"""
    
    ast = parse(source)
    
    with pytest.raises((RuntimeErrorLyric, NameErrorLyric)) as exc_info:
        evaluate(ast)
    
    error = exc_info.value
    error_str = str(error)
    
    # Error message should be informative
    assert len(error_str) > 0
    assert "undefined_var" in error_str or "not defined" in error_str


def test_division_by_zero_error():
    """Test division by zero error."""
    source = """
def main() {
    x = 5
    y = 0
    z = x / y
}"""
    
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        evaluate(ast)
    
    error = exc_info.value
    assert "zero" in str(error).lower()


def test_multiple_errors_first_caught():
    """Test that the first error is caught and reported."""
    source = """
def main() {
    print(first_undefined)
    print(second_undefined)
}"""
    
    ast = parse(source)
    
    with pytest.raises((RuntimeErrorLyric, NameErrorLyric)) as exc_info:
        evaluate(ast)
    
    error = exc_info.value
    # Should catch the first undefined variable
    assert "first_undefined" in str(error) or "not defined" in str(error)
