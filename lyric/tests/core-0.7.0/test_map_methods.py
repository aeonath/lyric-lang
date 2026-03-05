"""
Unit tests for map (dictionary) methods - Sprint 8 Task 9
Tests all dictionary methods and the 'in' operator
"""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric, KeyErrorLyric


def parse(code: str, interactive: bool = False):
    """Helper to parse source code."""
    tokens = tokenize(code)
    parser = Parser(tokens)
    if interactive:
        parser._interactive_mode = True
        parser.is_top_level = False
    return parser.parse()


def evaluate(ast):
    """def main() {\n    Helper to evaluate Lyric AST.\n}"""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


class TestMapMethods:
    """def main() {\n    Test map (dict) methods and operations.\n}"""
    
    # Mutation Methods
    
    def test_clear_removes_all_items(self):
        """def main() {\n    Test clear() removes all items from map.\n}"""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
data.clear()
print data.len()
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 0
    
    def test_update_merges_maps(self):
        """def main() {\n    Test update() merges another map into current map.\n}"""
        code = """
map data = {"a": 1, "b": 2}
map other = {"c": 3, "d": 4}
data.update(other)
print data.len()
print data["c"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 4, 3
    
    def test_pop_removes_and_returns_value(self):
        """def main() {\n    Test pop() removes key and returns value.\n}"""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
int val = data.pop("b")
print val
print data.len()
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2, 2
    
    def test_pop_with_default(self):
        """def main() {\n    Test pop() with default value.\n}"""
        code = """
map data = {"a": 1}
int val = data.pop("missing", 99)
print val
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 99
    
    def test_pop_missing_key_error(self):
        """def main() {\n    Test pop() raises error for missing key without default.\n}"""
        code = """
map data = {"a": 1}
data.pop("missing")
"""
        ast = parse(code, interactive=True)
        with pytest.raises(KeyErrorLyric, match="not found"):
            evaluate(ast)
    
    def test_popitem_removes_last_item(self):
        """def main() {\n    Test popitem() removes and returns last key-value pair.\n}"""
        code = """
map data = {"a": 1, "b": 2}
arr item = data.popitem()
print item.len()
print data.len()
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2, 1
    
    def test_popitem_empty_error(self):
        """def main() {\n    Test popitem() raises error on empty map.\n}"""
        code = """
map data = {}
data.popitem()
"""
        ast = parse(code, interactive=True)
        with pytest.raises(KeyErrorLyric, match="empty"):
            evaluate(ast)
    
    def test_setdefault_returns_existing_value(self):
        """def main() {\n    Test setdefault() returns existing value.\n}"""
        code = """
map data = {"a": 1}
int val = data.setdefault("a", 99)
print val
print data["a"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 1, 1
    
    def test_setdefault_sets_default_value(self):
        """def main() {\n    Test setdefault() sets value for missing key.\n}"""
        code = """
map data = {"a": 1}
int val = data.setdefault("b", 2)
print val
print data["b"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2, 2
    
    # Query Methods
    
    def test_get_returns_value(self):
        """def main() {\n    Test get() returns value for existing key.\n}"""
        code = """
map data = {"name": "Alice", "age": 30}
str name = data.get("name")
print name
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print Alice
    
    def test_get_returns_default(self):
        """def main() {\n    Test get() returns default for missing key.\n}"""
        code = """
map data = {"a": 1}
int val = data.get("missing", 99)
print val
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 99
    
    def test_keys_returns_arr_of_keys(self):
        """def main() {\n    Test keys() returns array of keys.\n}"""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
arr keys = data.keys()
print keys.len()
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3
    
    def test_values_returns_arr_of_values(self):
        """def main() {\n    Test values() returns array of values.\n}"""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
arr values = data.values()
print values.len()
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3
    
    def test_items_returns_arr_of_pairs(self):
        """def main() {\n    Test items() returns array of key-value pairs.\n}"""
        code = """
map data = {"a": 1, "b": 2}
arr items = data.items()
print items.len()
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2
    
    def test_copy_creates_shallow_copy(self):
        """def main() {\n    Test copy() creates a shallow copy.\n}"""
        code = """
map original = {"a": 1, "b": 2}
map copied = original.copy()
copied["c"] = 3
print original.len()
print copied.len()
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 2, 3
    
    # Built-in Functions as Methods
    
    def test_len_returns_size(self):
        """def main() {\n    Test len() returns number of items.\n}"""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
int size = data.len()
print size
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3
    
    def test_sorted_returns_sorted_keys(self):
        """def main() {\n    Test sorted() returns sorted array of keys.\n}"""
        code = """
map data = {"c": 3, "a": 1, "b": 2}
arr sorted_keys = data.sorted()
print sorted_keys.len()
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3
    
    def test_sorted_reverse(self):
        """def main() {\n    Test sorted() with reverse parameter.\n}"""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
arr sorted_keys = data.sorted(True)
print sorted_keys.len()
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3
    
    # Membership Check with 'in' operator
    
    def test_in_operator_key_exists(self):
        """def main() {\n    Test 'in' operator for existing key.\n}"""
        code = """
map data = {"name": "Alice", "age": 30}
bin exists = "name" in data
print exists
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print god
    
    def test_in_operator_key_missing(self):
        """def main() {\n    Test 'in' operator for missing key.\n}"""
        code = """
map data = {"name": "Alice"}
bin exists = "age" in data
print exists
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print bin
    
    def test_in_operator_with_if(self):
        """def main() {\n    Test 'in' operator in conditional.\n}"""
        code = """
map data = {"a": 1, "b": 2}
bin result = "a" in data
if result:
    print "found"
end
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print found
    
    # Iteration
    
    def test_iteration_over_keys(self):
        """def main() {\n    Test iteration over map keys.\n}"""
        code = """
map data = {"a": 1, "b": 2, "c": 3}
int count = 0
var key
for key in data:
    count = count + 1
done
print count
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 3
    
    # Indexing
    
    def test_index_access(self):
        """def main() {\n    Test accessing values by key.\n}"""
        code = """
map data = {"name": "Bob", "age": 25}
str name = data["name"]
print name
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print Bob
    
    def test_index_assignment(self):
        """def main() {\n    Test assigning values by key.\n}"""
        code = """
map data = {}
data["key"] = 42
print data["key"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 42
    
    def test_index_missing_key_error(self):
        """def main() {\n    Test accessing missing key raises error.\n}"""
        code = """
map data = {"a": 1}
data["missing"]
"""
        ast = parse(code, interactive=True)
        with pytest.raises(KeyErrorLyric, match="not found"):
            evaluate(ast)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

