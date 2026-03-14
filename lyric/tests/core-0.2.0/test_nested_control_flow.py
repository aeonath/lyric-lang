# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for nested control flow in Lyric language."""

from lyric.parser import parse
from lyric.interpreter import evaluate
import io
import sys


def test_nested_control_flow():
    """Test nested if statements and loops."""
    source = """
def main() {
    var x = 5
    if x > 0:
        print("x is positive")
        if x > 3:
            print("x is greater than 3")
        else:
            print("x is 3 or less")
        end
    else:
        print("x is not positive")
    end

    int i
    for i in range(2):
        print("Outer loop:", i)
        if i == 0:
            print("  First iteration")
        else:
            print("  Second iteration")
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
        expected = """x is positive
x is greater than 3
Outer loop: 0
  First iteration
Outer loop: 1
  Second iteration"""
        assert output == expected
    finally:
        sys.stdout = old_stdout


def test_nested_loops():
    """Test nested loops (A2: loop inside if)."""
    source = """
def main() {
    var x = 2
    if x > 0:
        print("Starting nested loop test")
        int i
        int j
        for i in range(2):
            print("Outer:", i)
            for j in range(2):
                print("  Inner:", j)
            done
        done
    else:
        print("x is not positive")
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
        expected = """Starting nested loop test
Outer: 0
  Inner: 0
  Inner: 1
Outer: 1
  Inner: 0
  Inner: 1"""
        assert output == expected
    finally:
        sys.stdout = old_stdout


def test_nested_if_in_loop():
    """Test nested if statements inside loops (A2: if inside loop)."""
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


def test_complex_nested_structure():
    """Test complex nested structure with multiple levels."""
    source = """
def main() {
    var x = 1
    var y = 2

    if x > 0:
        print("x is positive")
        if y > 1:
            print("y is greater than 1")
            int i
            for i in range(2):
                print("Loop iteration:", i)
                if i == 0:
                    print("  First loop iteration")
                else:
                    print("  Second loop iteration")
                end
            done
        else:
            print("y is not greater than 1")
        end
    else:
        print("x is not positive")
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
        expected = """x is positive
y is greater than 1
Loop iteration: 0
  First loop iteration
Loop iteration: 1
  Second loop iteration"""
        assert output == expected
    finally:
        sys.stdout = old_stdout
