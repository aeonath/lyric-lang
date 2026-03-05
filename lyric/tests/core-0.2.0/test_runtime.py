# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for Lyric runtime built-in functions.
"""

import pytest
import tempfile
import os
from lyric.runtime import (
    print_builtin, input_builtin, int_builtin, flt_builtin, str_builtin,
    range_builtin, open_builtin, register_builtins
)


class TestRuntimeBuiltins:
    """Test cases for runtime built-in functions."""
    
    def test_print_builtin_no_args(self, capsys):
        """Test print built-in with no arguments."""
        print_builtin()
        captured = capsys.readouterr()
        assert captured.out == "\n"
    
    def test_print_builtin_single_arg(self, capsys):
        """Test print built-in with single argument."""
        print_builtin("Hello")
        captured = capsys.readouterr()
        assert captured.out == "Hello\n"
    
    def test_print_builtin_multiple_args(self, capsys):
        """Test print built-in with multiple arguments."""
        print_builtin("Hello", "World", 42)
        captured = capsys.readouterr()
        assert captured.out == "Hello World 42\n"
    
    def test_print_builtin_mixed_types(self, capsys):
        """Test print built-in with mixed types."""
        print_builtin("Number:", 42, "Float:", 3.14)
        captured = capsys.readouterr()
        assert captured.out == "Number: 42 Float: 3.14\n"
    
    def test_int_builtin(self):
        """Test int built-in function."""
        assert int_builtin("42") == 42
        assert int_builtin(3.14) == 3
        assert int_builtin(True) == 1
        assert int_builtin(False) == 0
    
    def test_flt_builtin(self):
        """Test flt built-in function."""
        assert flt_builtin("3.14") == 3.14
        assert flt_builtin(42) == 42.0
        assert flt_builtin(True) == 1.0
        assert flt_builtin(False) == 0.0
    
    def test_str_builtin(self):
        """Test str built-in function."""
        assert str_builtin(42) == "42"
        assert str_builtin(3.14) == "3.14"
        assert str_builtin(True) == "True"
        assert str_builtin(False) == "False"
        assert str_builtin("hello") == "hello"
    
    def test_range_builtin(self):
        """Test range built-in function."""
        result = list(range_builtin(5))
        assert result == [0, 1, 2, 3, 4]
        
        result = list(range_builtin(0))
        assert result == []
        
        result = list(range_builtin(1))
        assert result == [0]
    
    def test_len_method_on_objects(self):
        """Test that len() is now a method on arr and map objects, not a standalone function."""
        # This test documents that len() has been migrated to a method-based API
        # len([1,2,3]) -> [1,2,3].len()
        # len({"a": 1}) -> {"a": 1}.len()
        from lyric.interpreter import ArrObject, MapObject
        
        arr = ArrObject([1, 2, 3])
        assert arr.len() == 3
        
        map_obj = MapObject({"a": 1, "b": 2})
        assert map_obj.len() == 2
    
    def test_open_builtin(self):
        """Test open built-in function."""
        # Create a temporary file with test content
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp.write("line1\nline2\nline3\n")
            tmp_path = tmp.name
        
        try:
            # Test reading lines
            lines = list(open_builtin(tmp_path))
            assert lines == ["line1", "line2", "line3"]
            
            # Test with empty file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as empty_tmp:
                empty_path = empty_tmp.name
            
            lines = list(open_builtin(empty_path))
            assert lines == []
            
            # Clean up empty file
            os.unlink(empty_path)
            
        finally:
            # Clean up test file
            os.unlink(tmp_path)
    
    def test_register_builtins(self):
        """Test register_builtins function."""
        env = {}
        register_builtins(env)
        
        # Check that all current built-ins are registered
        # Note: len, append, keys, values are now methods on objects, not standalone functions
        assert 'print' in env
        assert 'input' in env
        assert 'int' in env
        assert 'flt' in env
        assert 'str' in env
        assert 'arr' in env
        assert 'map' in env
        assert 'range' in env
        assert 'open' in env
        assert 'isinstance' in env
        assert 'type' in env
        assert 'regex' in env
        
        # Check that deprecated functions are NOT registered
        assert 'len' not in env
        assert 'append' not in env
        assert 'keys' not in env
        assert 'values' not in env
        
        # Check that registered functions are callable
        assert callable(env['print'])
        assert callable(env['input'])
        assert callable(env['int'])
        assert callable(env['flt'])
        assert callable(env['str'])
        assert callable(env['range'])
        assert callable(env['open'])
    
    def test_builtins_integration(self, capsys):
        """Test built-ins working together."""
        env = {}
        register_builtins(env)
        
        # Test print with converted values
        env['print']("Number:", env['int']("42"), "Float:", env['flt']("3.14"))
        captured = capsys.readouterr()
        assert captured.out == "Number: 42 Float: 3.14\n"
        
        # Test range and arr (list) creation
        from lyric.interpreter import ArrObject
        numbers = env['arr'](list(env['range'](5)))
        env['print']("Length:", numbers.len())
        captured = capsys.readouterr()
        assert captured.out == "Length: 5\n"
        
        # Test string conversion
        env['print']("String:", env['str'](42))
        captured = capsys.readouterr()
        assert captured.out == "String: 42\n"
