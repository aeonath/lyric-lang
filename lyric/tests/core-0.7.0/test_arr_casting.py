"""
Test suite for arr type casting in Lyric.

Tests:
- int(arr) returns length
- flt(arr) returns length as float
- str(arr) returns string representation
- map(arr) converts to dict with string keys
- arr(str) converts string to list of characters
- arr(map) converts dict values to list
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


class TestArrCasting:
    """def main() {\n    Test arr type casting operations.\n}"""

    def test_int_arr_returns_length(self):
        """def main() {\n    Test that int(arr) returns the length of the array.\n}"""
        code = """
arr numbers = [10, 20, 30, 40, 50]
int length = int(numbers)
print length
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 5

    def test_float_arr_returns_length_as_float(self):
        """def main() {\n    Test that flt(arr) returns the length as a float.\n}"""
        code = """
arr items = [1, 2, 3]
flt length = flt(items)
print length
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3.0

    def test_str_arr_returns_string_representation(self):
        """def main() {\n    Test that str(arr) returns a string representation.\n}"""
        code = """
arr colors = ["red", "green", "blue"]
str representation = str(colors)
print representation
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print string representation of list

    def test_map_arr_converts_to_dict_with_string_keys(self):
        """def main() {\n    Test that map(arr) converts array to dict with string keys "1", "2", "3", etc.\n}"""
        code = """
arr values = [100, 200, 300]
map result = map(values)
print result["1"]
print result["2"]
print result["3"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 100, 200, 300

    def test_arr_str_converts_to_list_of_characters(self):
        """def main() {\n    Test that arr(str) converts a string to a list of characters.\n}"""
        code = """
str word = "hello"
arr chars = arr(word)
print chars[0]
print chars[1]
print chars[2]
print chars[3]
print chars[4]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print h, e, l, l, o

    def test_arr_map_converts_dict_values_to_list(self):
        """def main() {\n    Test that arr(map) converts dict values to a list.\n}"""
        code = """
map person = {"name": "Alice", "age": 30, "city": "Seattle"}
arr values = arr(person)
print values.len()
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3

    def test_int_empty_arr(self):
        """def main() {\n    Test that int() on an empty array returns 0.\n}"""
        code = """
arr empty = []
int count = int(empty)
print count
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 0

    def test_float_empty_arr(self):
        """def main() {\n    Test that flt() on an empty array returns 0.0.\n}"""
        code = """
arr empty = []
flt count = flt(empty)
print count
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 0.0

    def test_arr_empty_string(self):
        """def main() {\n    Test that arr() on an empty string returns an empty list.\n}"""
        code = """
str empty = ""
arr chars = arr(empty)
print int(chars)
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

    def test_arr_preserves_list_reference(self):
        """def main() {\n    Test that arr(list) returns the same list.\n}"""
        code = """
arr original = [1, 2, 3]
arr copy = arr(original)
print int(copy)
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3

    def test_map_preserves_dict_reference(self):
        """def main() {\n    Test that map(dict) returns the same dict.\n}"""
        code = """
map original = {"a": 1, "b": 2}
map copy = map(original)
print int(copy)
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2

    def test_arr_string_with_spaces(self):
        """def main() {\n    Test that arr(str) handles strings with spaces.\n}"""
        code = """
str phrase = "hi there"
arr chars = arr(phrase)
print chars[2]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print space character

    def test_map_arr_with_mixed_types(self):
        """def main() {\n    Test that map(arr) works with arrays containing mixed types.\n}"""
        code = """
arr mixed = [42, "text", 3.14]
map result = map(mixed)
print result["1"]
print result["2"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 42, text

    def test_chained_casting_arr_to_map_to_arr(self):
        """def main() {\n    Test chaining conversions: arr -> map -> arr.\n}"""
        code = """
arr original = [10, 20, 30]
map as_map = map(original)
arr back_to_arr = arr(as_map)
print int(back_to_arr)
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3 (three values)

    def test_casting_in_expressions(self):
        """def main() {\n    Test using casting in arithmetic expressions.\n}"""
        code = """
arr items = [1, 2, 3, 4, 5]
int double_length = int(items) * 2
print double_length
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 10

    def test_float_casting_in_division(self):
        """def main() {\n    Test using flt(arr) in division.\n}"""
        code = """
arr data = [1, 2, 3, 4]
flt average = 10 / flt(data)
print average
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2.5

    def test_arr_of_arr(self):
        """def main() {\n    Test arr() on nested arrays.\n}"""
        code = """
arr nested = [[1, 2], [3, 4]]
int length = int(nested)
print length
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2

    def test_map_arr_single_element(self):
        """def main() {\n    Test map(arr) with a single element.\n}"""
        code = """
arr single = [999]
map result = map(single)
print result["1"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 999


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

