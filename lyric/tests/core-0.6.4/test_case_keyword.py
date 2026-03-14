# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for the 'case' keyword as syntactic sugar for 'elif'."""

import pytest
import io
import sys
from lyric.lexer import tokenize
from lyric.parser import parse
from lyric.interpreter import evaluate


def test_case_tokenizes_as_elif():
    """Verify that 'case' tokenizes as an 'ELIF' token."""
    source = "if x > 5:\n    print(\"high\")\ncase x > 3:\n    print(\"medium\")\nelse:\n    print(\"low\")\nend"
    
    tokens = tokenize(source)
    
    # Find the 'case' token and verify it's an ELIF token
    case_token = None
    for token in tokens:
        if token.value == 'case':
            case_token = token
            break
    
    assert case_token is not None, "Expected to find 'case' token"
    assert case_token.type == 'ELIF', f"Expected 'case' to tokenize as 'ELIF', got '{case_token.type}'"


def test_case_parses_correctly():
    """Verify that 'case' parses correctly in if statements."""
    source = """
def main() {
    var x = 4
    if x > 5:
        print("high")
    case x > 3:
        print("medium")
    else:
        print("low")
    end
}
"""
    
    # Should parse without error
    ast = parse(source)
    assert ast is not None
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should print "medium" since x=4 is > 3 but not > 5
        output = captured_output.getvalue().strip()
        assert "medium" in output
        assert "high" not in output
        assert "low" not in output
    finally:
        sys.stdout = old_stdout


def test_case_executes_correctly():
    """Verify that 'case' executes with the same logic flow as 'elif'."""
    source = """
def main() {
    var x = 7
    if x > 10:
        print("high")
    case x > 5:
        print("medium")
    else:
        print("low")
    end
}
"""
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should print "medium" since x=7 is > 5 but not > 10
        output = captured_output.getvalue().strip()
        assert "medium" in output
    finally:
        sys.stdout = old_stdout


def test_mixed_elif_and_case():
    """Verify that mixing 'elif' and 'case' works correctly."""
    source = """
def main() {
    var x = 4
    if x > 10:
        print("high")
    elif x > 5:
        print("medium-high")
    case x > 3:
        print("medium")
    else:
        print("low")
    end
}
"""
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should print "medium" since x=4 is > 3 but not > 5 or > 10
        output = captured_output.getvalue().strip()
        assert "medium" in output
        assert "high" not in output
        assert "medium-high" not in output
        assert "low" not in output
    finally:
        sys.stdout = old_stdout


def test_multiple_case_statements():
    """Verify multiple 'case' statements work correctly."""
    source = """
def main() {
    var x = 2
    if x > 5:
        print("high")
    case x > 3:
        print("medium")
    case x > 1:
        print("low-medium")
    else:
        print("low")
    end
}
"""
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should print "low-medium" since x=2 is > 1 but not > 3 or > 5
        output = captured_output.getvalue().strip()
        assert output == "low-medium"
        assert "high" not in output
    finally:
        sys.stdout = old_stdout


def test_case_with_else():
    """Verify that 'case' works with 'else' clause."""
    source = """
def main() {
    var x = 1
    if x > 5:
        print("high")
    case x > 3:
        print("medium")
    else:
        print("low")
    end
}
"""
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should print "low" since none of the conditions are met
        output = captured_output.getvalue().strip()
        assert "low" in output
        assert "high" not in output
        assert "medium" not in output
    finally:
        sys.stdout = old_stdout


def test_case_without_else():
    """Verify that 'case' works without 'else' clause."""
    source = """
def main() {
    var x = 4
    if x > 5:
        print("high")
    case x > 3:
        print("medium")
    end
}
"""
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should print "medium" since x=4 > 3
        output = captured_output.getvalue().strip()
        assert "medium" in output
        assert "high" not in output
    finally:
        sys.stdout = old_stdout


def test_case_only_no_if():
    """Verify that 'case' requires an 'if' statement first."""
    source = """
def main() {
    var x = 4
    case x > 3:  # Should cause parse error - case must follow if
        print("medium")
    end
}
"""
    
    # This should raise a parse error since 'case' must follow 'if'
    with pytest.raises(Exception):  # Should raise ParseError
        ast = parse(source)


def test_case_token_position():
    """Verify that 'case' token has correct position information."""
    source = "def main() {\n    if x > 5:\n        print(\"high\")\n    case x > 3:\n        print(\"medium\")\n    end\n}"
    
    tokens = tokenize(source)
    
    # Find the 'case' token
    case_token = None
    for token in tokens:
        if token.value == 'case':
            case_token = token
            break
    
    assert case_token is not None
    assert case_token.line == 4  # Should be on line 4 (1-based)
    assert case_token.type == 'ELIF'
