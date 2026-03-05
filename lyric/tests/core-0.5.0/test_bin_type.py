# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for the bin type (alias for god type)."""

import pytest
from lyric.lexer import tokenize
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import ParseError, RuntimeErrorLyric


def test_bin_keyword_recognized():
    """Test that 'bin' is recognized as a type keyword."""
    source = "bin ready = true"
    tokens = tokenize(source)
    # bin should be tokenized as TYPE_OR_IDENT
    assert any(token.type == 'TYPE_OR_IDENT' and token.value == 'bin' for token in tokens)


def test_bin_type_declaration():
    """Test bin type declaration with true literal."""
    source = "bin ready = true\nprint(ready)"
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    # Should execute without errors


def test_bin_type_false():
    """Test bin type declaration with false literal."""
    source = "bin flag = false\nprint(flag)"
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    # Should execute without errors


def test_bin_in_conditional():
    """Test bin variables in if statements."""
    source = """
bin ready = true
var result = 0
if ready
    result = 1
end
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_logical_operations():
    """Test logical operations with bin type."""
    source = """
bin a = true
bin b = false
var result1 = a and b
var result2 = a or b
var result3 = not a
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_comparison():
    """Test comparison operations with bin type."""
    source = """
bin a = true
bin b = false
var same = a == a
var different = a != b
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_function_parameter():
    """Test bin type as function parameter."""
    source = """
def check_status(bin is_ready) {
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


def test_bin_function_return():
    """Test bin type as function return value."""
    source = """
def is_valid() {
    return true
}
bin status = is_valid()
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_type_enforcement():
    """Test that bin type enforces boolean values."""
    source = """
bin flag = 42
"""
    ast = parse(source, interactive=True)
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        evaluate(ast)
    assert "Type mismatch" in str(exc_info.value)
    assert "bin" in str(exc_info.value)


def test_bin_type_reassignment_error():
    """Test that bin type prevents non-boolean reassignment."""
    source = """
bin flag = true
flag = 42
"""
    ast = parse(source, interactive=True)
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        evaluate(ast)
    assert "Type mismatch" in str(exc_info.value)


def test_isinstance_with_bin():
    """Test isinstance() function with bin type."""
    source = """
bin flag = true
var result = isinstance(flag, "bin")
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_in_list():
    """Test bin values in lists."""
    source = """
var flags = [true, false, true]
bin first = flags[0]
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_in_dict():
    """Test bin values in dictionaries."""
    source = """
var config = {"enabled": true, "debug": false}
bin enabled = config["enabled"]
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_multi_declaration():
    """Test multi-variable declaration with bin type."""
    source = """
bin flag1, bin flag2
flag1 = true
flag2 = false
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_with_var():
    """Test that var can hold bin values."""
    source = """
var x = true
var y = false
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_ternary_like_usage():
    """Test bin type in ternary-like conditional usage."""
    source = """
bin condition = true
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


def test_bin_in_given_loop():
    """Test bin type in given loop condition."""
    source = """
bin should_run = true
var count = 0
given should_run and count < 3
    count = count + 1
    should_run = false
done
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_class_member():
    """Test bin type as class member."""
    source = """
class Config
    bin debug = false
    
    def init() {
        self.debug = true
    }
+++

var cfg = Config()
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_type_with_none():
    """Test that bin type accepts None (nullable)."""
    source = """
bin flag = None
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


def test_bin_mixed_with_other_types():
    """Test bin type alongside other type declarations."""
    source = """
int x = 10
str y = "hello"
bin flag = true
flt z = 3.14
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_and_god_interchangeable():
    """Test that bin and god types are interchangeable."""
    source = """
god flag1 = true
bin flag2 = false
var same = flag1 == flag2
var both_true = flag1 and flag1
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_god_function_interchange():
    """Test that functions can accept both bin and god parameters."""
    source = """
def check(god flag1, bin flag2) {
    return flag1 and flag2
}
var result = check(true, false)
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_god_return_interchange():
    """Test that functions can return both bin and god types."""
    source = """
def get_god() {
    return true
}
def get_bin() {
    return false
}
bin result1 = get_god()
god result2 = get_bin()
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_god_multi_declaration():
    """Test multi-variable declaration mixing bin and god types."""
    source = """
god flag1, bin flag2
flag1 = true
flag2 = false
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_god_type_checking():
    """Test type checking with both bin and god types."""
    source = """
god flag1 = true
bin flag2 = false
var check1 = isinstance(flag1, "god")
var check2 = isinstance(flag2, "bin")
var check3 = isinstance(flag1, "bin")  # Should be false
var check4 = isinstance(flag2, "god")  # Should be false
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_god_class_members():
    """Test class with both bin and god members."""
    source = """
class Settings
    god enabled = true
    bin debug = false
    
    def init() {
        self.enabled = true
        self.debug = false
    }
+++

var settings = Settings()
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_god_comparison():
    """Test comparison between bin and god values."""
    source = """
god flag1 = true
bin flag2 = true
var same = flag1 == flag2
var different = flag1 != flag2
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors


def test_bin_god_logical_operations():
    """Test logical operations between bin and god values."""
    source = """
god flag1 = true
bin flag2 = false
var and_result = flag1 and flag2
var or_result = flag1 or flag2
var not_result1 = not flag1
var not_result2 = not flag2
"""
    ast = parse(source, interactive=True)
    evaluate(ast)
    # Should execute without errors
