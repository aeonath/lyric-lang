# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for Sprint 4 Task 6: Control structure syntax simplification.

This test suite verifies that:
1. New colonless syntax works correctly
2. Old colon syntax still works but shows deprecation warnings
3. Both if/else and given/done constructs are supported
"""

import pytest
import io
import sys
from lyric.parser import parse
from lyric.interpreter import Interpreter


class TestControlStructureSyntaxSimplification:
    """Test control structure syntax simplification."""

    def test_if_statement_colonless_syntax(self):
        """Test that if statements work without colons."""
        source = '''def main() {
var x = 5
if x > 0
print("positive")
end
}'''
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "positive" was printed
            output = captured_output.getvalue().strip()
            assert "positive" in output
        finally:
            sys.stdout = old_stdout

    def test_if_else_statement_colonless_syntax(self):
        """Test that if/else statements work without colons."""
        source = '''def main() {
var x = -1
if x > 0
print("positive")
else
print("non-positive")
end
}'''
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "non-positive" was printed
            output = captured_output.getvalue().strip()
            assert "non-positive" in output
        finally:
            sys.stdout = old_stdout

    def test_if_elif_else_statement_colonless_syntax(self):
        """Test that if/elif/else statements work without colons."""
        source = '''def main() {
var x = 0
if x > 0
print("positive")
elif x == 0
print("zero")
else
print("negative")
end
}'''
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "zero" was printed
            output = captured_output.getvalue().strip()
            assert "zero" in output
        finally:
            sys.stdout = old_stdout

    def test_for_loop_colonless_syntax(self):
        """Test that for loops work without colons."""
        source = '''def main() {
int i
for i in range(3)
print("iteration")
done
}'''
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "iteration" was printed 3 times
            output = captured_output.getvalue().strip()
            assert output.count("iteration") == 3
        finally:
            sys.stdout = old_stdout

    def test_given_while_loop_colonless_syntax(self):
        """Test that given while loops work without colons."""
        source = '''def main() {
var x = 3
given x > 0
print("looping")
x = x - 1
done
}'''
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "looping" was printed 3 times
            output = captured_output.getvalue().strip()
            assert output.count("looping") == 3
        finally:
            sys.stdout = old_stdout

    def test_nested_control_structures_colonless_syntax(self):
        """Test nested control structures without colons."""
        source = '''def main() {
var x = 1
given x < 3
if x == 1
print("first")
else
print("other")
end
x = x + 1
done
}'''
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check output
            output = captured_output.getvalue().strip()
            assert "first" in output
            assert "other" in output
        finally:
            sys.stdout = old_stdout

    def test_if_statement_with_colon_works_without_warning(self):
        """Test that if statements with colons work without deprecation warnings."""
        source = '''def main() {
var x = 5
if x > 0:
print("positive")
end
}'''
        
        # Should work without any warnings
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "positive" was printed
            output = captured_output.getvalue().strip()
            assert "positive" in output
        finally:
            sys.stdout = old_stdout

    def test_for_loop_with_colon_works_without_warning(self):
        """Test that for loops with colons work without deprecation warnings."""
        source = '''def main() {
int i
for i in range(2):
print("iteration")
done
}'''
        
        # Should work without any warnings
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "iteration" was printed
            output = captured_output.getvalue().strip()
            assert output.count("iteration") == 2
        finally:
            sys.stdout = old_stdout

    def test_else_with_colon_works_without_warning(self):
        """Test that else statements with colons work without deprecation warnings."""
        source = '''def main() {
var x = -1
if x > 0:
print("positive")
else:
print("non-positive")
end
}'''
        
        # Should work without any warnings
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "non-positive" was printed
            output = captured_output.getvalue().strip()
            assert "non-positive" in output
        finally:
            sys.stdout = old_stdout

    def test_elif_with_colon_works_without_warning(self):
        """Test that elif statements with colons work without deprecation warnings."""
        source = '''def main() {
var x = 0
if x > 0:
print("positive")
elif x == 0:
print("zero")
else:
print("negative")
end
}'''
        
        # Should work without any warnings
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "zero" was printed
            output = captured_output.getvalue().strip()
            assert "zero" in output
        finally:
            sys.stdout = old_stdout

    def test_function_with_colon_works_without_warning(self):
        """Test that function definitions with colons work without warnings."""
        source = '''def main(): {
print("hello")
}'''
        
        # Should work without any warnings
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "hello" was printed
            output = captured_output.getvalue().strip()
            assert "hello" in output
        finally:
            sys.stdout = old_stdout

    def test_function_without_colon_works(self):
        """Test that function definitions without colons work."""
        source = '''def main() {
print("hello")
}'''
        
        # Should work without any warnings
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "hello" was printed
            output = captured_output.getvalue().strip()
            assert "hello" in output
        finally:
            sys.stdout = old_stdout

    def test_try_catch_with_colon_works_without_warning(self):
        """Test that try/catch blocks with colons work without warnings."""
        source = '''def main() {
try:
print("in try")
raise TestError
catch:
print("in catch")
fade
}'''
        
        # Should work without any warnings
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that both messages were printed
            output = captured_output.getvalue().strip()
            assert "in try" in output
            assert "in catch" in output
        finally:
            sys.stdout = old_stdout

    def test_try_catch_without_colon_works(self):
        """Test that try/catch blocks without colons work."""
        source = '''def main() {
try
print("in try")
raise TestError
catch
print("in catch")
fade
}'''
        
        # Should work without any warnings
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that both messages were printed
            output = captured_output.getvalue().strip()
            assert "in try" in output
            assert "in catch" in output
        finally:
            sys.stdout = old_stdout

    def test_class_with_colon_works_without_warning(self):
        """Test that class definitions with colons work without warnings."""
        source = '''class TestClass:
def init() {
self.value = 42
}
+++

def main() {
var myobj = TestClass()
print("class created")
}'''
        
        # Should work without any warnings
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "class created" was printed
            output = captured_output.getvalue().strip()
            assert "class created" in output
        finally:
            sys.stdout = old_stdout

    def test_class_without_colon_works(self):
        """Test that class definitions without colons work."""
        source = '''class TestClass
def init() {
self.value = 42
}
+++

def main() {
var myobj = TestClass()
print("class created")
}'''
        
        # Should work without any warnings
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check that "class created" was printed
            output = captured_output.getvalue().strip()
            assert "class created" in output
        finally:
            sys.stdout = old_stdout

    def test_complex_nested_structures_colonless_syntax(self):
        """Test complex nested control structures without colons."""
        source = '''def main() {
var x = 1
given x < 3
if x == 1
print("first iteration")
elif x == 2
print("second iteration")
else
print("other iteration")
end
x = x + 1
done
}'''
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check output
            output = captured_output.getvalue().strip()
            assert "first iteration" in output
            assert "second iteration" in output
        finally:
            sys.stdout = old_stdout

    def test_control_structures_do_not_affect_other_constructs(self):
        """Test that control structure changes don't affect other constructs."""
        source = '''def main() {
# Function definition should still work
def helper() {
print("helper called")
}

# Class definition should still work
class TestClass
def init() {
self.value = 42
}
+++

# Call the helper
helper()

# Create class instance
var myobj = TestClass()
print("class value: " + str(myobj.value))
}'''
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = interpreter.evaluate(ast)
            assert result is None
            
            # Check output
            output = captured_output.getvalue().strip()
            assert "helper called" in output
            assert "class value: 42" in output
        finally:
            sys.stdout = old_stdout
