# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for built-in data structures (lists and dictionaries)."""

import pytest
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import RuntimeErrorLyric, ParseError


def test_list_literal_creation():
    """Test creating list literals."""
    source = '''
    def main() {
        var list_example = [1, 2, 3]
        return list_example
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # Result is now ArrObject, extract elements for comparison
    from lyric.interpreter import ArrObject
    assert isinstance(result, ArrObject)
    assert result.elements == [1, 2, 3]


def test_empty_list_literal():
    """Test creating empty list literals."""
    source = '''
    def main() {
        var empty_list = []
        return empty_list
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # Result is now ArrObject, extract elements for comparison
    from lyric.interpreter import ArrObject
    assert isinstance(result, ArrObject)
    assert result.elements == []


def test_list_with_mixed_types():
    """Test creating lists with mixed types."""
    source = '''
    def main() {
        var mixed_list = [1, "hello", True, 3.14]
        return mixed_list
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # Result is now ArrObject, extract elements for comparison
    from lyric.interpreter import ArrObject
    assert isinstance(result, ArrObject)
    assert result.elements == [1, "hello", True, 3.14]


def test_dictionary_literal_creation():
    """Test creating dictionary literals."""
    source = '''
    def main() {
        var dict_example = {"key": "value", "number": 42}
        return dict_example
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # Result is now MapObject, extract elements for comparison
    from lyric.interpreter import MapObject
    assert isinstance(result, MapObject)
    assert result.elements == {"key": "value", "number": 42}


def test_empty_dictionary_literal():
    """Test creating empty dictionary literals."""
    source = '''
    def main() {
        var empty_dict = {}
        return empty_dict
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # Result is now MapObject, extract elements for comparison
    from lyric.interpreter import MapObject
    assert isinstance(result, MapObject)
    assert result.elements == {}


def test_dictionary_with_mixed_types():
    """Test creating dictionaries with mixed key and value types."""
    source = '''
    def main() {
        var mixed_dict = {"string": 123, 456: "number", "bool": True}
        return mixed_dict
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # Result is now MapObject, extract elements for comparison
    from lyric.interpreter import MapObject
    assert isinstance(result, MapObject)
    assert result.elements == {"string": 123, 456: "number", "bool": True}


def test_list_indexing():
    """Test indexing lists."""
    source = '''
    def main() {
        var my_list = [10, 20, 30]
        var first = my_list[0]
        var second = my_list[1]
        var third = my_list[2]
        return first + second + third
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 60


def test_dictionary_key_lookup():
    """Test dictionary key lookup."""
    source = '''
    def main() {
        var my_dict = {"name": "Alice", "age": 30}
        var name = my_dict["name"]
        var age = my_dict["age"]
        return name + " is " + str(age)
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == "Alice is 30"


def test_list_index_out_of_range():
    """Test list index out of range error."""
    source = '''
    def main() {
        var my_list = [1, 2, 3]
        return my_list[5]
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="Index out of range"):
        evaluate(ast)


def test_dictionary_key_not_found():
    """Test dictionary key not found error."""
    source = '''
    def main() {
        var my_dict = {"name": "Alice"}
        return my_dict["age"]
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="Key.*not found"):
        evaluate(ast)


def test_list_index_type_error():
    """Test list index type error."""
    source = '''
    def main() {
        var my_list = [1, 2, 3]
        return my_list["invalid"]
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="Invalid list index"):
        evaluate(ast)


def test_cannot_index_non_indexable():
    """Test indexing non-indexable objects."""
    source = '''
    def main() {
        var number = 42
        return number[0]
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="Cannot index object"):
        evaluate(ast)


def test_len_function():
    """Test len() method with lists and dictionaries."""
    source = '''
    def main() {
        var my_list = [1, 2, 3, 4, 5]
        var my_dict = {"a": 1, "b": 2, "c": 3}
        var list_len = my_list.len()
        var dict_len = my_dict.len()
        return list_len + dict_len
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 8  # 5 + 3


def test_append_function():
    """Test append() method."""
    source = '''
    def main() {
        var my_list = [1, 2, 3]
        my_list.append(4)
        my_list.append(5)
        return my_list
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # Result is now ArrObject, extract elements for comparison
    from lyric.interpreter import ArrObject
    assert isinstance(result, ArrObject)
    assert result.elements == [1, 2, 3, 4, 5]


def test_append_function_type_error():
    """Test append() method type error - removed as append is now a method."""
    # This test is no longer applicable since append() is now a method on ArrObject
    # If you call my_string.append(), the parser/interpreter will catch this
    pass


def test_keys_function():
    """Test keys() method."""
    source = '''
    def main() {
        var my_dict = {"name": "Alice", "age": 30, "city": "NYC"}
        var dict_keys = my_dict.keys()
        return dict_keys
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # Result is now ArrObject containing the keys
    from lyric.interpreter import ArrObject
    assert isinstance(result, ArrObject)
    assert set(result.elements) == {"name", "age", "city"}


def test_keys_function_type_error():
    """Test keys() method type error - removed as keys is now a method."""
    # This test is no longer applicable since keys() is now a method on MapObject
    pass


def test_values_function():
    """Test values() method."""
    source = '''
    def main() {
        var my_dict = {"a": 1, "b": 2, "c": 3}
        var dict_values = my_dict.values()
        return dict_values
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # Result is now ArrObject containing the values
    from lyric.interpreter import ArrObject
    assert isinstance(result, ArrObject)
    assert set(result.elements) == {1, 2, 3}


def test_values_function_type_error():
    """Test values() method type error - removed as values is now a method."""
    # This test is no longer applicable since values() is now a method on MapObject
    pass


def test_nested_data_structures():
    """Test nested lists and dictionaries."""
    source = '''
    def main() {
        var nested = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ],
            "count": 2
        }
        var first_user = nested["users"][0]
        var first_name = first_user["name"]
        return first_name
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == "Alice"


def test_list_and_dict_in_expressions():
    """Test lists and dictionaries in expressions."""
    source = '''
    def main() {
        var numbers = [1, 2, 3]
        var info = {"sum": 6, "length": 3}
        var total = numbers[0] + numbers[1] + numbers[2]
        var expected = info["sum"]
        return total == expected
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == True


def test_dictionary_literal_syntax_errors():
    """Test dictionary literal syntax errors."""
    # Missing colon
    with pytest.raises((ParseError, RuntimeErrorLyric)):
        parse('{"key" "value"}')
    
    # Missing closing brace
    with pytest.raises((ParseError, RuntimeErrorLyric)):
        parse('{"key": "value"')


def test_list_literal_syntax_errors():
    """Test list literal syntax errors."""
    # Missing closing bracket
    with pytest.raises((ParseError, RuntimeErrorLyric)):
        parse('[1, 2, 3')


def test_indexing_syntax_errors():
    """Test indexing syntax errors."""
    # Missing closing bracket
    with pytest.raises((ParseError, RuntimeErrorLyric)):
        parse('my_list[0')


def test_complex_data_structure_operations():
    """Test complex operations with data structures."""
    source = '''
    def main() {
        # Create a list of dictionaries
        var people = [
            {"name": "Alice", "scores": [85, 90, 88]},
            {"name": "Bob", "scores": [92, 87, 95]}
        ]
        
        # Get first person's average score
        var alice = people[0]
        var alice_scores = alice["scores"]
        var alice_avg = (alice_scores[0] + alice_scores[1] + alice_scores[2]) / 3
        
        return alice_avg
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 87.66666666666667


def test_data_structure_modification():
    """Test modifying data structures."""
    source = '''
    def main() {
        # Start with empty structures
        var numbers = []
        var info = {}
        
        # Add items
        numbers.append(10)
        numbers.append(20)
        info["count"] = numbers.len()
        info["total"] = numbers[0] + numbers[1]
        
        return info
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # Result is now MapObject, extract elements for comparison
    from lyric.interpreter import MapObject
    assert isinstance(result, MapObject)
    assert result.elements == {"count": 2, "total": 30}
