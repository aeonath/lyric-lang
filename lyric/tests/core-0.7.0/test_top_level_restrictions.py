# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""def main() {\n    Unit tests for top-level statement restrictions.\n}"""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.errors import SyntaxErrorLyric


def test_top_level_variable_declaration_allowed():
    """def main() {\n    Test that variable declarations are allowed at top level.\n}"""
    code = """
int x = 10
str name = "test"

def main() {
    print(x)
}
"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()  # Should not raise


def test_top_level_function_definition_allowed():
    """def main() {\n    Test that function definitions are allowed at top level.\n}"""
    code = """
int add(int a, int b) {
    return a + b
}

def main() {
    print(add(1, 2))
}
"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()  # Should not raise


def test_top_level_class_definition_allowed():
    """def main() {\n    Test that class definitions are allowed at top level.\n}"""
    code = """
class Person
    str name
    
    def Person(str n) {
        self.name = n
    }
+++

def main() {
    obj p = Person("Alice")
    print(p.name)
}
"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()  # Should not raise


def test_top_level_if_statement_not_allowed():
    """def main() {\n    Test that if statements are not allowed at top level.\n}"""
    code = """
int x = 1
if x == 1
    print("hi")
end

def main() {
    print(x)
}
"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    
    with pytest.raises(SyntaxErrorLyric) as exc_info:
        parser.parse()
    
    assert "Control structures not allowed at module level" in str(exc_info.value)


def test_top_level_loop_not_allowed():
    """def main() {\n    Test that loops are not allowed at top level.\n}"""
    code = """
int x = 1
given x < 10:
    x = x + 1
done

def main() {
    print(x)
}
"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    
    with pytest.raises(SyntaxErrorLyric) as exc_info:
        parser.parse()
    
    assert "Control structures not allowed at module level" in str(exc_info.value)


def test_top_level_try_block_not_allowed():
    """def main() {\n    Test that try blocks are not allowed at top level.\n}"""
    code = """
try:
    int x = 10
catch:
    print("error")
fade

def main() {
    print("done")
}
"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    
    with pytest.raises(SyntaxErrorLyric) as exc_info:
        parser.parse()
    
    assert "Control structures not allowed at module level" in str(exc_info.value)


def test_top_level_return_not_allowed():
    """def main() {\n    Test that return statements are not allowed at top level.\n}"""
    code = """
int x = 10
return x

def main() {
    print("done")
}
"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    
    with pytest.raises(SyntaxErrorLyric) as exc_info:
        parser.parse()
    
    assert "'return' statement not allowed at module level" in str(exc_info.value)


def test_top_level_function_call_not_allowed():
    """def main() {\n    Test that function calls are not allowed at top level.\n}"""
    code = """
def helper() {
    return 42
}

helper()

def main() {
    print("done")
}
"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    
    with pytest.raises(SyntaxErrorLyric) as exc_info:
        parser.parse()
    
    assert "Only variable declarations, functions, and classes are allowed at module level" in str(exc_info.value)


def test_top_level_import_allowed():
    """def main() {\n    Test that import statements are allowed at top level.\n}"""
    code = """
import some_module

def main() {
    print("done")
}
"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()  # Should not raise


def test_statements_allowed_inside_functions():
    """def main() {\n    Test that all statements are allowed inside functions.\n}"""
    code = """
int x = 10

def main() {
    if x > 5
        print("big")
    end
    
    given x < 20:
        print("in range")
    done
    
    try:
        var y = x / 2
    catch:
        print("error")
    fade
    
    return 0
}
"""
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()  # Should not raise
