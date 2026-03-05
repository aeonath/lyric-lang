#!/usr/bin/env python
"""
Tests to verify that 'else if' syntax is deprecated and raises ParseError.
"""
import pytest
from lyric.parser import Parser, parse as parse_source
from lyric.lexer import tokenize
from lyric.errors import ParseError


class TestElseIfDeprecated:
    """Test that 'else if' syntax is deprecated and raises ParseError."""
    
    def test_else_if_raises_parse_error(self):
        """Test that using 'else if' raises a ParseError with a clear message."""
        source = '''
def main() {
    x = 5
    if x > 10:
        print("high")
    else if x > 5:
        print("medium")
    end
}
'''
        tokens = tokenize(source)
        
        with pytest.raises(ParseError) as exc_info:
            parser = Parser(tokens)
            parser.parse()
        
        error_message = str(exc_info.value)
        assert "elif" in error_message.lower()
        assert "else if" in error_message.lower()
        assert "deprecated" in error_message or "removed" in error_message or "use" in error_message
    
    def test_elif_still_works(self):
        """Test that 'elif' syntax still works correctly."""
        source = '''
def main() {
    x = 5
    if x > 10:
        print("high")
    elif x > 5:
        print("medium")
    else:
        print("low")
    end
}
'''
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Verify AST was created successfully
        assert ast is not None
        func = ast.statements[0]
        
        # Find the if statement (second statement after x = 5)
        if_stmt = func.body_statements[1]
        
        # Verify elif was parsed correctly
        assert len(if_stmt.elifs) == 1
    
    def test_multiple_elif_works(self):
        """Test that multiple 'elif' clauses work correctly."""
        source = '''
def main() {
    x = 5
    if x > 10:
        print("high")
    elif x > 7:
        print("medium-high")
    elif x > 3:
        print("medium")
    else:
        print("low")
    end
}
'''
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Verify AST was created successfully
        assert ast is not None
        func = ast.statements[0]
        
        # Find the if statement (second statement after x = 5)
        if_stmt = func.body_statements[1]
        
        # Verify multiple elifs were parsed correctly
        assert len(if_stmt.elifs) == 2
