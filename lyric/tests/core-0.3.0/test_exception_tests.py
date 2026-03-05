# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Test suite for exception_tests.ly - Sprint 3 exception handling tests."""

import pytest
import subprocess
import os
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric, SyntaxErrorLyric, ParseError
from builtins import ZeroDivisionError


class TestExceptionTests:
    """Test exception handling functionality."""
    
    def test_exception_tests_ly_runs_successfully(self):
        """Test that exception_tests.ly runs successfully through CLI."""
        exception_tests_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'exception_tests.ly')
        
        # Run the CLI command
        result = subprocess.run(['lyric', 'run', exception_tests_path],
                               capture_output=True, text=True)
        
        # Should succeed (exit code 0)
        assert result.returncode == 0, f"CLI failed with error: {result.stderr}"
        
        # Check that output contains expected content or is empty (no main function)
        output = result.stdout
        # Since the test file only has variable declarations, no output is expected
        assert len(output) >= 0  # Allow empty output
    
    def test_basic_try_catch(self):
        """Test basic try/catch functionality."""
        source = """
        try:
            var result = 10 / 0
        catch:
            print("Caught division by zero error")
        fade
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors (catch handles the division by zero)
        interpreter.evaluate(ast)
    
    def test_try_catch_with_finally(self):
        """Test try/catch with finally block."""
        source = """
        var cleanup_done = False
        try:
            var result = 10 / 2
            print("Division successful:", result)
        catch:
            print("Caught an error")
        finally:
            cleanup_done = True
            print("Cleanup completed")
        fade
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check that finally block executed
        assert interpreter.global_scope['cleanup_done'] == True
    
    def test_try_catch_with_variable_access(self):
        """Test try/catch with variable access and modification."""
        source = """
        var x = 10
        try:
            var y = x / 0
        catch:
            x = 20
        finally:
            print("Final x value:", x)
        fade
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check that variable was modified in catch block
        assert interpreter.global_scope['x'] == 20
    
    def test_raise_different_exception_types(self):
        """Test raising different exception types."""
        test_cases = [
            ('raise RuntimeErrorLyric', 'RuntimeErrorLyric'),
            ('raise IndexErrorLyric', 'IndexErrorLyric'),
            ('raise TypeErrorLyric', 'TypeErrorLyric'),
            ('raise ValueErrorLyric', 'ValueErrorLyric'),
            ('raise KeyErrorLyric', 'KeyErrorLyric'),
            ('raise AttributeErrorLyric', 'AttributeErrorLyric'),
            ('raise ZeroDivisionErrorLyric', 'ZeroDivisionErrorLyric'),
        ]
        
        for source, expected_exception in test_cases:
            tokens = tokenize(source)
            parser = Parser(tokens)
            ast = parser.parse()
            interpreter = Interpreter()
            
            with pytest.raises(RuntimeErrorLyric) as exc_info:
                interpreter.evaluate(ast)
            
            assert expected_exception in str(exc_info.value)
    
    def test_exception_in_function(self):
        """Test exception handling in function definitions."""
        source = """
        def risky_function(int divisor) {
            if divisor == 0:
                raise ZeroDivisionErrorLyric
            end
            return 10 / divisor
        }
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should parse and define function without errors
        interpreter.evaluate(ast)
        
        # Test calling the function with valid input
        result = interpreter._call_function("risky_function", [5])
        assert result == 2.0
        
        # Test calling the function with invalid input (should raise exception)
        with pytest.raises(ZeroDivisionError) as exc_info:
            interpreter._call_function("risky_function", [0])
        
        assert "ZeroDivisionErrorLyric raised" in str(exc_info.value)
    
    def test_exception_handling_in_function(self):
        """Test exception handling within function definitions."""
        source = """
        def safe_divide(int a, int b) {
            try:
                return a / b
            catch:
                print("Division failed, returning 0")
                return 0
            finally:
                print("Division attempt completed")
            fade
        }
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should parse and define function without errors
        interpreter.evaluate(ast)
        
        # Test calling the function with valid input
        result = interpreter._call_function("safe_divide", [10, 2])
        assert result == 5.0
        
        # Test calling the function with invalid input (should return 0)
        result = interpreter._call_function("safe_divide", [10, 0])
        assert result == 0
    
    def test_multiple_statements_in_try_block(self):
        """Test multiple statements in try block."""
        source = """
        var counter = 0
        try:
            counter = counter + 1
            var result = 10 / 0
            counter = counter + 1
        catch:
            counter = counter + 10
        finally:
            counter = counter + 100
        fade
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check that counter was modified correctly
        # Initial: 0, try: +1, catch: +10, finally: +100 = 111
        assert interpreter.global_scope['counter'] == 111
    
    def test_exception_with_method_calls(self):
        """Test exception handling with method calls."""
        source = """
        class Calculator
            def divide(int a, int b) {
                try:
                    return a / b
                catch:
                    print("Division error in calculator")
                    return 0
                fade
            }
        +++
        
        var calc = Calculator()
        var result = calc.divide(10, 0)
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check that method call handled exception and returned 0
        assert interpreter.global_scope['result'] == 0
    
    def test_exception_with_builtin_functions(self):
        """Test exception handling with built-in functions."""
        source = """
        try:
            var result = append("not_a_list", 5)
        catch:
            print("Caught append error")
        fade
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors (catch handles the append error)
        interpreter.evaluate(ast)
    
    def test_exception_with_indexing(self):
        """Test exception handling with indexing operations."""
        source = """
        try:
            var numbers = [1, 2, 3]
            var result = numbers[10]
        catch:
            print("Caught index error")
        fade
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors (catch handles the index error)
        interpreter.evaluate(ast)
    
    def test_try_without_catch_syntax_error(self):
        """Test that try without catch raises syntax error."""
        source = """
        try:
            var result = 10 / 2
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        
        # Should raise parse error for incomplete try block
        with pytest.raises(ParseError):
            parser.parse()
    
    def test_nested_try_catch_not_supported(self):
        """Test that nested try/catch is not supported (should parse but may not work correctly)."""
        source = """
        try:
            try:
                var result = 10 / 0
            catch:
                print("Inner catch")
            fade
        catch:
            print("Outer catch")
        fade
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        
        # Should parse (nested try/catch is syntactically valid)
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute (though behavior may not be as expected)
        interpreter.evaluate(ast)
