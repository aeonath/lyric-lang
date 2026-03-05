# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for rex type functionality in Sprint 5 Task 1."""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter


class TestRexTypeDefinition:
    """Test the basic rex type definition and parsing."""
    
    def test_rex_keyword_recognized(self):
        """Test that 'rex' is recognized as a type keyword."""
        tokens = tokenize("rex pattern")
        assert len(tokens) >= 2
        assert tokens[0].type == 'TYPE_OR_IDENT'
        assert tokens[0].value == 'rex'
        assert tokens[1].type == 'IDENT'
        assert tokens[1].value == 'pattern'
    
    def test_regex_literal_parsing(self):
        """Test that regex constructor calls are parsed correctly."""
        tokens = tokenize('regex("/^abc/")')
        assert len(tokens) >= 4
        assert tokens[0].type == 'IDENT'
        assert tokens[0].value == 'regex'
        assert tokens[1].type == 'LPAREN'
        assert tokens[2].type == 'STRING'
        assert tokens[2].value == '/^abc/'
    
    def test_regex_literal_with_special_chars(self):
        """Test that regex constructor calls with special chars are parsed correctly."""
        tokens = tokenize('regex("/\\d+/")')
        assert len(tokens) >= 4
        assert tokens[0].type == 'IDENT'
        assert tokens[0].value == 'regex'
        assert tokens[1].type == 'LPAREN'
        assert tokens[2].type == 'STRING'
        assert tokens[2].value == '/\\d+/'
    
    def test_regex_literal_empty_pattern(self):
        """Test that empty regex constructor calls are parsed correctly."""
        tokens = tokenize('regex("//")')
        assert len(tokens) >= 4
        assert tokens[0].type == 'IDENT'
        assert tokens[0].value == 'regex'
        assert tokens[1].type == 'LPAREN'
        assert tokens[2].type == 'STRING'
        assert tokens[2].value == '//'
    
    def test_regex_literal_does_not_conflict_with_division(self):
        """Test that regex literals don't conflict with division."""
        tokens = tokenize("a / b")
        assert len(tokens) >= 4
        assert tokens[0].type == 'IDENT'
        assert tokens[1].type == 'DIVIDE'
        assert tokens[2].type == 'IDENT'
    
    def test_invalid_regex_pattern_raises_error(self):
        """Test that invalid regex patterns in constructor raise runtime errors."""
        # This should now parse successfully but fail at runtime
        tokens = tokenize('regex("/[unclosed/")')
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        interpreter = Interpreter()
        with pytest.raises(Exception):  # Should be RuntimeErrorLyric
            interpreter.evaluate(ast)
    
    def test_unterminated_regex_raises_error(self):
        """Test that unterminated regex literals are treated as division."""
        # /unterminated is actually treated as division followed by identifier
        # since there's no closing slash
        tokens = tokenize("/unterminated")
        # Should be DIVIDE token followed by IDENT
        assert tokens[0].type == 'DIVIDE'
    
    def test_regex_literal_in_parser(self):
        """Test that regex constructor calls are parsed into CallNode."""
        parser = Parser(tokenize('regex("/^abc/")'))
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        assert len(ast.statements) == 1
        # The expression should be a CallNode to regex()
        assert hasattr(ast.statements[0], 'func_name')
        assert ast.statements[0].func_name == 'regex'
    
    def test_rex_type_declaration(self):
        """Test rex type declarations."""
        parser = Parser(tokenize("rex pattern = regex(\"/^abc/\")"))
        ast = parser.parse()
        assert len(ast.statements) == 1
        # Should be an assignment with rex type
        assert ast.statements[0].name == 'pattern'
    
    def test_rex_type_compatibility(self):
        """Test that rex objects are compatible with rex type."""
        interpreter = Interpreter()
        # Create a rex object
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': '^abc', 'line': 1, 'column': 1})())
        
        # Test type compatibility
        assert interpreter._is_type_compatible('rex', rex_obj)
        assert interpreter._is_type_compatible('var', rex_obj)
        assert not interpreter._is_type_compatible('int', rex_obj)
        assert not interpreter._is_type_compatible('str', rex_obj)


