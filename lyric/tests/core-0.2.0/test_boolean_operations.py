# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for boolean and comparison operations in Lyric language."""

from lyric.parser import parse
from lyric.interpreter import evaluate
import io
import sys


def test_comparison_operators():
    """Test all comparison operators (A4)."""
    source = """
def main() {
    x = 5
    y = 3
    
    if x == 5:
        print("x equals 5")
    end
    
    if x != 3:
        print("x does not equal 3")
    end
    
    if x > 3:
        print("x is greater than 3")
    end
    
    if x >= 5:
        print("x is greater than or equal to 5")
    end
    
    if y < 5:
        print("y is less than 5")
    end
    
    if y <= 3:
        print("y is less than or equal to 3")
    end
}"""
    
    ast = parse(source)
    
    # Capture print output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check exact output
        output = captured_output.getvalue().strip()
        expected = """x equals 5
x does not equal 3
x is greater than 3
x is greater than or equal to 5
y is less than 5
y is less than or equal to 3"""
        assert output == expected
    finally:
        sys.stdout = old_stdout


def test_logical_operators():
    """Test logical operators and, or, not (A4)."""
    source = """
def main() {
    x = 5
    y = 0
    
    if x > 0 and y == 0:
        print("Both conditions true")
    end
    
    if x == 0 or y == 0:
        print("At least one condition true")
    end
    
    if not (x == 0):
        print("x is not zero")
    end
}"""
    
    ast = parse(source)
    
    # Capture print output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check exact output
        output = captured_output.getvalue().strip()
        expected = """Both conditions true
At least one condition true
x is not zero"""
        assert output == expected
    finally:
        sys.stdout = old_stdout


def test_truthiness_rules():
    """Test truthiness rules for different types (A4)."""
    source = """
def main() {
    # Test numbers
    if 5:
        print("5 is truthy")
    end
    
    if not 0:
        print("0 is falsy")
    end
    
    # Test strings
    if "hello":
        print("non-empty string is truthy")
    end
    
    if not "":
        print("empty string is falsy")
    end
    
    # Test boolean literals
    if true:
        print("true is truthy")
    end
    
    if not false:
        print("false is falsy")
    end
}"""
    
    ast = parse(source)
    
    # Capture print output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check exact output
        output = captured_output.getvalue().strip()
        expected = """5 is truthy
0 is falsy
non-empty string is truthy
empty string is falsy
true is truthy
false is falsy"""
        assert output == expected
    finally:
        sys.stdout = old_stdout


def test_range_comparison():
    """Test range(3) and numeric comparisons (A6)."""
    source = """
def main() {
    int i
    for i in range(3):
        if i == 0:
            print("First iteration")
        elif i == 1:
            print("Second iteration")
        else:
            print("Third iteration")
        end
    done
}"""
    
    ast = parse(source)
    
    # Capture print output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check exact output
        output = captured_output.getvalue().strip()
        expected = """First iteration
Second iteration
Third iteration"""
        assert output == expected
    finally:
        sys.stdout = old_stdout


def test_complex_boolean_expressions():
    """Test complex boolean expressions with proper precedence."""
    source = """
def main() {
    x = 5
    y = 3
    z = 0
    
    if x > y and y > z:
        print("x > y and y > z")
    end
    
    if x == 5 or y == 5:
        print("x or y equals 5")
    end
    
    if not (x == 0 and y == 0):
        print("not (x == 0 and y == 0)")
    end
}"""
    
    ast = parse(source)
    
    # Capture print output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check exact output
        output = captured_output.getvalue().strip()
        expected = """x > y and y > z
x or y equals 5
not (x == 0 and y == 0)"""
        assert output == expected
    finally:
        sys.stdout = old_stdout
