# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for built-in functions integration with interpreter.
"""

import pytest
from lyric.parser import parse
from lyric.interpreter import evaluate


class TestBuiltinsIntegration:
    """Test cases for built-in functions integration."""
    
    def test_print_builtin_available(self):
        """Test that print built-in is available in interpreter."""
        ast = parse('def main() { print("Hello") }')
        interpreter = evaluate(ast)
        # If we get here without error, print is working
        assert True
    
    def test_int_builtin_available(self):
        """Test that int built-in is available in interpreter."""
        ast = parse('def main() { x = int("42") }')
        interpreter = evaluate(ast)
        # If we get here without error, int is working
        assert True
    
    def test_flt_builtin_available(self):
        """Test that flt built-in is available in interpreter."""
        ast = parse('def main() { x = flt("3.14") }')
        interpreter = evaluate(ast)
        # If we get here without error, flt is working
        assert True
    
    def test_str_builtin_available(self):
        """Test that str built-in is available in interpreter."""
        ast = parse('def main() { x = str(42) }')
        interpreter = evaluate(ast)
        # If we get here without error, str is working
        assert True
    
    def test_len_method_available(self):
        """Test that len() is now a method on arr and map objects."""
        # len() is no longer a standalone function - it's a method on arr and map objects
        code = '''
        def main() {
            x = [1, 2, 3]
            y = x.len()
        }'''
        ast = parse(code)
        interpreter = evaluate(ast)
        # If we get here without error, len() method is working
        assert True
    
    def test_range_builtin_available(self):
        """Test that range built-in is available in interpreter."""
        ast = parse('def main() { int i for i in range(3): print(i) done }')
        interpreter = evaluate(ast)
        # If we get here without error, range is working
        assert True
    
    def test_all_builtins_registered(self):
        """Test that all built-ins are registered in interpreter."""
        from lyric.interpreter import Interpreter
        interpreter = Interpreter()
        
        # Check that current built-ins are in global scope
        # Note: len, append, keys, values are now methods, not standalone functions
        assert 'print' in interpreter.global_scope
        assert 'input' in interpreter.global_scope
        assert 'int' in interpreter.global_scope
        assert 'flt' in interpreter.global_scope
        assert 'str' in interpreter.global_scope
        assert 'arr' in interpreter.global_scope
        assert 'map' in interpreter.global_scope
        assert 'range' in interpreter.global_scope
        assert 'open' in interpreter.global_scope
        assert 'isinstance' in interpreter.global_scope
        assert 'type' in interpreter.global_scope
        assert 'regex' in interpreter.global_scope
        
        # Check that deprecated functions are NOT registered
        assert 'len' not in interpreter.global_scope
        assert 'append' not in interpreter.global_scope
        assert 'keys' not in interpreter.global_scope
        assert 'values' not in interpreter.global_scope
        
        # Check that registered functions are callable
        assert callable(interpreter.global_scope['print'])
        assert callable(interpreter.global_scope['input'])
        assert callable(interpreter.global_scope['int'])
        assert callable(interpreter.global_scope['flt'])
        assert callable(interpreter.global_scope['str'])
        assert callable(interpreter.global_scope['range'])
        assert callable(interpreter.global_scope['open'])