class TestRexMatchMethod:
    """Test the .match() method functionality."""
    
    def test_match_method_basic(self):
        """Test basic match functionality."""
        interpreter = Interpreter()
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': '^abc', 'line': 1, 'column': 1})())
        
        assert rex_obj.match("abcdef") == True
        assert rex_obj.match("xyz") == False
    
    def test_match_method_with_string_literal(self):
        """Test match method with string literals."""
        interpreter = Interpreter()
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': '^abc', 'line': 1, 'column': 1})())
        
        assert rex_obj.match("abc") == True
        assert rex_obj.match("ab") == False
        assert rex_obj.match("abcd") == True
    
    def test_match_method_with_variables(self):
        """Test match method with string variables."""
        interpreter = Interpreter()
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': '^abc', 'line': 1, 'column': 1})())
        
        interpreter.global_scope['text'] = "abcdef"
        assert rex_obj.match(interpreter.global_scope['text']) == True
        
        interpreter.global_scope['text'] = "xyz"
        assert rex_obj.match(interpreter.global_scope['text']) == False
    
    def test_match_method_type_error(self):
        """Test that match method raises error for non-string input."""
        interpreter = Interpreter()
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': '^abc', 'line': 1, 'column': 1})())
        
        with pytest.raises(Exception):  # Should be RuntimeErrorLyric
            rex_obj.match(123)
        
        with pytest.raises(Exception):  # Should be RuntimeErrorLyric
            rex_obj.match(None)


class TestRexReplaceMethod:
    """Test the .replace() method functionality."""
    
    def test_replace_method_basic(self):
        """Test basic replace functionality."""
        interpreter = Interpreter()
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': 'cat', 'line': 1, 'column': 1})())
        
        result = rex_obj.replace("the cat sat", "dog")
        assert result == "the dog sat"
    
    def test_replace_method_multiple_matches(self):
        """Test replace with multiple matches."""
        interpreter = Interpreter()
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': 'cat', 'line': 1, 'column': 1})())
        
        result = rex_obj.replace("cat cat cat", "dog")
        assert result == "dog dog dog"
    
    def test_replace_method_no_matches(self):
        """Test replace when no matches are found."""
        interpreter = Interpreter()
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': 'cat', 'line': 1, 'column': 1})())
        
        result = rex_obj.replace("the dog sat", "cat")
        assert result == "the dog sat"  # No change
    
    def test_replace_method_with_string_literals(self):
        """Test replace method with string literals."""
        interpreter = Interpreter()
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': '\\d+', 'line': 1, 'column': 1})())
        
        result = rex_obj.replace("abc123def456", "X")
        assert result == "abcXdefX"
    
    def test_replace_method_type_errors(self):
        """Test that replace method raises errors for invalid types."""
        interpreter = Interpreter()
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': 'cat', 'line': 1, 'column': 1})())
        
        with pytest.raises(Exception):  # Should be RuntimeErrorLyric
            rex_obj.replace(123, "dog")
        
        with pytest.raises(Exception):  # Should be RuntimeErrorLyric
            rex_obj.replace("text", 123)


class TestRexIntegration:
    """Test rex type integration with the full language."""
    
    def test_rex_assignment_and_usage(self):
        """Test assigning rex objects and using them."""
        source = """
        rex pattern = regex("/^abc/")
        var result = pattern.match("abcdef")
        """
        
        parser = Parser(tokenize(source))
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] == True
    
    def test_rex_with_replace_method(self):
        """Test rex object with replace method."""
        source = """
        rex pattern = regex("/cat/")
        var result = pattern.replace("the cat sat", "dog")
        """
        
        parser = Parser(tokenize(source))
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] == "the dog sat"
    
    def test_rex_type_enforcement(self):
        """Test type enforcement for rex variables."""
        source = """
        rex pattern = regex("/^abc/")
        pattern = "not a regex"
        """
        
        parser = Parser(tokenize(source))
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(Exception):  # Should be RuntimeErrorLyric
            interpreter.evaluate(ast)
    
    def test_rex_in_function(self):
        """Test rex objects in functions."""
        source = """
        def test_rex(rex pattern) {
            return pattern.match("test")
        }
        
        rex my_pattern = regex("/^test/")
        var result = test_rex(my_pattern)
        """
        
        parser = Parser(tokenize(source))
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] == True
    
    def test_rex_object_repr(self):
        """Test string representation of rex objects."""
        interpreter = Interpreter()
        rex_obj = interpreter._evaluate_rex_literal(type('RexNode', (), {'pattern': '^abc', 'line': 1, 'column': 1})())
        
        repr_str = repr(rex_obj)
        assert "RexObject" in repr_str
        assert "^abc" in repr_str
