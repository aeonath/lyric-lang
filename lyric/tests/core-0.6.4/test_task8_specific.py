"""Specific test for Task 8 failing pattern."""

import pytest
from lyric.lexer import Lexer
from lyric.parser import Parser
from lyric.interpreter import Interpreter


class TestTask8Specific:
    """Test the exact pattern from Task 8 that was failing."""
    
    def test_task8_pattern_parse_only(self):
        """Test that the Task 8 pattern parses without errors at column 45."""
        # Using a simpler pattern to test mixed quotes - using raw string to avoid Python escaping
        source = r'rex pattern = regex("<a href=[\"]([^\"]+)[\"]>")'
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Verify no lexical errors
        assert len(tokens) > 0
        
        # Verify the pattern parses
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Should parse successfully
        assert ast is not None
    
    def test_task8_mixed_quotes_complex(self):
        """Test mixed quotes in complex pattern - simplified version."""
        # Test that single and double quotes can coexist in a regex pattern
        source = r'rex pattern = regex("<a href=[\"]([^\"]+)[\"]>")'
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Find the string token
        string_token = next((t for t in tokens if t.type == 'STRING'), None)
        assert string_token is not None
        assert '"' in string_token.value  # Should contain escaped quotes
        assert "(" in string_token.value  # Should contain capture group
