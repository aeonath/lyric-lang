# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Test integration with importpy_tests.ly example file."""

import pytest
import subprocess
import sys
import os
from pathlib import Path

# Add the lyric module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lyric.cli import main
from lyric.interpreter import Interpreter
from lyric.parser import Parser
from lyric.lexer import Lexer


class TestImportPyIntegration:
    """Test the importpy_tests.ly example file integration."""


    def test_importpy_basic_functionality(self):
        """Test basic importpy functionality through interpreter."""
        source = """
importpy math
var result = math.sqrt(16)
print(result)
"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Capture output
        import io
        import contextlib
        
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            interpreter.evaluate(ast)
        
        result = output.getvalue().strip()
        assert result == "4.0", f"Expected 4.0, got {result}"

    def test_importpy_datetime_functionality(self):
        """Test datetime module importpy functionality."""
        source = """
importpy datetime
var now = datetime.datetime.now()
print(now.year)
"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Capture output
        import io
        import contextlib
        
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            interpreter.evaluate(ast)
        
        result = output.getvalue().strip()
        # Should print current year (2025)
        assert result.isdigit(), f"Expected year as digits, got {result}"
        assert len(result) == 4, f"Expected 4-digit year, got {result}"

    def test_importpy_chained_access(self):
        """Test chained member access with importpy."""
        source = """
importpy math
var pi = math.pi
var sqrt_func = math.sqrt
var result = sqrt_func(25)
print(result)
"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Capture output
        import io
        import contextlib
        
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            interpreter.evaluate(ast)
        
        result = output.getvalue().strip()
        assert result == "5.0", f"Expected 5.0, got {result}"

    def test_importpy_error_handling(self):
        """Test that importpy errors are handled gracefully."""
        source = """
importpy nonexistent_module
"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should raise ImportError
        with pytest.raises(Exception) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "ImportError" in error_msg
        assert "nonexistent_module" in error_msg

    def test_importpy_attribute_error_handling(self):
        """Test that attribute errors are handled gracefully."""
        source = """
importpy math
var result = math.nonexistent_function(5)
"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should raise AttributeError
        with pytest.raises(Exception) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "AttributeError" in error_msg
        assert "nonexistent_function" in error_msg

    def test_importpy_pyobject_type_integration(self):
        """Test that pyobject values work with var type."""
        source = """
importpy math
var math_obj = math
var sqrt_func = math_obj.sqrt
var result = sqrt_func(36)
print(result)
"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Capture output
        import io
        import contextlib
        
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            interpreter.evaluate(ast)
        
        result = output.getvalue().strip()
        assert result == "6.0", f"Expected 6.0, got {result}"

    def test_importpy_multiple_modules(self):
        """Test importing multiple modules."""
        source = """
importpy math
importpy datetime
importpy os

var pi = math.pi
var now = datetime.datetime.now()
var cwd = os.getcwd()

print("Multiple modules imported successfully")
"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Capture output
        import io
        import contextlib
        
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            interpreter.evaluate(ast)
        
        result = output.getvalue().strip()
        assert "Multiple modules imported successfully" in result

    def test_importpy_function_parameters_and_returns(self):
        """Test pyobject function parameters and returns."""
        source = """
importpy math

    def test_function(var func, var value) {
        return func(value)
    }

var result = test_function(math.sqrt, 49)
print(result)
"""
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Capture output
        import io
        import contextlib
        
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            interpreter.evaluate(ast)
        
        result = output.getvalue().strip()
        assert result == "7.0", f"Expected 7.0, got {result}"
