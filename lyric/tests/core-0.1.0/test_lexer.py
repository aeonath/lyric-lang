# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for lexer module."""

import pytest
from lyric.lexer import tokenize, Token, LexError


def test_basic_if_statement():
    """Test tokenizing a basic if statement."""
    source = """if x > 0:
print("positive")
end"""
    
    tokens = tokenize(source)
    
    # Expected sequence: IF, IDENT(x), GT, INT(0), COLON, NEWLINE, IDENT(print), LPAREN, STRING("positive"), RPAREN, NEWLINE, END, NEWLINE/EOF
    expected_types = [
        'IF', 'IDENT', 'GT', 'INT', 'COLON', 'NEWLINE',
        'IDENT', 'LPAREN', 'STRING', 'RPAREN', 'NEWLINE',
        'END', 'EOF'
    ]
    
    assert len(tokens) == len(expected_types)
    for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
        assert token.type == expected_type, f"Token {i}: expected {expected_type}, got {token.type}"
    
    # Check specific values
    assert tokens[0].value == 'if'
    assert tokens[1].value == 'x'
    assert tokens[2].value == '>'
    assert tokens[3].value == 0
    assert tokens[6].value == 'print'
    assert tokens[8].value == 'positive'


def test_class_with_terminator():
    """Test tokenizing class definition with +++ terminator."""
    source = "class Player +++"
    
    tokens = tokenize(source)
    
    expected_types = ['CLASS', 'IDENT', 'CLASS_END', 'EOF']
    assert len(tokens) == len(expected_types)
    
    for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
        assert token.type == expected_type, f"Token {i}: expected {expected_type}, got {token.type}"
    
    # Check specific values
    assert tokens[0].value == 'class'
    assert tokens[1].value == 'Player'
    assert tokens[2].value == '+++'


def test_class_with_methods_and_terminator():
    """Test tokenizing class with methods and +++ terminator."""
    source = """class Calculator
def add(x, y):
return x + y
+++"""
    
    tokens = tokenize(source)
    
    # Should contain class, method definition, and terminator
    token_types = [token.type for token in tokens]
    assert 'CLASS' in token_types
    assert 'DEF' in token_types
    assert 'CLASS_END' in token_types
    
    # Find the class end token
    class_end_token = next(token for token in tokens if token.type == 'CLASS_END')
    assert class_end_token.value == '+++'


def test_multiple_classes_with_terminators():
    """Test tokenizing multiple classes with +++ terminators."""
    source = """class A +++
class B +++"""
    
    tokens = tokenize(source)
    
    # Should have two CLASS_END tokens
    class_end_tokens = [token for token in tokens if token.type == 'CLASS_END']
    assert len(class_end_tokens) == 2
    
    for token in class_end_tokens:
        assert token.value == '+++'


def test_else_if_tokens():
    """Test that 'else if' is tokenized as separate ELSE and IF tokens (deprecated but still tokenizes correctly)."""
    source = "else if x > 0:"
    
    tokens = tokenize(source)
    
    expected_types = ['ELSE', 'IF', 'IDENT', 'GT', 'INT', 'COLON', 'EOF']
    assert len(tokens) == len(expected_types)
    
    for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
        assert token.type == expected_type, f"Token {i}: expected {expected_type}, got {token.type}"
    
    assert tokens[0].value == 'else'
    assert tokens[1].value == 'if'


def test_comments_ignored():
    """Test that comments are properly ignored."""
    source = """# This is a comment
def main() {
print("hello")  # Another comment
}"""
    
    tokens = tokenize(source)
    
    # Should not contain any comment tokens
    token_types = [token.type for token in tokens]
    assert '#' not in token_types
    
    # Should contain the actual code tokens
    expected_types = ['NEWLINE', 'DEF', 'IDENT', '(', ')', '{', 'NEWLINE', 'IDENT', '(', 'STRING', ')', 'NEWLINE', '}', 'EOF']
    assert len(tokens) == len(expected_types)


def test_numbers_integers_and_floats():
    """Test tokenizing integers and floats."""
    source = "x = 42 y = 3.14"
    
    tokens = tokenize(source)
    
    # Find the number tokens
    int_token = next(token for token in tokens if token.type == 'INT')
    float_token = next(token for token in tokens if token.type == 'FLOAT')
    
    assert int_token.value == 42
    assert float_token.value == 3.14


def test_string_literals():
    """Test tokenizing string literals."""
    source = 'name = "Hello, World!"'
    
    tokens = tokenize(source)
    
    string_token = next(token for token in tokens if token.type == 'STRING')
    assert string_token.value == 'Hello, World!'


def test_line_and_column_numbers():
    """Test that tokens have correct line and column numbers."""
    source = """line1
line2 token"""
    
    tokens = tokenize(source)
    
    # Find the 'token' identifier
    token_token = next(token for token in tokens if token.value == 'token')
    assert token_token.line == 2
    assert token_token.col == 7  # 'line2 ' is 6 chars, so 'token' starts at col 7


def test_unterminated_string_error():
    """Test that unterminated strings raise LexError."""
    source = 'name = "unterminated string'
    
    with pytest.raises(LexError):
        tokenize(source)


def test_unexpected_character_error():
    """Test that unexpected characters raise LexError."""
    source = "x = @"
    
    with pytest.raises(LexError):
        tokenize(source)


def test_keywords():
    """Test that all keywords are properly recognized."""
    keywords = ['def', 'class', 'if', 'else', 'given', 'done', 'end', 'try', 'catch', 'finally', 'fade', 'raise']
    
    for keyword in keywords:
        tokens = tokenize(keyword)
        assert len(tokens) == 2  # keyword + EOF
        assert tokens[0].type == keyword.upper()
        assert tokens[0].value == keyword


def test_operators():
    """Test that operators are properly tokenized."""
    source = "x == y != z < w <= v > u >= t"
    
    tokens = tokenize(source)
    
    # Extract operator tokens
    operators = [token for token in tokens if token.type in ['==', '!=', 'LT', '<=', 'GT', '>=']]
    
    expected_operators = ['==', '!=', 'LT', '<=', 'GT', '>=']
    assert len(operators) == len(expected_operators)
    
    for i, op in enumerate(operators):
        assert op.type == expected_operators[i]