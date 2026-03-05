"""
Test suite for map type casting in Lyric.

Tests:
- int(map) returns number of keys
- flt(map) returns number of keys as float
- str(map) returns string representation
- arr(map) converts dict values to list
- map(arr) converts list to dict with string keys
- map(str) raises error
- map(map) identity operation
"""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


def parse(source: str, interactive: bool = False):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    if interactive:
        parser._interactive_mode = True
        parser.is_top_level = False
    return parser.parse()


def evaluate(ast):
    """def main() {\n    Helper to evaluate an AST.\n}"""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


class TestMapCasting:
    """def main() {\n    Test map type casting operations.\n}"""

    def test_int_map_returns_key_count(self):
        """def main() {\n    Test that int(map) returns the number of keys.\n}"""
        code = """
map person = {"name": "Alice", "age": 30, "city": "Seattle"}
int count = int(person)
print count
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3

    def test_float_map_returns_key_count_as_float(self):
        """def main() {\n    Test that flt(map) returns the number of keys as a float.\n}"""
        code = """
map data = {"x": 10, "y": 20}
flt count = flt(data)
print count
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2.0

    def test_str_map_returns_string_representation(self):
        """def main() {\n    Test that str(map) returns a string representation.\n}"""
        code = """
map config = {"host": "localhost", "port": 8080}
str representation = str(config)
print representation
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print string representation of dict

    def test_arr_map_converts_values_to_list(self):
        """def main() {\n    Test that arr(map) converts dictionary values to a list.\n}"""
        code = """
map scores = {"alice": 95, "bob": 87, "charlie": 92}
arr values = arr(scores)
print int(values)
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3

    def test_map_arr_converts_to_dict_with_string_keys(self):
        """def main() {\n    Test that map(arr) converts array to dict with string keys.\n}"""
        code = """
arr numbers = [100, 200, 300]
map indexed = map(numbers)
print indexed["1"]
print indexed["2"]
print indexed["3"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 100, 200, 300

    def test_map_str_raises_error(self):
        """def main() {\n    Test that map(str) raises an error.\n}"""
        code = """
str text = "hello"
map result = map(text)
"""
        ast = parse(code, interactive=True)
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            evaluate(ast)
        assert "Cannot directly convert str to map" in str(exc_info.value)

    def test_map_map_identity(self):
        """def main() {\n    Test that map(map) returns the same dictionary.\n}"""
        code = """
map original = {"a": 1, "b": 2}
map copy = map(original)
print int(copy)
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2

    def test_int_empty_map(self):
        """def main() {\n    Test that int() on an empty map returns 0.\n}"""
        code = """
map empty = {}
int count = int(empty)
print count
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 0

    def test_float_empty_map(self):
        """def main() {\n    Test that flt() on an empty map returns 0.0.\n}"""
        code = """
map empty = {}
flt count = flt(empty)
print count
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 0.0

    def test_arr_empty_map(self):
        """def main() {\n    Test that arr() on an empty map returns an empty list.\n}"""
        code = """
map empty = {}
arr values = arr(empty)
print int(values)
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 0

    def test_map_empty_arr(self):
        """def main() {\n    Test that map() on an empty array returns an empty dict.\n}"""
        code = """
arr empty = []
map result = map(empty)
print int(result)
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 0

    def test_arr_map_with_mixed_value_types(self):
        """def main() {\n    Test that arr(map) works with maps containing mixed value types.\n}"""
        code = """
map mixed = {"name": "Alice", "age": 30, "active": true}
arr values = arr(mixed)
print int(values)
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3

    def test_map_arr_with_mixed_types(self):
        """def main() {\n    Test that map(arr) works with arrays containing mixed types.\n}"""
        code = """
arr mixed = [42, "text", 3.14, true]
map result = map(mixed)
print result["1"]
print result["4"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 42, true

    def test_chained_casting_map_to_arr_to_map(self):
        """def main() {\n    Test chaining conversions: map -> arr -> map.\n}"""
        code = """
map original = {"a": 10, "b": 20, "c": 30}
arr as_arr = arr(original)
map back_to_map = map(as_arr)
print int(back_to_map)
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3 (three values)

    def test_casting_in_expressions(self):
        """def main() {\n    Test using map casting in arithmetic expressions.\n}"""
        code = """
map items = {"x": 1, "y": 2, "z": 3}
int double_count = int(items) * 2
print double_count
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 6

    def test_float_casting_in_division(self):
        """def main() {\n    Test using flt(map) in division.\n}"""
        code = """
map data = {"a": 1, "b": 2, "c": 3, "d": 4}
flt result = 10 / flt(data)
print result
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2.5

    def test_map_single_element(self):
        """def main() {\n    Test map operations with a single key-value pair.\n}"""
        code = """
map single = {"only": 999}
int count = int(single)
print count
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 1

    def test_arr_map_single_value(self):
        """def main() {\n    Test arr(map) with a single value.\n}"""
        code = """
map single = {"key": 42}
arr values = arr(single)
print values[0]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 42

    def test_map_arr_single_element(self):
        """def main() {\n    Test map(arr) with a single element.\n}"""
        code = """
arr single = [777]
map result = map(single)
print result["1"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 777

    def test_map_with_numeric_string_keys(self):
        """def main() {\n    Test that existing numeric string keys in maps are preserved.\n}"""
        code = """
map data = {"1": "first", "2": "second"}
int count = int(data)
print count
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2

    def test_arr_map_preserves_order(self):
        """def main() {\n    Test that arr(map) preserves insertion order of values.\n}"""
        code = """
map ordered = {"first": 1, "second": 2, "third": 3}
arr values = arr(ordered)
print int(values)
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

