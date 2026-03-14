# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for inline loop variable declaration.

Allows `for TYPE VAR in EXPR` syntax so the loop variable does not
need to be declared before the loop.

Tests:
- for int i in range(n)
- for var item in [...]
- for str word in [...]
- range with start/end/step
- Type mismatch detection
- Nested inline loops
- Variable persists after loop
- Map iteration with inline var
"""

import pytest
import sys
import io
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
    """Helper to evaluate an AST."""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


def run_code_capture(code: str) -> str:
    """Run code and capture stdout output."""
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        ast = parse(code, interactive=True)
        evaluate(ast)
    finally:
        sys.stdout = old_stdout
    return captured.getvalue()


class TestInlineRangeLoop:
    def test_int_in_range(self):
        """for int i in range(5) should work."""
        code = '''int total = 0
for int i in range(5)
    total += i
done
print(total)'''
        output = run_code_capture(code)
        assert output.strip() == "10"

    def test_int_in_range_start_end(self):
        """for int i in range(2, 5) should work."""
        code = '''int total = 0
for int i in range(2, 5)
    total += i
done
print(total)'''
        output = run_code_capture(code)
        assert output.strip() == "9"

    def test_int_in_range_step(self):
        """for int i in range(0, 10, 2) should work."""
        code = '''int total = 0
for int i in range(0, 10, 2)
    total += i
done
print(total)'''
        output = run_code_capture(code)
        assert output.strip() == "20"

    def test_var_in_range(self):
        """for var i in range(3) should work."""
        code = '''str result = ""
for var i in range(3)
    result += str(i)
done
print(result)'''
        output = run_code_capture(code)
        assert output.strip() == "012"


class TestInlineListLoop:
    def test_var_in_list(self):
        """for var item in [1, 2, 3] should work."""
        code = '''int total = 0
for var item in [1, 2, 3]
    total += item
done
print(total)'''
        output = run_code_capture(code)
        assert output.strip() == "6"

    def test_str_in_list(self):
        """for str word in ["hello", "world"] should work."""
        code = '''str result = ""
for str word in ["hello", "world"]
    result += word + " "
done
print(result)'''
        output = run_code_capture(code)
        assert output.strip() == "hello world"

    def test_int_in_int_list(self):
        """for int n in [10, 20, 30] should work."""
        code = '''int total = 0
for int n in [10, 20, 30]
    total += n
done
print(total)'''
        output = run_code_capture(code)
        assert output.strip() == "60"


class TestInlineMapLoop:
    def test_var_in_map(self):
        """for var key in map should iterate keys."""
        code = '''str result = ""
for var key in {"a": 1, "b": 2, "c": 3}
    result += key
done
print(result)'''
        output = run_code_capture(code)
        assert output.strip() == "abc"

    def test_str_in_map(self):
        """for str key in map should iterate keys with type check."""
        code = '''str result = ""
for str key in {"x": 10, "y": 20}
    result += key + " "
done
print(result)'''
        output = run_code_capture(code)
        assert output.strip() == "x y"


class TestInlineLoopTypeMismatch:
    def test_int_with_string_list(self):
        """for int i in ["a", "b"] should fail with type mismatch."""
        code = '''for int i in ["a", "b"]
    print(i)
done'''
        with pytest.raises(RuntimeErrorLyric):
            ast = parse(code, interactive=True)
            evaluate(ast)


class TestInlineLoopNested:
    def test_nested_inline_loops(self):
        """Nested for loops with inline declarations should work."""
        code = '''int total = 0
for int i in range(3)
    for int j in range(3)
        total += 1
    done
done
print(total)'''
        output = run_code_capture(code)
        assert output.strip() == "9"


class TestInlineLoopVarPersists:
    def test_var_accessible_after_loop(self):
        """Inline-declared variable should persist after the loop."""
        code = '''var x
for int i in range(5)
    x = i
done
print(i)'''
        output = run_code_capture(code)
        assert output.strip() == "4"


class TestExistingSyntaxStillWorks:
    def test_predeclared_var_still_works(self):
        """Old syntax with pre-declared variable should still work."""
        code = '''int total = 0
int i
for i in range(5)
    total += i
done
print(total)'''
        output = run_code_capture(code)
        assert output.strip() == "10"

    def test_predeclared_var_list_still_works(self):
        """Old syntax with pre-declared var for list iteration."""
        code = '''str result = ""
var word
for word in ["hello", "world"]
    result += word + " "
done
print(result)'''
        output = run_code_capture(code)
        assert output.strip() == "hello world"
