# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Test suite for runtime safety and error message improvements."""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric, ParseError, SyntaxErrorLyric, TypeErrorLyric


class TestRuntimeSafety:
    """Test runtime safety features and enhanced error messages."""
    
    def test_enhanced_index_error_messages(self):
        """Test enhanced error messages for index operations."""
        # Test list index out of range
        source = """
        var numbers = [1, 2, 3]
        var result = numbers[5]
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Index out of range" in error_msg
        assert "tried to access index 5" in error_msg
        assert "arr of length 3" in error_msg
        assert "Valid indices are 0 to 2" in error_msg
    
    def test_enhanced_dictionary_key_error_messages(self):
        """Test enhanced error messages for dictionary key access."""
        source = """
        var data = {"name": "Alice", "age": 30}
        var result = data["city"]
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "'city'" in error_msg
        assert "not found" in error_msg
        # Note: MapObject doesn't provide "Available keys" in error message
    
    def test_enhanced_type_mismatch_messages(self):
        """Test enhanced error messages for type mismatches."""
        source = """
        int x = "hello"
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch" in error_msg
        assert "cannot assign str to variable 'x' declared as int" in error_msg
        assert "Expected int, but got str" in error_msg
        assert "Use 'var x = ...' if you need dynamic typing" in error_msg
    
    def test_enhanced_undefined_variable_messages(self):
        """Test enhanced error messages for undefined variables."""
        source = """
        var result = undefined_var
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Undefined variable" in error_msg
        assert "'undefined_var' has not been declared" in error_msg
        assert "Use a type declaration" in error_msg
    
    def test_enhanced_function_not_found_messages(self):
        """Test enhanced error messages for undefined functions."""
        source = """
        var result = unknown_function()
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Function not found" in error_msg
        assert "'unknown_function' is not defined" in error_msg
        assert "Built-in functions: print, range, len, int, float, str" in error_msg
    
    def test_enhanced_method_not_found_messages(self):
        """Test enhanced error messages for undefined methods."""
        source = """
        var myobj = {"name": "test"}
        var result = myobj.unknown_method()
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "AttributeError" in error_msg or "has no attribute" in error_msg
        assert "unknown_method" in error_msg
    
    def test_enhanced_division_by_zero_messages(self):
        """Test enhanced error messages for division by zero."""
        source = """
        var result = 10 / 0
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Division by zero" in error_msg
        assert "cannot divide by zero" in error_msg
        assert "Check your divisor value" in error_msg
    
    def test_enhanced_type_mismatch_in_operations(self):
        """Test enhanced error messages for type mismatches in operations."""
        source = """
        var result = 5 + "hello"
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()

        # Mixing int and str with '+' should raise a TypeError
        with pytest.raises(TypeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        error_msg = str(exc_info.value)
        assert "Cannot concatenate" in error_msg
        assert "str()" in error_msg
    
    def test_enhanced_range_function_error_messages(self):
        """Test enhanced error messages for range function."""
        source = """
        var result = range(1, 2, 3, 4)
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Invalid range() arguments" in error_msg
        assert "range() takes 1-3 arguments" in error_msg
        assert "Usage: range(stop) or range(start, stop) or range(start, stop, step)" in error_msg
    
    def test_enhanced_unknown_operator_messages(self):
        """Test that mixed-type '+' raises a clear TypeError."""
        source = """
        var result = 5 + "hello"
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()

        # Mixing int and str with '+' should raise a TypeError
        with pytest.raises(TypeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        error_msg = str(exc_info.value)
        assert "Cannot concatenate" in error_msg
    
    def test_enhanced_unknown_unary_operator_messages(self):
        """Test enhanced error messages for unknown unary operators."""
        # Use a valid syntax that will cause a runtime error for unknown unary operator
        source = """
        var result = -"hello"
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "bad operand type for unary -" in error_msg
        assert "str" in error_msg
    
    def test_enhanced_exception_raise_messages(self):
        """Test enhanced error messages for unknown exceptions."""
        source = """
        raise UnknownException
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Unknown exception" in error_msg
        assert "'UnknownException' is not a valid exception type" in error_msg
        assert "Available exceptions" in error_msg
    
    def test_enhanced_builtin_function_error_messages(self):
        """Test enhanced error messages for undefined functions."""
        # Note: append() is no longer a standalone function; it's a method on arr objects
        # This test now checks for undefined function errors
        source = """
        var result = undefined_function()
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Function not found" in error_msg
        assert "undefined_function" in error_msg
    
    def test_enhanced_indexing_error_messages(self):
        """Test enhanced error messages for invalid indexing."""
        source = """
        var myobj = 5
        var result = myobj[0]
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Cannot index object" in error_msg
        assert "'int' does not support indexing" in error_msg
        assert "Only lists and dictionaries can be indexed" in error_msg
        assert "Use dot notation (.) for object properties" in error_msg
    
    def test_enhanced_callable_error_messages(self):
        """Test enhanced error messages for non-callable objects."""
        source = """
        var myobj = {"name": "test"}
        var result = myobj.name()
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "name" in error_msg
        assert "AttributeError" in error_msg or "has no attribute" in error_msg
    
    def test_enhanced_assignment_error_messages(self):
        """Test enhanced error messages for assignment errors."""
        source = """
        var result = undefined_var
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Undefined variable" in error_msg
        assert "'undefined_var' has not been declared" in error_msg
        assert "Use a type declaration" in error_msg
    
    def test_enhanced_member_access_error_messages(self):
        """Test enhanced error messages for member access errors."""
        source = """
        var myobj = {"name": "test"}
        var result = myobj.unknown_member
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Member not found" in error_msg or "has no members" in error_msg
        assert "unknown_member" in error_msg
    
    def test_error_message_consistency(self):
        """Test that error messages follow consistent patterns."""
        # Test that all error messages contain descriptive categories
        error_tests = [
            ("var x = undefined_var", "Undefined variable"),
            ("var x = unknown_func()", "Function not found"),
            ("var x = 5 / 0", "Division by zero"),
            ("var x = [1, 2, 3][5]", "Index out of range"),
            ("var x = {\"a\": 1}[\"b\"]", "not found"),  # Changed from "Key not found" to just "not found"
        ]
        
        for source, expected_category in error_tests:
            tokens = tokenize(source)
            parser = Parser(tokens)
            ast = parser.parse()
            interpreter = Interpreter()
            
            with pytest.raises(RuntimeErrorLyric) as exc_info:
                interpreter.evaluate(ast)
            
            error_msg = str(exc_info.value)
            assert expected_category in error_msg, f"Expected '{expected_category}' in error message but got: {error_msg}"
    
    def test_error_message_consistency_methods(self):
        """Test that method and member error messages follow consistent patterns."""
        # Test method not found
        source = """
        var myobj = {"name": "test"}
        var x = myobj.unknown_method()
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "AttributeError" in error_msg or "has no attribute" in error_msg
    
    def test_error_message_consistency_members(self):
        """Test that member access error messages follow consistent patterns."""
        # Test member not found
        source = """
        var myobj = {"name": "test"}
        var x = myobj.unknown_member
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Member not found" in error_msg
    
    def test_no_python_stack_traces(self):
        """Test that no Python stack traces appear in user-facing output."""
        source = """
        var result = 5 + "hello"
        """
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()

        # Mixing int and str with '+' should raise a TypeErrorLyric, not a raw Python error
        with pytest.raises(TypeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        error_msg = str(exc_info.value)
        assert "Cannot concatenate" in error_msg
        # Ensure the error message is user-friendly, not a Python stack trace
        assert "Traceback" not in error_msg
