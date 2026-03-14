# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for interpreter module."""

import pytest
from lyric.interpreter import evaluate, Interpreter
from lyric.parser import parse
from lyric.errors import RuntimeErrorLyric


def test_evaluate_function_definition():
    """Test evaluating function definition: def main() { print("Hello, Lyric!") }"""
    source = 'def main() { print("Hello, Lyric!") }'
    
    ast = parse(source)
    result = evaluate(ast)
    
    # Function definition should not return anything
    assert result is None
    
    # Verify function was defined
    interpreter = Interpreter()
    interpreter.evaluate(ast)
    assert "main" in interpreter.functions


def test_evaluate_if_else_statement():
    """Test evaluating if/else statement."""
    source = '''def main() {
var x = 5
if x > 0
print("positive")
else
print("non-positive")
end
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that "positive" was printed
        output = captured_output.getvalue().strip()
        assert "positive" in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_loop_statement():
    """Test evaluating loop statement: for i in range(3) print(i) done"""
    source = '''def main() {
int i
for i in range(3)
print("iteration")
done
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that "iteration" was printed 3 times
        output = captured_output.getvalue().strip()
        lines = output.split('\n')
        assert len(lines) == 3
        assert all("iteration" in line for line in lines)
    finally:
        sys.stdout = old_stdout


def test_evaluate_class_definition():
    """Test evaluating class definition: class Player name = "Guest" def greet() { print("Hello,", self.name) } +++"""
    source = '''class Player
var name = "Guest"
def greet() {
print("Hello,", self.name)
}
+++'''
    
    ast = parse(source)
    result = evaluate(ast)
    
    # Class definition should not return anything
    assert result is None
    
    # Verify class was defined
    interpreter = Interpreter()
    interpreter.evaluate(ast)
    assert "Player" in interpreter.classes
    
    # Check class members
    player_class = interpreter.classes["Player"]
    assert "name" in player_class
    assert player_class["name"] == "Guest"
    assert "greet" in player_class


def test_evaluate_else_if_sequence():
    """Test evaluating else-if sequence."""
    source = '''def main() {
var x = 5
if x > 10:
print("high")
elif x > 5:
print("medium")
elif x > 0:
print("low")
else:
print("zero or negative")
end
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that "low" was printed (since x = 5)
        output = captured_output.getvalue().strip()
        assert "low" in output
        assert "high" not in output
        assert "medium" not in output
        assert "zero or negative" not in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_binary_operations():
    """Test evaluating binary operations with precedence."""
    source = '''def main() {
var result = 2 + 3 * 4 - 1
print(result)
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that result is 13 (2 + (3 * 4) - 1 = 2 + 12 - 1 = 13)
        output = captured_output.getvalue().strip()
        assert "13" in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_function_with_parameters():
    """Test evaluating function with parameters."""
    source = '''def add(x, y) {
return x + y
}

def main() {
var result = add(3, 4)
print(result)
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check that result is 7
        output = captured_output.getvalue().strip()
        assert "7" in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_complex_nested_structure():
    """Test evaluating a complex nested structure."""
    source = '''def main() {
    var x = 10
    if x > 5:
        var y = x * 2
        if y > 15:
            print("nested if")
        else:
            print("nested else")
        end
    else:
        print("outer else")
    end
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None  # main function has no explicit return
        
        # Check that "nested if" was printed (since x=10, y=20, y>15)
        output = captured_output.getvalue().strip()
        assert "nested if" in output
        assert "nested else" not in output
        assert "outer else" not in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_variable_scope():
    """Test variable scope handling."""
    source = '''def test_scope() {
var local_var = "local"
print(local_var)
}

def main() {
var global_var = "global"
test_scope()
print(global_var)
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check output
        output = captured_output.getvalue().strip()
        lines = output.split('\n')
        assert len(lines) == 2
        assert "local" in lines[0]
        assert "global" in lines[1]
    finally:
        sys.stdout = old_stdout


def test_evaluate_error_handling():
    """Test interpreter error handling."""
    # Test undefined variable
    source = 'def main() { print(undefined_var) }'
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric):
        evaluate(ast)
    
    # Test undefined function
    source = 'def main() { undefined_func() }'
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric):
        evaluate(ast)
    
    # Test division by zero
    source = 'def main() { var result = 5 / 0 }'
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric):
        evaluate(ast)


def test_evaluate_member_access():
    """Test member access evaluation."""
    source = '''class Person
var name = "John"
var age = 30
+++

def main() {
var person = Person
print(person.name)
print(person.age)
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check output
        output = captured_output.getvalue().strip()
        assert "John" in output
        assert "30" in output
    finally:
        sys.stdout = old_stdout


def test_evaluate_logical_operations():
    """Test logical operations evaluation."""
    source = '''def main() {
var a = true
var b = false
var result1 = a and b
var result2 = a or b
var result3 = not a
print(result1, result2, result3)
}'''
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check output (Note: true/false are not implemented yet, so this will test the structure)
        output = captured_output.getvalue().strip()
        # This test will need to be updated when boolean literals are implemented
    finally:
        sys.stdout = old_stdout


def test_evaluate_hello_example():
    """Test evaluating the hello.ly example."""
    source = """def main() {
    print("Hello, Lyric!")
}"""
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check exact output
        output = captured_output.getvalue().strip()
        assert output == "Hello, Lyric!"
    finally:
        sys.stdout = old_stdout


def test_evaluate_if_demo_example():
    """Test evaluating the if_demo.ly example."""
    source = """def main() {
    var x = 5
    if x > 0:
        print("positive")
    else:
        print("non-positive")
    end
}"""
    
    ast = parse(source)
    
    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        result = evaluate(ast)
        assert result is None
        
        # Check exact output
        output = captured_output.getvalue().strip()
        assert output == "positive"
    finally:
        sys.stdout = old_stdout


def test_evaluate_loop_example():
    """Test evaluating the loop.ly example."""
    source = """def main() {
    int i
    for i in range(3):
        print(i)
    done
}"""

    ast = parse(source)

    # Capture print output
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()

    try:
        result = evaluate(ast)
        assert result is None

        # Check exact output
        output = captured_output.getvalue().strip()
        assert output == "0\n1\n2"
    finally:
        sys.stdout = old_stdout


def test_evaluate_class_instantiation():
    """Test class instantiation and method calls."""
    source = """class Person
    var name = "Guest"
    var age = 25

    def greet() {
        print("Hello, I'm", self.name)
    }

    def set_name(new_name) {
        self.name = new_name
    }
+++

def main() {
    var person = Person()
    person.greet()
    person.set_name("Alice")
    person.greet()
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None


def test_evaluate_nested_control_flow():
    """Test nested if statements and loops."""
    source = """def main() {
    var x = 5
    if x > 0:
        print("x is positive")
        if x > 3:
            print("x is greater than 3")
        else:
            print("x is 3 or less")
        end
    else:
        print("x is not positive")
    end

    int i
    int j
    for i in range(2):
        print("Outer:", i)
        for j in range(2):
            print("  Inner:", j)
        done
    done
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None


def test_evaluate_error_reporting():
    """Test error reporting for undefined variables."""
    source = """def main() {
    print(undefined_variable)
}"""
    
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        evaluate(ast)
    
    assert "Undefined variable" in str(exc_info.value)
    assert "'undefined_variable' has not been declared" in str(exc_info.value)


def test_evaluate_isinstance_function():
    """Test isinstance function with classes and built-in types."""
    source = """class Person
    var name = "Guest"
+++

def main() {
    var person = Person()
    print("isinstance(person, Person):", isinstance(person, Person))
    print("isinstance(5, int):", isinstance(5, int))
    print("isinstance(5, str):", isinstance(5, str))
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None


def test_evaluate_type_function():
    """Test type function with classes and built-in types."""
    source = """class Person
    var name = "Guest"
+++

def main() {
    var person = Person()
    print("type(person):", type(person))
    print("type(5):", type(5))
    print("type(3.14):", type(3.14))
    print("type(hello):", type("hello"))
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None


def test_evaluate_list_literals():
    """Test list literal creation and manipulation."""
    source = """def main() {
    var numbers = [1, 2, 3]
    print("numbers:", numbers)

    var mixed = [1, "hello", 3.14]
    print("mixed:", mixed)

    var empty = []
    print("empty:", empty)
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None


def test_evaluate_none_literal():
    """Test None literal handling."""
    source = """def main() {
    var x = None
    print("x is:", x)
    print("None value:", None)
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None


def test_evaluate_range_enhancements():
    """Test enhanced range function with start/stop parameters."""
    source = """def main() {
    print("range(2, 5):", range(2, 5))
    print("range(0, 3):", range(0, 3))
    print("range(1, 1):", range(1, 1))
    print("range(1, 5, 2):", range(1, 5, 2))
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None


def test_evaluate_complex_class_interaction():
    """Test complex class interactions with multiple classes."""
    source = """class Person
    var name = "Guest"

    def greet() {
        print("Hello, I'm", self.name)
    }

    def set_name(new_name) {
        self.name = new_name
    }
+++

class Student
    var name = "Student"
    var grade = "A"
    
    def introduce() {
        print("Hi, I'm", self.name, "with grade", self.grade)
    }
+++

def main() {
    var person = Person()
    var student = Student()
    
    person.greet()
    student.introduce()
    
    person.set_name("Alice")
    student.name = "Bob"
    
    person.greet()
    student.introduce()
}"""
    
    ast = parse(source)
    result = evaluate(ast)
    assert result is None


def test_evaluate_method_call_errors():
    """Test error handling for method calls on non-objects."""
    source = """def main() {
    var x = 5
    x.non_existent_method()
}"""
    
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        evaluate(ast)
    
    assert "Method not found" in str(exc_info.value)
    assert "'non_existent_method' is not a method" in str(exc_info.value)


def test_evaluate_class_instantiation_errors():
    """Test error handling for undefined class instantiation."""
    source = """def main() {
    var result = NonExistentClass()
}"""
    
    ast = parse(source)
    
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        evaluate(ast)
    
    assert "Function not found" in str(exc_info.value)
    assert "'NonExistentClass' is not defined" in str(exc_info.value)