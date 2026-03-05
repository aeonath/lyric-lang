# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for escape sequence handling in regex string literals."""

import pytest
import io
import sys
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.lexer import tokenize


def test_escaped_forward_slash_in_regex():
    """Verify that escaped forward slashes work in regex patterns."""
    source = '''
def main() {
    # Pattern with escaped forward slash
    rex pattern = regex("/<title>(.*?)<\\/title>/")
    
    # Test matching
    var html = "<title>Hello World</title>"
    var match = pattern.search(html)
    
    if match:
        print("Match found")
        print(match.group(1))
    end
}
'''
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should find match and extract "Hello World"
        output = captured_output.getvalue().strip()
        assert "Match found" in output
        assert "Hello World" in output
    finally:
        sys.stdout = old_stdout


def test_digit_escape_in_regex():
    """Verify that \\d works correctly in regex patterns."""
    source = '''
def main() {
    rex pattern = regex("/\\d+/")
    var text = "Phone: 555-1234"
    var match = pattern.search(text)
    
    if match:
        print("Digits found: " + match.group(0))
    end
}
'''
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should find "555" (first sequence of digits)
        output = captured_output.getvalue().strip()
        assert "Digits found:" in output
    finally:
        sys.stdout = old_stdout


def test_escaped_slash_at_end_of_pattern():
    """Verify that \\/ works at the end of a regex pattern."""
    source = '''
def main() {
    rex pattern = regex("/foo\\//")
    var text1 = "foo/"
    var text2 = "foo"
    
    var match1 = pattern.search(text1)
    var match2 = pattern.search(text2)
    
    if match1:
        print("Match1 found")
    end
    
    if match2:
        print("Match2 found")
    end
}
'''
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should match text1 but not text2
        output = captured_output.getvalue().strip()
        assert "Match1 found" in output
        assert "Match2 found" not in output
    finally:
        sys.stdout = old_stdout


def test_word_and_space_escapes_in_regex():
    """Verify that \\w+\\s\\w+ works correctly."""
    source = '''
def main() {
    rex pattern = regex("/\\w+\\s\\w+/")
    var text = "Hello World"
    var match = pattern.search(text)
    
    if match:
        print("Match: " + match.group(0))
    end
}
'''
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should match "Hello World"
        output = captured_output.getvalue().strip()
        assert "Match:" in output
    finally:
        sys.stdout = old_stdout


def test_double_backslash_in_string():
    """Verify that \\\\ is handled correctly (literal backslash)."""
    source = '''
def main() {
    rex pattern = regex("/\\\\d+/")
    var text = "123"
    var match = pattern.search(text)
    
    if match:
        print("Backslash match found")
    end
}
'''
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        # This should work - pattern should be "\\d+" which means "\d+"
        output = captured_output.getvalue().strip()
        # Should match
        assert "Backslash match found" in output
    finally:
        sys.stdout = old_stdout


def test_newline_escape_in_string():
    """Verify that \\n is handled correctly in string literals."""
    source = '''
def main() {
    var text = "Line 1\\nLine 2"
    # Just verify we can create the string and print it
    print(text)
}
'''
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should print the string (newline will be printed)
        output = captured_output.getvalue()
        assert "Line 1" in output
        assert "Line 2" in output
    finally:
        sys.stdout = old_stdout


def test_tab_escape_in_string():
    """Verify that \\t is handled correctly in string literals."""
    source = '''
def main() {
    var text = "Column1\\tColumn2"
    # Just verify we can create the string and print it
    print(text)
}
'''
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        # Should work - the string contains an actual tab character
        output = captured_output.getvalue()
        assert "Column1" in output
        assert "Column2" in output
    finally:
        sys.stdout = old_stdout


def test_quote_escape_in_string():
    """Verify that \\" is handled correctly in string literals."""
    source = '''
def main() {
    var text = "Say \\"Hello\\" to me"
    print(text)
}
'''
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should print the string with embedded quotes
        output = captured_output.getvalue().strip()
        assert "Say" in output and "Hello" in output
    finally:
        sys.stdout = old_stdout


def test_string_tokenization_with_escapes():
    """Verify that escaped sequences are correctly tokenized."""
    source = 'var text = "Line 1\\nLine 2\\tTabbed"'
    
    tokens = tokenize(source)
    
    # Find the STRING token
    string_token = None
    for token in tokens:
        if token.type == 'STRING':
            string_token = token
            break
    
    assert string_token is not None
    assert 'Line 1' in string_token.value
    assert 'Line 2' in string_token.value
    # The value should contain actual newline and tab characters
    assert '\n' in string_token.value
    assert '\t' in string_token.value


def test_regex_with_capture_groups_and_escapes():
    """Verify regex with capture groups and escaped characters."""
    source = '''
def main() {
    rex pattern = regex("/<div class=\\"content\\">(.*?)<\\/div>/")
    var html = "<div class=\\"content\\">Hello World</div>"
    var match = pattern.search(html)
    
    if match:
        print("Content: " + match.group(1))
    end
}
'''
    
    ast = parse(source)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Should extract "Hello World"
        output = captured_output.getvalue().strip()
        assert "Content:" in output
        assert "Hello World" in output
    finally:
        sys.stdout = old_stdout
