"""
Test suite for the map type (Python dict) in Lyric.

Tests:
- map type declarations and assignments
- Key/value access operations
- Key/value updates
- Iteration over map
- Type compatibility and validation
"""

import pytest
import sys
import io
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import TypeErrorLyric, KeyErrorLyric, RuntimeErrorLyric


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


class TestMapType:
    """def main() {\n    Test the map type in Lyric.\n}"""

    def _run_code(self, code: str):
        """def main() {\n    Helper function to tokenize, parse, and run code.\n}"""
        ast = parse(code, interactive=True)
        return evaluate(ast)

    def test_map_declaration_empty_dict(self):
        """def main() {\n    Test map declaration with empty dictionary.\n}"""
        code = """
map mydict = {}
print mydict
"""
        result = self._run_code(code)
        # Should print {}

    def test_map_declaration_with_pairs(self):
        """def main() {\n    Test map declaration with key-value pairs.\n}"""
        code = """
map person = {"name": "Alice", "age": 30, "city": "NYC"}
print person
"""
        result = self._run_code(code)
        # Should print the dictionary

    def test_map_key_access_string_key(self):
        """def main() {\n    Test accessing map values with string keys.\n}"""
        code = """
map data = {"x": 10, "y": 20}
print data["x"]
print data["y"]
"""
        result = self._run_code(code)
        # Should print 10, 20

    def test_map_key_access_int_key(self):
        """def main() {\n    Test accessing map values with integer keys.\n}"""
        code = """
map numbers = {1: "one", 2: "two", 3: "three"}
print numbers[1]
print numbers[2]
"""
        result = self._run_code(code)
        # Should print one, two

    def test_map_key_access_missing_key(self):
        """def main() {\n    Test accessing non-existent key raises KeyError.\n}"""
        code = """
map data = {"a": 1, "b": 2}
print data["c"]
"""
        with pytest.raises(KeyErrorLyric):
            self._run_code(code)

    def test_map_key_assignment_new(self):
        """def main() {\n    Test adding new key-value pair to map.\n}"""
        code = """
map data = {"x": 10}
data["y"] = 20
print data["y"]
"""
        result = self._run_code(code)
        # Should print 20

    def test_map_key_assignment_update(self):
        """def main() {\n    Test updating existing key in map.\n}"""
        code = """
map scores = {"alice": 85, "bob": 90}
scores["alice"] = 95
print scores["alice"]
"""
        result = self._run_code(code)
        # Should print 95

    def test_map_mixed_key_types(self):
        """def main() {\n    Test map with mixed key types.\n}"""
        code = """
map mixed = {"name": "Alice", 1: "first", 2.5: "two-and-half"}
print mixed["name"]
print mixed[1]
print mixed[2.5]
"""
        result = self._run_code(code)
        # Should print Alice, first, two-and-half

    def test_map_mixed_value_types(self):
        """def main() {\n    Test map with mixed value types.\n}"""
        code = """
map data = {"count": 42, "name": "test", "active": true, "items": [1, 2, 3]}
print data["count"]
print data["name"]
print data["active"]
"""
        result = self._run_code(code)
        # Should print values

    def test_map_nested_dict(self):
        """def main() {\n    Test map with nested dictionary structure.\n}"""
        code = """
map person = {"name": "Alice", "address": {"city": "NYC", "zip": "10001"}}
print person["name"]
print person["address"]["city"]
"""
        result = self._run_code(code)
        # Should print Alice, NYC

    def test_map_iteration_keys(self):
        """def main() {\n    Test iterating over map yields keys.\n}"""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
var key
for key in data:
    print key
done
"""
        result = self._run_code(code)
        # Should print a, b, c

    def test_map_type_validation_strict(self):
        """def main() {\n    Test map type validation rejects non-dict values.\n}"""
        code = """
map mydict = 42
"""
        with pytest.raises(RuntimeErrorLyric):
            self._run_code(code)

    def test_map_type_validation_list(self):
        """def main() {\n    Test map type validation rejects list values.\n}"""
        code = """
map mydict = [1, 2, 3]
"""
        with pytest.raises(RuntimeErrorLyric):
            self._run_code(code)

    def test_map_type_validation_string(self):
        """def main() {\n    Test map type validation rejects string values.\n}"""
        code = """
map mydict = "not a dict"
"""
        with pytest.raises(RuntimeErrorLyric):
            self._run_code(code)

    def test_map_empty_dict_iteration(self):
        """def main() {\n    Test iterating over empty map.\n}"""
        code = """
map empty = {}
var key
for key in empty:
    print key
done
print "done"
"""
        result = self._run_code(code)
        # Should only print "done"

    def test_map_with_list_values(self):
        """def main() {\n    Test map containing list values.\n}"""
        code = """
map data = {"numbers": [1, 2, 3], "names": ["alice", "bob"]}
print data["numbers"][0]
print data["names"][1]
"""
        result = self._run_code(code)
        # Should print 1, bob

    def test_map_in_function_parameter(self):
        """def main() {\n    Test passing map as function parameter.\n}"""
        code = """
def print_keys(map data) {
    var key
    for key in data:
        print key
    done
}

map mydata = {"x": 1, "y": 2}
print_keys(mydata)
"""
        result = self._run_code(code)
        # Should print x, y

    def test_map_in_function_return(self):
        """def main() {\n    Test returning map from function.\n}"""
        code = """
map get_dict() {
    return {"status": "ok", "code": 200}
}

map result = get_dict()
print result["status"]
"""
        result = self._run_code(code)
        # Should print ok

    def test_map_len_builtin(self):
        """def main() {\n    Test using len() method with map.\n}"""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
print data.len()
"""
        result = self._run_code(code)
        # Should print 3

    def test_map_multiple_assignments(self):
        """def main() {\n    Test multiple key assignments in sequence.\n}"""
        code = """
map config = {}
config["host"] = "localhost"
config["port"] = 8080
config["debug"] = true
print config["host"]
print config["port"]
print config["debug"]
"""
        result = self._run_code(code)
        # Should print localhost, 8080, true

    def test_map_overwrite_value(self):
        """def main() {\n    Test overwriting existing values multiple times.\n}"""
        code = """
map counter = {"count": 0}
counter["count"] = 1
counter["count"] = 2
counter["count"] = 3
print counter["count"]
"""
        result = self._run_code(code)
        # Should print 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

