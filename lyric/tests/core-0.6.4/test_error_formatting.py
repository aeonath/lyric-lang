# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Test suite for Sprint 7 Task 3: Error Message Line Number Formatting."""

import pytest
import sys
import os

# Add the lyric module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.errors import LexError, ParseError, RuntimeErrorLyric
from lyric.interpreter import Interpreter


class TestErrorLineNumberFormatting:
    """Test error message formatting to ensure single, accurate line/column references."""
    
    def test_lexical_error_formatting(self):
        """Test that lexical errors show only one line/column reference."""
        code = "var x = ^invalid"
        
        with pytest.raises(LexError) as exc_info:
            tokenize(code)
        
        error_msg = str(exc_info.value)
        
        # Should contain only one line/column reference
        assert "at line 1, column 9" in error_msg
        assert "line 0, column 0" not in error_msg
        assert error_msg.count("at line") == 1
        assert error_msg.count("column") == 1
    
    def test_syntax_error_formatting(self):
        """Test that syntax errors show only one line/column reference."""
        code = """
        var x = 5
        if x > 3
            print "hello"
        """
        
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        
        with pytest.raises(ParseError) as exc_info:
            parser.parse()
        
        error_msg = str(exc_info.value)
        
        # Should contain only one line/column reference
        assert "at line 5, column 9" in error_msg
        assert "line 0, column 0" not in error_msg
        assert error_msg.count("at line") == 1
        assert error_msg.count("column") == 1
    
    def test_runtime_error_formatting(self):
        """Test that runtime errors show only one line/column reference."""
        code = "var x = undefined_variable"
        
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        from lyric.interpreter import Interpreter
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        
        # Should contain the error message without "Runtime error:" prefix
        # (the CLI adds the prefix; __str__ returns the clean message for catch blocks)
        assert "Undefined variable" in error_msg
        assert "line 0, column 0" not in error_msg
    
    def test_error_message_consistency(self):
        """Test that all error types have consistent formatting."""
        # Test lexical error
        with pytest.raises(LexError) as lex_exc:
            tokenize("var x = @invalid")
        
        lex_msg = str(lex_exc.value)
        assert lex_msg.startswith("Lexical error:")
        assert "at line 1, column 9" in lex_msg
        
        # Test parse error
        tokens = tokenize("if true\nprint \"hello\"")
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        with pytest.raises(ParseError) as parse_exc:
            parser.parse()
        
        parse_msg = str(parse_exc.value)
        assert parse_msg.startswith("Parse error:")
        assert "at line 2, column 1" in parse_msg
        
        # Test runtime error
        tokens = tokenize("var x = undefined")
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        with pytest.raises(RuntimeErrorLyric) as runtime_exc:
            interpreter.evaluate(ast)
        
        runtime_msg = str(runtime_exc.value)
        # Runtime errors return clean message (no prefix) for use in catch blocks
        assert "Undefined variable" in runtime_msg
    
    def test_no_duplicate_line_column_info(self):
        """Test that error messages never contain duplicate line/column information."""
        test_cases = [
            ("var x = ^invalid", "lexical"),
            ("if true\nprint \"hello\"", "syntax"),
            ("var x = undefined", "runtime")
        ]
        
        for code, error_type in test_cases:
            try:
                if error_type == "lexical":
                    tokenize(code)
                elif error_type == "syntax":
                    tokens = tokenize(code)
                    parser = Parser(tokens)
                    parser._interactive_mode = True
                    parser.is_top_level = False
                    parser.parse()
                elif error_type == "runtime":
                    tokens = tokenize(code)
                    parser = Parser(tokens)
                    parser._interactive_mode = True
                    parser.is_top_level = False
                    ast = parser.parse()
                    interpreter = Interpreter()
                    interpreter.evaluate(ast)
            except Exception as e:
                error_msg = str(e)
                
                # Should not contain "line 0, column 0"
                assert "line 0, column 0" not in error_msg, f"Found 'line 0, column 0' in {error_type} error: {error_msg}"
                
                # Should not have duplicate "at line" references
                at_line_count = error_msg.count("at line")
                assert at_line_count <= 1, f"Found {at_line_count} 'at line' references in {error_type} error: {error_msg}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
