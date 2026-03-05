"""Tests for mixed quote handling in regex string literals."""

import pytest
from lyric.lexer import Lexer
from lyric.parser import Parser
from lyric.interpreter import Interpreter


class TestMixedQuotes:
    """Test handling of mixed single and double quotes in regex patterns."""
    
    def test_single_quoted_string(self):
        """Test basic single-quoted string parsing."""
        source = "var text = 'Hello World'"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Verify the string token
        string_token = next((t for t in tokens if t.type == 'STRING'), None)
        assert string_token is not None
        assert string_token.value == "Hello World"
    
    def test_single_quote_inside_double_quoted_string(self):
        """Test single quotes inside double-quoted string."""
        source = 'var text = "This has a \' quote"'
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        string_token = next((t for t in tokens if t.type == 'STRING'), None)
        assert string_token is not None
        assert "This has a ' quote" in string_token.value
    
    def test_escaped_single_quote_in_double_quoted_string(self):
        """Test escaped single quote inside double-quoted string."""
        source = 'var text = "This has a \\\' quote"'
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        string_token = next((t for t in tokens if t.type == 'STRING'), None)
        assert string_token is not None
        assert "'" in string_token.value
    
    def test_double_quote_inside_single_quoted_string(self):
        """Test double quotes inside single-quoted string."""
        source = "var text = 'This has a \" quote'"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        string_token = next((t for t in tokens if t.type == 'STRING'), None)
        assert string_token is not None
        assert '"' in string_token.value
    
    def test_escaped_double_quote_in_single_quoted_string(self):
        """Test escaped double quote inside single-quoted string."""
        source = "var text = 'This has a \\\" quote'"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        string_token = next((t for t in tokens if t.type == 'STRING'), None)
        assert string_token is not None
        assert '"' in string_token.value
    
    def test_regex_simple_mixed_quotes(self):
        """Test simple regex pattern with mixed quotes."""
        source = r'rex pattern = regex("<a href=[\"]value[\"]>")'
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        # Should parse without error
        ast = parser.parse()
        assert ast is not None
    
    def test_regex_parse_with_single_quote_pattern(self):
        """Test regex pattern wrapped in single quotes with internal double quotes."""
        source = "rex pattern = regex('<a href=[\"]value[\"]>')"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        # Should parse without error
        ast = parser.parse()
        assert ast is not None
    
    def test_regex_execute_simple_match(self, capsys):
        """Test that regex pattern with mixed quotes executes and matches correctly."""
        source = r'''
rex href_pattern = regex("<a href=[\"]([^\"]+)[\"]>")
var html = '<a href="https://example.com">link</a>'
var match = href_pattern.search(html)
print match.group(1)
'''
        
        interpreter = Interpreter()
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        interpreter.evaluate(ast)
        
        # Should have matched the href value
        captured = capsys.readouterr()
        assert captured.out.strip() == "https://example.com"
    
    def test_nested_quotes_different_types(self):
        """Test that nested quotes of different types are preserved correctly."""
        source = r'var pattern = "outer \" inner ' + "' text" + r'"'
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        string_token = next((t for t in tokens if t.type == 'STRING'), None)
        assert string_token is not None
        assert 'outer' in string_token.value and 'text' in string_token.value
    
    def test_multiple_mixed_quotes(self):
        """Test pattern with multiple instances of mixed quotes."""
        source = r'var text = "text with \"quotes\" and ' + "'more' text" + r'"'
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Should parse without error
        assert len([t for t in tokens if t.type == 'STRING']) >= 1
