# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for function parameter type annotations."""

import pytest
from lyric.lexer import tokenize, LexError
from lyric.parser import parse, ParseError, SyntaxErrorLyric
from lyric.interpreter import evaluate, Interpreter
from lyric.errors import RuntimeErrorLyric


def test_typed_function_parameter_parsing():
    """Test parsing of functions with typed parameters."""
    source = "def add(int x, int y) { return x + y }"
    ast = parse(source)
    
    assert len(ast.statements) == 1
    func = ast.statements[0]
    assert func.name == 'add'
    assert func.params == ['x', 'y']
    assert func.param_types == ['int', 'int']


def test_mixed_typed_untyped_parameters():
    """Test parsing of functions with mixed typed and untyped parameters."""
    source = "def process(int x, str name, var data) { return x }"
    ast = parse(source)
    
    assert len(ast.statements) == 1
    func = ast.statements[0]
    assert func.name == 'process'
    assert func.params == ['x', 'name', 'data']
    assert func.param_types == ['int', 'str', 'var']


def test_untyped_function_parameters():
    """Test parsing of functions with untyped parameters (backward compatibility)."""
    source = "def greet(name) { return name }"
    ast = parse(source)
    
    assert len(ast.statements) == 1
    func = ast.statements[0]
    assert func.name == 'greet'
    assert func.params == ['name']
    assert func.param_types == ['var']  # Default to var


def test_typed_parameter_enforcement():
    """Test that typed parameters enforce type checking."""
    source = """
    def add(int x, int y) {
        return x + y
    }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    # Valid call
    result = interpreter._call_function("add", [5, 10])
    assert result == 15
    
    # Invalid call - wrong type
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        interpreter._call_function("add", ["hello", 10])
    
    assert "Type error: parameter 'x' expects int, got str" in str(exc_info.value)


def test_mixed_parameter_type_enforcement():
    """Test type enforcement with mixed parameter types."""
    source = """
    def process(int x, str name, var data) {
        return x
    }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    # Valid call
    result = interpreter._call_function("process", [5, "hello", [1, 2, 3]])
    assert result == 5
    
    # Invalid call - wrong type for int parameter
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        interpreter._call_function("process", ["hello", "world", None])
    
    assert "Type error: parameter 'x' expects int, got str" in str(exc_info.value)
    
    # Invalid call - wrong type for str parameter
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        interpreter._call_function("process", [5, 42, None])
    
    assert "Type error: parameter 'name' expects str, got int" in str(exc_info.value)


def test_var_parameter_accepts_any_type():
    """Test that var parameters accept any type."""
    source = """
    def flexible(var data) {
        return data
    }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    # All these should work without type errors
    test_cases = [5, "hello", 3.14, True, None, [1, 2, 3]]
    
    for test_value in test_cases:
        result = interpreter._call_function("flexible", [test_value])
        assert result == test_value


def test_typed_class_method_parameters():
    """Test typed parameters in class methods."""
    source = """
    class Calculator
        def add(int x, int y) {
            return x + y
        }
    +++
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    # Create instance using function call evaluation
    from lyric.ast_nodes import CallNode, LiteralNode
    calc_call = CallNode("Calculator", [])
    calc = interpreter._evaluate_function_call(calc_call)
    
    # Valid method call
    result = interpreter._call_method(calc, interpreter.classes["Calculator"]["add"], 
                                    [LiteralNode(5), LiteralNode(10)])
    assert result == 15
    
    # Invalid method call
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        interpreter._call_method(calc, interpreter.classes["Calculator"]["add"], 
                                [LiteralNode("hello"), LiteralNode(10)])
    
    assert "Type error: parameter 'x' expects int, got str" in str(exc_info.value)


def test_function_with_no_parameters():
    """Test function with no parameters."""
    source = """
    def get_answer() {
        return 42
    }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    result = interpreter._call_function("get_answer", [])
    assert result == 42


def test_complex_typed_function():
    """Test complex function with multiple typed parameters."""
    source = """
    def calculate(int a, flt b, str operation, var extra) {
        if operation == "add":
            return a + b
        else:
            return extra
        end
    }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    # Valid calls
    result1 = interpreter._call_function("calculate", [5, 3.14, "add", None])
    assert result1 == 8.14
    
    result2 = interpreter._call_function("calculate", [10, 2.5, "multiply", "done"])
    assert result2 == "done"
    
    # Invalid calls
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        interpreter._call_function("calculate", ["hello", 3.14, "add", None])
    
    assert "Type error: parameter 'a' expects int, got str" in str(exc_info.value)


def test_parameter_type_inference():
    """Test that untyped parameters default to var type."""
    source = """
    def test(x, y) {
        return x + y
    }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    func_def = interpreter.functions["test"]
    assert func_def['param_types'] == ['var', 'var']
    
    # Should accept compatible types
    result = interpreter._call_function("test", [5, 10])
    assert result == 15
    
    # Should accept string concatenation
    result = interpreter._call_function("test", ["hello", "world"])
    assert result == "helloworld"


def test_typed_parameter_syntax_errors():
    """Test syntax errors in typed parameter declarations."""
    # Missing parameter name after type
    with pytest.raises((ParseError, SyntaxErrorLyric)):
        parse("def test(int) { return 5 }")
    
    # Missing type before parameter name (this should work - defaults to var)
    source = "def test(x) { return 5 }"
    ast = parse(source)
    assert ast.statements[0].param_types == ['var']


def test_nested_function_calls_with_types():
    """Test nested function calls with typed parameters."""
    source = """
    def outer(int x) {
        return inner(x + 1)
    }
    
    def inner(int y) {
        return y * 2
    }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    result = interpreter._call_function("outer", [5])
    assert result == 12  # (5 + 1) * 2


def test_typed_parameters_with_default_values():
    """Test that typed parameters work with function calls."""
    source = """
    def multiply(int x, int y) {
        return x * y
    }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    # Test with different argument counts
    result = interpreter._call_function("multiply", [3, 4])
    assert result == 12
    
    # Test with fewer arguments (y defaults to None — accepted as nullable,
    # but arithmetic with None causes a runtime type mismatch)
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        interpreter._call_function("multiply", [3])

    assert "Type mismatch in operation" in str(exc_info.value)


def test_type_compatibility_edge_cases():
    """Test edge cases in type compatibility."""
    source = """
    def test_int(int x) { return x }
    def test_flt(flt y) { return y }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    # int should accept integers but not floats
    result = interpreter._call_function("test_int", [5])
    assert result == 5
    
    # flt should accept both int and float
    result1 = interpreter._call_function("test_flt", [5])
    assert result1 == 5
    
    result2 = interpreter._call_function("test_flt", [3.14])
    assert result2 == 3.14
    
    # int should not accept boolean True (which is int in Python)
    with pytest.raises(RuntimeErrorLyric):
        interpreter._call_function("test_int", [True])


def test_function_parameter_type_storage():
    """Test that parameter types are correctly stored in function definitions."""
    source = """
    def example(int a, str b, flt c, var d) {
        return a
    }
    """
    interpreter = Interpreter()
    interpreter.evaluate(parse(source))
    
    func_def = interpreter.functions["example"]
    assert func_def['params'] == ['a', 'b', 'c', 'd']
    assert func_def['param_types'] == ['int', 'str', 'flt', 'var']
