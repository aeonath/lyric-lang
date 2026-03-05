"""
Test suite for new function declaration syntax in Lyric (Task 7).

Tests:
- TYPE funcname() syntax for typed functions
- def funcname() syntax for untyped functions
- Return type inference
- Both old and new syntax work
"""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric, ParseError


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


class TestFunctionDeclarationSyntax:
    """def main() {\n    Test new function declaration syntax.\n}"""

    def test_new_syntax_typed_int_function(self):
        """def main() {\n    Test new syntax: int funcname()\n}"""
        code = """
int get_sum(int a, int b) {
    return a + b
}

int result = get_sum(5, 3)
print result
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 8

    def test_new_syntax_typed_str_function(self):
        """def main() {\n    Test new syntax: str funcname()\n}"""
        code = """
str greet(str name) {
    return "Hello, " + name
}

str message = greet("Alice")
print message
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print "Hello, Alice"

    def test_new_syntax_typed_flt_function(self):
        """def main() {\n    Test new syntax: flt funcname()\n}"""
        code = """
flt calculate_average(int a, int b) {
    return (a + b) / 2
}

flt avg = calculate_average(10, 20)
print avg
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 15.0

    def test_new_syntax_untyped_function_with_def(self):
        """def main() {\n    Test that def funcname() still works for untyped functions.\n}"""
        code = """
def say_hello(name) {
    print "Hello, " + name
}

say_hello("Bob")
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print "Hello, Bob"

    def test_new_syntax_typed_map_function(self):
        """def main() {\n    Test new syntax with map return type.\n}"""
        code = """
map create_dict(str key, int value) {
    return {key: value}
}

map data = create_dict("count", 42)
print data["count"]
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 42

    def test_new_syntax_typed_var_function(self):
        """def main() {\n    Test new syntax with var return type.\n}"""
        code = """
var get_value(god condition) {
    if condition:
        return 100
    else:
        return "none"
    end
}

var result1 = get_value(true)
var result2 = get_value(false)
print result1
print result2
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 100, none

    def test_new_syntax_typed_function_with_no_params(self):
        """def main() {\n    Test new syntax with no parameters.\n}"""
        code = """
int get_constant() {
    return 42
}

int value = get_constant()
print value
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 42

    def test_new_syntax_def_function_with_return(self):
        """def main() {\n    Test that def functions can return values.\n}"""
        code = """
def multiply(int a, int b) {
    return a * b
}

int product = multiply(6, 7)
print product
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 42

    def test_new_syntax_def_function_no_return(self):
        """def main() {\n    Test that def functions can have no return (None).\n}"""
        code = """
def print_message(str msg) {
    print msg
}

print_message("Testing")
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print "Testing"

    def test_new_syntax_nested_function_calls(self):
        """def main() {\n    Test new syntax with nested function calls.\n}"""
        code = """
int add(int a, int b) {
    return a + b
}

int multiply(int a, int b) {
    return a * b
}

int result = multiply(add(2, 3), add(4, 6))
print result
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 50 (5 * 10)

    def test_new_syntax_function_with_mixed_param_types(self):
        """def main() {\n    Test new syntax with mixed typed and untyped parameters.\n}"""
        code = """
str format_message(str name, age) {
    return name + " is " + str(age)
}

str message = format_message("Alice", 30)
print message
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print "Alice is 30"

    def test_new_syntax_recursive_function(self):
        """def main() {\n    Test new syntax with recursive function.\n}"""
        code = """
int factorial(int n) {
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
    end
}

int result = factorial(5)
print result
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 120

    def test_old_syntax_rejected(self):
        """Test that old syntax 'int def funcname()' is rejected with a ParseError."""
        code = """
int def add_old_style(int a, int b) {
    return a + b
}
"""
        with pytest.raises(ParseError):
            parse(code, interactive=True)

    def test_new_syntax_with_rex_return_type(self):
        """def main() {\n    Test new syntax with rex return type.\n}"""
        code = """
rex get_pattern(str pattern_str) {
    return regex(pattern_str)
}

rex pattern = get_pattern("[0-9]+")
print pattern.match("123")
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print True

    def test_new_syntax_bin_return_type(self):
        """def main() {\n    Test new syntax with bin (boolean alias) return type.\n}"""
        code = """def main() {\n    
bin is_positive(int n) {
    return n > 0
}

print is_positive(5)
print is_positive(-3)
\n}"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print True, False

    def test_def_function_inference(self):
        """def main() {\n    Test that def functions infer return type or return None.\n}"""
        code = """
def get_number() {
    return 42
}

def get_nothing() {
    print "void function"
}

var num = get_number()
var nothing = get_nothing()
print num
print nothing
"""
        ast = parse(code, interactive=True)
        evaluate(ast)
        # Should print 42, void function, None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
