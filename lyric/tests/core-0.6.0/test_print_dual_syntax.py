# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Test suite for Sprint 6 Pivot 6.8.1: Print Dual Syntax Support."""

import pytest
import sys
import os

# Add the lyric module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.ast_nodes import CallNode, LiteralNode, BinaryOpNode, IdentifierNode


class TestPrintDualSyntax:
    """Test both print(<expr>) and print <expr> syntax forms."""
    
    def test_print_function_form_single_arg(self):
        """Test print("Hello") syntax."""
        code = 'print("Hello")'
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Should create a CallNode with single argument
        assert len(ast.statements) == 1
        call_node = ast.statements[0]
        assert isinstance(call_node, CallNode)
        assert call_node.func_name == 'print'
        assert len(call_node.args) == 1
        assert isinstance(call_node.args[0], LiteralNode)
        assert call_node.args[0].value == "Hello"
    
    def test_print_bare_form_single_arg(self):
        """Test print "Hello" syntax."""
        code = 'print "Hello"'
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Should create a CallNode with single argument (same as function form)
        assert len(ast.statements) == 1
        call_node = ast.statements[0]
        assert isinstance(call_node, CallNode)
        assert call_node.func_name == 'print'
        assert len(call_node.args) == 1
        assert isinstance(call_node.args[0], LiteralNode)
        assert call_node.args[0].value == "Hello"
    
    def test_print_function_form_multi_arg(self):
        """Test print("a", "b") syntax."""
        code = 'print("a", "b")'
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Should create a CallNode with multiple arguments
        assert len(ast.statements) == 1
        call_node = ast.statements[0]
        assert isinstance(call_node, CallNode)
        assert call_node.func_name == 'print'
        assert len(call_node.args) == 2
        assert isinstance(call_node.args[0], LiteralNode)
        assert call_node.args[0].value == "a"
        assert isinstance(call_node.args[1], LiteralNode)
        assert call_node.args[1].value == "b"
    
    def test_print_bare_form_multi_arg(self):
        """Test print "a", "b" syntax."""
        code = 'print "a", "b"'
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Should create a CallNode with multiple arguments (same as function form)
        assert len(ast.statements) == 1
        call_node = ast.statements[0]
        assert isinstance(call_node, CallNode)
        assert call_node.func_name == 'print'
        assert len(call_node.args) == 2
        assert isinstance(call_node.args[0], LiteralNode)
        assert call_node.args[0].value == "a"
        assert isinstance(call_node.args[1], LiteralNode)
        assert call_node.args[1].value == "b"
    
    def test_print_with_expressions(self):
        """Test print with complex expressions."""
        code = 'print "Hello " + name'
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        
        # Should create a CallNode with binary expression
        assert len(ast.statements) == 1
        call_node = ast.statements[0]
        assert isinstance(call_node, CallNode)
        assert call_node.func_name == 'print'
        assert len(call_node.args) == 1
        assert isinstance(call_node.args[0], BinaryOpNode)
        assert call_node.args[0].op == '+'
    
    def test_print_function_vs_bare_equivalence(self):
        """Test that both forms produce identical AST."""
        code1 = 'print("Hello")'
        code2 = 'print "Hello"'
        
        tokens1 = tokenize(code1)
        parser1 = Parser(tokens1)
        parser1._interactive_mode = True
        parser1.is_top_level = False
        ast1 = parser1.parse()
        
        tokens2 = tokenize(code2)
        parser2 = Parser(tokens2)
        parser2._interactive_mode = True
        parser2.is_top_level = False
        ast2 = parser2.parse()
        
        # Both should produce identical CallNode structures
        call1 = ast1.statements[0]
        call2 = ast2.statements[0]
        
        assert isinstance(call1, CallNode)
        assert isinstance(call2, CallNode)
        assert call1.func_name == call2.func_name
        assert len(call1.args) == len(call2.args)
        assert isinstance(call1.args[0], LiteralNode)
        assert isinstance(call2.args[0], LiteralNode)
        assert call1.args[0].value == call2.args[0].value
    
    def test_print_multi_arg_equivalence(self):
        """Test that multi-argument forms produce identical AST."""
        code1 = 'print("a", "b", "c")'
        code2 = 'print "a", "b", "c"'
        
        tokens1 = tokenize(code1)
        parser1 = Parser(tokens1)
        parser1._interactive_mode = True
        parser1.is_top_level = False
        ast1 = parser1.parse()
        
        tokens2 = tokenize(code2)
        parser2 = Parser(tokens2)
        parser2._interactive_mode = True
        parser2.is_top_level = False
        ast2 = parser2.parse()
        
        # Both should produce identical CallNode structures
        call1 = ast1.statements[0]
        call2 = ast2.statements[0]
        
        assert isinstance(call1, CallNode)
        assert isinstance(call2, CallNode)
        assert call1.func_name == call2.func_name
        assert len(call1.args) == len(call2.args) == 3
        
        for i in range(3):
            assert isinstance(call1.args[i], LiteralNode)
            assert isinstance(call2.args[i], LiteralNode)
            assert call1.args[i].value == call2.args[i].value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
