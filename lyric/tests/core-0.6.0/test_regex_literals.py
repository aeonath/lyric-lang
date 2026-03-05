# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Test suite for Sprint 7 Task 1: Constructor-based Regex Syntax."""

import pytest
import sys
import os

# Add the lyric module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.ast_nodes import TypeDeclarationNode


class TestRegexConstructorSyntax:
    """Test constructor-based regex syntax support."""
    
    def test_basic_regex_constructor(self):
        """Test basic regex constructor declaration."""
        code = 'rex pattern = regex("/hello/")'
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Should create a type declaration with CallNode
        assert len(ast.statements) == 1
        decl_node = ast.statements[0]
        assert isinstance(decl_node, TypeDeclarationNode)
        assert decl_node.name == 'pattern'
        assert decl_node.type_name == 'rex'
        # The value should be a CallNode to regex()
        assert decl_node.expr.func_name == 'regex'
        assert len(decl_node.expr.args) == 1
        assert decl_node.expr.args[0].value == '/hello/'
    
    def test_complex_regex_constructor(self):
        """Test complex regex constructor with special characters."""
        code = 'rex email = regex("/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\\\.[a-zA-Z]{2,}$/")'
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Should create a type declaration with CallNode
        assert len(ast.statements) == 1
        decl_node = ast.statements[0]
        assert isinstance(decl_node, TypeDeclarationNode)
        assert decl_node.name == 'email'
        assert decl_node.type_name == 'rex'
        # The value should be a CallNode to regex()
        assert decl_node.expr.func_name == 'regex'
        assert len(decl_node.expr.args) == 1
        assert '/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/' in decl_node.expr.args[0].value
    
    def test_regex_with_groups(self):
        """Test regex constructor with capturing groups."""
        code = 'rex phone = regex("/(\\\\d{3})-(\\\\d{3})-(\\\\d{4})/")'
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Should create a type declaration with CallNode
        assert len(ast.statements) == 1
        decl_node = ast.statements[0]
        assert isinstance(decl_node, TypeDeclarationNode)
        assert decl_node.name == 'phone'
        assert decl_node.type_name == 'rex'
        # The value should be a CallNode to regex()
        assert decl_node.expr.func_name == 'regex'
        assert len(decl_node.expr.args) == 1
        assert '(\\d{3})-(\\d{3})-(\\d{4})' in decl_node.expr.args[0].value
    
    def test_regex_match_method(self):
        """Test regex match method."""
        code = '''
        rex pattern = regex("/hello/")
        var result = pattern.match("hello world")
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that result is True (match found)
        result = interpreter.global_scope['result']
        assert result == True
    
    def test_regex_search_method(self):
        """Test regex search method."""
        code = '''
        rex pattern = regex("/world/")
        var match = pattern.search("hello world")
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that match is not None
        match = interpreter.global_scope['match']
        assert match is not None
        assert hasattr(match, 'group')
    
    def test_regex_findall_method(self):
        """Test regex findall method."""
        code = '''
        rex pattern = regex("/\\d+/")
        var matches = pattern.findall("I have 5 apples and 10 oranges")
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that matches contains the numbers
        matches = interpreter.global_scope['matches']
        assert isinstance(matches, list)
        assert '5' in matches
        assert '10' in matches
    
    def test_regex_replace_method(self):
        """Test regex replace method."""
        code = '''
        rex pattern = regex("/\\d+/")
        var result = pattern.replace("I have 5 apples", "X")
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that result has numbers replaced
        result = interpreter.global_scope['result']
        assert result == "I have X apples"
    
    def test_regex_group_access(self):
        """Test accessing regex match groups."""
        code = '''
        rex phone = regex("/(\\d{3})-(\\d{3})-(\\d{4})/")
        var match = phone.search("Call 555-123-4567")
        var area_code = match.group(1)
        var exchange = match.group(2)
        var number = match.group(3)
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that groups are extracted correctly
        area_code = interpreter.global_scope['area_code']
        exchange = interpreter.global_scope['exchange']
        number = interpreter.global_scope['number']
        
        assert area_code == "555"
        assert exchange == "123"
        assert number == "4567"
    
    def test_invalid_regex_pattern(self):
        """Test that invalid regex patterns raise errors."""
        code = 'rex invalid = regex("/[unclosed/")'
        
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        interpreter = Interpreter()
        
        # Should raise RuntimeErrorLyric when evaluating
        with pytest.raises(Exception) as exc_info:
            interpreter.evaluate(ast)
        
        # Check that it's a regex compilation error
        assert "Invalid regex pattern" in str(exc_info.value)
    
    def test_regex_in_expression(self):
        """Test regex constructor in expressions."""
        code = '''
        rex pattern1 = regex("/hello/")
        rex pattern2 = regex("/world/")
        var text = "hello world"
        var match1 = pattern1.match(text)
        var match2 = pattern2.search(text)
        '''
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Check that both patterns work
        match1 = interpreter.global_scope['match1']
        match2 = interpreter.global_scope['match2']
        
        assert match1 == True
        assert match2 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])