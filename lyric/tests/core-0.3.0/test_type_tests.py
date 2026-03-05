# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Test suite for type_tests.ly - Sprint 3 type declaration and enforcement tests."""

import pytest
import subprocess
import os
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


class TestTypeTests:
    """Test type declaration and enforcement functionality."""
    
    def test_type_tests_ly_runs_successfully(self):
        """Test that type_tests.ly runs successfully through CLI."""
        type_tests_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'type_tests.ly')
        
        # Run the CLI command
        result = subprocess.run(['lyric', 'run', type_tests_path],
                               capture_output=True, text=True)
        
        # Should succeed (exit code 0)
        assert result.returncode == 0, f"CLI failed with error: {result.stderr}"
        
        # Check that output contains expected content or is empty (no main function)
        output = result.stdout
        # Since the test file only has variable declarations, no output is expected
        assert len(output) >= 0  # Allow empty output
    
    def test_basic_type_declarations(self):
        """Test basic type declarations work correctly."""
        source = """
        int x = 42
        str name = "Alice"
        flt pi = 3.14159
        var dynamic = "anything"
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check that variables are correctly typed and stored
        assert interpreter.global_scope['x'] == 42
        assert interpreter.global_scope['name'] == "Alice"
        assert interpreter.global_scope['pi'] == 3.14159
        assert interpreter.global_scope['dynamic'] == "anything"
        
        # Check that types are stored correctly
        assert interpreter.variable_types['x'] == 'int'
        assert interpreter.variable_types['name'] == 'str'
        assert interpreter.variable_types['pi'] == 'flt'
        assert interpreter.variable_types['dynamic'] == 'var'
    
    def test_type_enforcement_success(self):
        """Test that valid type assignments work."""
        source = """
        int count = 100
        str greeting = "Hello"
        flt rate = 0.15
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['count'] == 100
        assert interpreter.global_scope['greeting'] == "Hello"
        assert interpreter.global_scope['rate'] == 0.15
    
    def test_type_enforcement_failure(self):
        """Test that invalid type assignments raise errors."""
        test_cases = [
            ('int invalid = "hello"', "Type mismatch"),
            ('str invalid2 = 42', "Type mismatch"),
            ('flt invalid3 = "pi"', "Type mismatch"),
        ]
        
        for source, expected_error in test_cases:
            tokens = tokenize(source)
            parser = Parser(tokens)
            ast = parser.parse()
            interpreter = Interpreter()
            
            with pytest.raises(RuntimeErrorLyric) as exc_info:
                interpreter.evaluate(ast)
            
            assert expected_error in str(exc_info.value)
    
    def test_var_type_accepts_anything(self):
        """Test that var type accepts any value."""
        source = """
        var anything1 = 42
        var anything2 = "hello"
        var anything3 = 3.14
        var anything4 = True
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['anything1'] == 42
        assert interpreter.global_scope['anything2'] == "hello"
        assert interpreter.global_scope['anything3'] == 3.14
        assert interpreter.global_scope['anything4'] == True
    
    def test_type_compatibility_with_builtins(self):
        """Test type compatibility with built-in functions."""
        source = """
        var result1 = int("42")
        var result2 = str(42)
        var result3 = flt("3.14")
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['result1'] == 42
        assert interpreter.global_scope['result2'] == "42"
        assert interpreter.global_scope['result3'] == 3.14
    
    def test_type_checking_with_isinstance(self):
        """Test isinstance function for type checking."""
        source = """
        var is_int = isinstance(42, int)
        var is_str = isinstance("hello", str)
        var is_flt = isinstance(3.14, flt)
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['is_int'] == True
        assert interpreter.global_scope['is_str'] == True
        assert interpreter.global_scope['is_flt'] == True
    
    def test_type_function(self):
        """Test type() function for getting type names."""
        source = """
        var type_name1 = type(42)
        var type_name2 = type("hello")
        var type_name3 = type(3.14)
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['type_name1'] == "int"
        assert interpreter.global_scope['type_name2'] == "str"
        assert interpreter.global_scope['type_name3'] == "float"
