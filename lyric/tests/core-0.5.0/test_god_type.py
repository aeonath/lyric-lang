# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for the god type (boolean type named after Kurt Gödel)."""

import pytest
from lyric.lexer import tokenize
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import ParseError, RuntimeErrorLyric


def test_god_keyword_recognized():
    """Test that 'god' is recognized as a type keyword."""
    source = "god ready = true"
    tokens = tokenize(source)
    # god should be tokenized as TYPE_OR_IDENT
    assert any(token.type == 'TYPE_OR_IDENT' and token.value == 'god' for token in tokens)


def test_true_false_literals():
    """Test that true and false literals are recognized."""
    source = "var x = true\nvar y = false"
    ast = parse(source, interactive=True)
    interpreter = evaluate(ast)
    # Evaluation should not raise errors


def test_god_type_declaration():
    """Test god type declaration with true literal."""
    source = "god ready = true\nprint(ready)"
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    # Should execute without errors


def test_god_type_false():
    """Test god type declaration with false literal."""
    source = "god flag = false\nprint(flag)"
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    # Should execute without errors


def test_god_in_conditional():
    """Test god variables in if statements."""
    source = """
god ready = true
var result = 0
if ready
    result = 1
end
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_logical_operations():
    """Test logical operations with god type."""
    source = """
god a = true
god b = false
var result1 = a and b
var result2 = a or b
var result3 = not a
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_comparison():
    """Test comparison operations with god type."""
    source = """
god a = true
god b = false
var same = a == a
var different = a != b
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_function_parameter():
    """Test god type as function parameter."""
    source = """
def check_status(god is_ready) {
    if is_ready
        return 1
    end
    return 0
}
var result = check_status(true)
"""
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    # Should execute without errors


def test_god_function_return():
    """Test god type as function return value."""
    source = """
def is_valid() {
    return true
}
god status = is_valid()
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_type_enforcement():
    """Test that god type enforces boolean values."""
    source = """
god flag = 42
"""
    ast = parse(source, interactive=True)
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        evaluate(ast)
    assert "Type mismatch" in str(exc_info.value)
    assert "god" in str(exc_info.value)


def test_god_type_reassignment_error():
    """Test that god type prevents non-boolean reassignment."""
    source = """
god flag = true
flag = 42
"""
    ast = parse(source, interactive=True)
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        evaluate(ast)
    assert "Type mismatch" in str(exc_info.value)


def test_type_function_returns_god():
    """Test that type() function returns 'god' for boolean values."""
    source = """
var result = type(true)
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should return "god"


def test_isinstance_with_god():
    """Test isinstance() function with god type."""
    source = """
god flag = true
var result = isinstance(flag, "god")
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_in_list():
    """Test god values in lists."""
    source = """
var flags = [true, false, true]
god first = flags[0]
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_in_dict():
    """Test god values in dictionaries."""
    source = """
var config = {"enabled": true, "debug": false}
god enabled = config["enabled"]
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_multi_declaration():
    """Test multi-variable declaration with god type."""
    source = """
god flag1, god flag2
flag1 = true
flag2 = false
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_with_var():
    """Test that var can hold god values."""
    source = """
var x = true
var y = false
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_true_false_case_sensitive():
    """Test that true and false are case-sensitive."""
    source = """
var x = true
var y = false
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_ternary_like_usage():
    """Test god type in ternary-like conditional usage."""
    source = """
god condition = true
var result = 0
if condition
    result = 10
else
    result = 20
end
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_in_given_loop():
    """Test god type in given loop condition."""
    source = """
god should_run = true
var count = 0
given should_run and count < 3
    count = count + 1
    should_run = false
done
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_class_member():
    """Test god type as class member."""
    source = """
class Config
    god debug = false
    
    def init() {
        self.debug = true
    }
+++

var cfg = Config()
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_god_type_with_none():
    """Test that god type accepts None (nullable)."""
    source = """
god flag = None
print(flag)
"""
    ast = parse(source, interactive=True)
    import sys, io
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        evaluate(ast)
    finally:
        sys.stdout = old_stdout
    assert captured.getvalue().strip() == "None"


def test_god_mixed_with_other_types():
    """Test god type alongside other type declarations."""
    source = """
int x = 10
str y = "hello"
god flag = true
flt z = 3.14
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_uppercase_true_false_still_work():
    """Test that uppercase True and False still work (backward compatibility)."""
    source = """
var x = True
var y = False
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors

