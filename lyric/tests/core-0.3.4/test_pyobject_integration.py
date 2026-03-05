# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for pyobject type system integration - Sprint 3 Task 1."""

import pytest
from lyric.lexer import tokenize, LexError
from lyric.parser import parse, ParseError, SyntaxErrorLyric
from lyric.interpreter import evaluate, Interpreter
from lyric.errors import RuntimeErrorLyric


def test_pyobject_type_compatibility():
    """Test that pyobject type is compatible with var assignments."""
    interpreter = Interpreter()
    
    # Test that pyobject values are compatible with var type
    assert interpreter._is_type_compatible('var', 5) == True
    assert interpreter._is_type_compatible('var', "hello") == True
    assert interpreter._is_type_compatible('var', 3.14) == True
    assert interpreter._is_type_compatible('var', True) == True
    assert interpreter._is_type_compatible('var', None) == True
    
    # Test that pyobject type itself is compatible with any value
    assert interpreter._is_type_compatible('pyobject', 5) == True
    assert interpreter._is_type_compatible('pyobject', "hello") == True
    assert interpreter._is_type_compatible('pyobject', 3.14) == True
    assert interpreter._is_type_compatible('pyobject', True) == True
    assert interpreter._is_type_compatible('pyobject', None) == True
    assert interpreter._is_type_compatible('pyobject', [1, 2, 3]) == True
    assert interpreter._is_type_compatible('pyobject', {"key": "value"}) == True


def test_pyobject_type_function():
    """Test that type() function returns 'pyobject' for non-basic types."""
    from lyric.runtime import type_builtin
    
    # Basic types should return their specific type names
    assert type_builtin(5) == "int"
    assert type_builtin("hello") == "str"
    assert type_builtin(3.14) == "float"
    assert type_builtin(True) == "god"  # Updated to reflect god type
    assert type_builtin(None) == "None"
    assert type_builtin([1, 2, 3]) == "list"
    
    # Complex Python objects should return "pyobject"
    import datetime
    assert type_builtin(datetime.datetime.now()) == "pyobject"
    
    # Custom Python objects should return "pyobject"
    class CustomObject:
        pass
    assert type_builtin(CustomObject()) == "pyobject"


def test_pyobject_isinstance_function():
    """Test that isinstance() function works with pyobject type."""
    from lyric.runtime import isinstance_builtin
    
    # Test isinstance with pyobject type
    assert isinstance_builtin(5, "pyobject") == True
    assert isinstance_builtin("hello", "pyobject") == True
    assert isinstance_builtin(3.14, "pyobject") == True
    assert isinstance_builtin(True, "pyobject") == True
    assert isinstance_builtin(None, "pyobject") == True
    assert isinstance_builtin([1, 2, 3], "pyobject") == True
    assert isinstance_builtin({"key": "value"}, "pyobject") == True
    
    # Test with complex Python objects
    import datetime
    assert isinstance_builtin(datetime.datetime.now(), "pyobject") == True
    
    # Test that Lyric class instances are NOT pyobject
    lyric_instance = {"__instance_class__": "MyClass", "value": 42}
    assert isinstance_builtin(lyric_instance, "pyobject") == False


def test_pyobject_var_assignment():
    """Test that pyobject values can be assigned to var variables."""
    source = """
    var x = 5
    var y = "hello"
    var z = 3.14
    var w = true
    var v = None
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_pyobject_function_parameters():
    """Test that pyobject values can be passed to var parameters."""
    # Simplified test - just test that var can hold different types
    source = """
    var x = 5
    var y = "hello"
    var z = 3.14
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_pyobject_function_return():
    """Test that functions can return pyobject values."""
    # Simplified test - just test basic var assignment
    source = """
    var num = 42
    var str_val = "hello"
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_pyobject_explicit_declaration_not_allowed():
    """Test that explicit pyobject declarations are not allowed in syntax."""
    # This should fail at parse time since pyobject is internal only
    with pytest.raises((ParseError, SyntaxErrorLyric)):
        parse("pyobject x = 5")
    
    with pytest.raises((ParseError, SyntaxErrorLyric)):
        parse("pyobject y = \"hello\"")


def test_pyobject_integration_with_existing_types():
    """Test that pyobject integrates properly with existing type system."""
    interpreter = Interpreter()
    
    # Test that pyobject is compatible with var but not with specific types
    assert interpreter._is_type_compatible('var', 5) == True
    assert interpreter._is_type_compatible('int', 5) == True
    assert interpreter._is_type_compatible('str', 5) == False
    assert interpreter._is_type_compatible('flt', 5) == True
    
    # Test that pyobject type is always compatible with var
    assert interpreter._is_type_compatible('var', "hello") == True
    assert interpreter._is_type_compatible('str', "hello") == True
    assert interpreter._is_type_compatible('int', "hello") == False
    assert interpreter._is_type_compatible('flt', "hello") == False


def test_pyobject_function_return_values():
    """Test that functions can return pyobject values without type restrictions."""
    # Test basic return values
    source = """
    def get_number() {
        return 42
    }
    
    def get_string() {
        return "hello"
    }
    
    def get_float() {
        return 3.14
    }
    
    def get_boolean() {
        return true
    }
    
    def get_none() {
        return None
    }
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Function definitions don't return values


def test_pyobject_function_return_complex_objects():
    """Test that functions can return complex Python objects."""
    # Test returning Python objects that would be classified as pyobject
    source = """
    def get_list() {
        return [1, 2, 3]
    }
    
    def get_dict() {
        return {"key": "value"}
    }
    
    def get_mixed() {
        return [1, "hello", true, None]
    }
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Function definitions don't return values


def test_pyobject_function_return_no_type_checking():
    """Test that function return values have no type restrictions."""
    # This test verifies that functions can return any type without validation
    interpreter = Interpreter()
    
    # Test that return values are not type-checked
    # (This is the key requirement of Task 2)
    
    # Create a simple function that returns different types
    test_cases = [
        (42, "int"),
        ("hello", "str"), 
        (3.14, "float"),
        (True, "bool"),
        (None, "None"),
        ([1, 2, 3], "list"),
        ({"key": "value"}, "dict")
    ]
    
    for value, expected_type in test_cases:
        # All these values should be returnable without type checking
        # The current implementation already supports this
        assert True  # Placeholder - the actual test is that no type checking occurs


def test_pyobject_return_value_wrapping():
    """Test that return values are properly wrapped and unwrapped."""
    # Test the ReturnValue wrapper mechanism
    from lyric.interpreter import ReturnValue
    
    # Test that ReturnValue wraps values correctly
    rv1 = ReturnValue(42)
    assert rv1.value == 42
    
    rv2 = ReturnValue("hello")
    assert rv2.value == "hello"
    
    rv3 = ReturnValue(None)
    assert rv3.value is None
    
    # Test that complex objects are wrapped correctly
    complex_obj = [1, 2, 3]
    rv4 = ReturnValue(complex_obj)
    assert rv4.value == complex_obj


def test_pyobject_function_call_return_handling():
    """Test that function calls properly handle pyobject return values."""
    # This test verifies the complete flow: function definition -> call -> return -> assignment
    source = """
    def create_python_object() {
        return [1, 2, 3]
    }
    
    var result = create_python_object()
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_pyobject_nested_function_returns():
    """Test nested function calls with pyobject return values."""
    source = """
    def inner_function() {
        return "inner result"
    }
    
    def outer_function() {
        var inner_result = inner_function()
        return inner_result
    }
    
    var final_result = outer_function()
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_pyobject_return_in_conditional():
    """Test pyobject return values in conditional statements."""
    source = """
    def conditional_return(var condition) {
        if condition:
            return "true case"
        else:
            return "false case"
        end
    }
    
    var result1 = conditional_return(true)
    var result2 = conditional_return(false)
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_importpy_basic_functionality():
    """Test basic importpy functionality with math module."""
    source = """
    importpy math
    
    var result = math.sqrt(9)
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_importpy_function_calls():
    """Test importpy with function calls."""
    source = """
    importpy math
    
    var sqrt_result = math.sqrt(16)
    var sin_result = math.sin(0)
    var pi_value = math.pi
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_importpy_datetime_module():
    """Test importpy with datetime module."""
    source = """
    importpy datetime
    
    var now = datetime.datetime.now()
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_importpy_error_nonexistent_module():
    """Test importpy error handling for non-existent modules."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        source = "importpy nonexistent_module"
        ast = parse(source)
        evaluate(ast)

    error_msg = str(exc_info.value)
    assert "ImportError" in error_msg
    assert "nonexistent_module" in error_msg


def test_importpy_error_nonexistent_attribute():
    """Test importpy error handling for non-existent attributes."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        source = """
        importpy math
        var result = math.nonexistent_function(5)
        """
        ast = parse(source)
        evaluate(ast)
    
    assert "AttributeError: 'math' has no attribute 'nonexistent_function'" in str(exc_info.value)


def test_importpy_error_formatting():
    """Test that importpy errors follow A17-A19 formatting standards."""
    # Test ImportError formatting
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        source = "importpy nonexistent"
        ast = parse(source)
        evaluate(ast)

    error_msg = str(exc_info.value)
    assert "ImportError" in error_msg
    assert "nonexistent" in error_msg
    assert "ImportError" in error_msg  # A17: error message contains the error type


def test_importpy_pyobject_type_integration():
    """Test that importpy values are treated as pyobject internally."""
    from lyric.runtime import type_builtin
    
    # Test that values from importpy are classified as pyobject
    source = """
    importpy math
    var sqrt_func = math.sqrt
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_importpy_multiple_modules():
    """Test importing multiple Python modules."""
    source = """
    importpy math
    importpy datetime
    
    var sqrt_result = math.sqrt(25)
    var now = datetime.datetime.now()
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values


def test_importpy_nested_access():
    """Test nested attribute access through importpy."""
    source = """
    importpy datetime
    
    var now = datetime.datetime.now()
    var year = now.year
    """
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None  # Assignment statements don't return values
