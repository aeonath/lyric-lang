# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for compound assignment operators (+=, -=, *=, /=, %=).

Tests:
- int with all 5 operators
- flt with +=, -=, *=, /=
- str with += (concatenation) and *= (repetition)
- Type errors: str -= 1, str /= 2, str %= 2
- Member compound assignment: self.count += 1
- Index compound assignment: arr[0] += 10
- Chained usage in loops: total += i
- Division by zero with /= and %=
"""

import pytest
import sys
import io
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import TypeErrorLyric, ZeroDivisionErrorLyric, RuntimeErrorLyric


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


# --- Integer compound assignment ---

class TestIntCompoundAssignment:
    def test_plus_assign_int(self):
        code = 'int x = 10\nx += 5\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "15"

    def test_minus_assign_int(self):
        code = 'int x = 10\nx -= 3\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "7"

    def test_multiply_assign_int(self):
        code = 'int x = 4\nx *= 3\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "12"

    def test_divide_assign_int(self):
        code = 'var x = 20\nx /= 4\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "5.0"

    def test_modulo_assign_int(self):
        code = 'int x = 17\nx %= 5\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "2"

    def test_plus_assign_negative(self):
        code = 'int x = 10\nx += -3\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "7"

    def test_multiple_compound_assignments(self):
        code = 'int x = 10\nx += 5\nx -= 3\nx *= 2\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "24"


# --- Float compound assignment ---

class TestFltCompoundAssignment:
    def test_plus_assign_flt(self):
        code = 'flt x = 1.5\nx += 2.5\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "4.0"

    def test_minus_assign_flt(self):
        code = 'flt x = 5.0\nx -= 1.5\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "3.5"

    def test_multiply_assign_flt(self):
        code = 'flt x = 2.5\nx *= 4.0\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "10.0"

    def test_divide_assign_flt(self):
        code = 'flt x = 10.0\nx /= 4.0\nprint(x)'
        output = run_code_capture(code)
        assert output.strip() == "2.5"


# --- String compound assignment ---

class TestStrCompoundAssignment:
    def test_plus_assign_str_concat(self):
        code = 'str s = "hello"\ns += " world"\nprint(s)'
        output = run_code_capture(code)
        assert output.strip() == "hello world"

    def test_multiply_assign_str_repeat(self):
        code = 'str s = "ab"\ns *= 3\nprint(s)'
        output = run_code_capture(code)
        assert output.strip() == "ababab"


# --- Type errors on strings ---

class TestStrCompoundAssignmentErrors:
    def test_minus_assign_str_error(self):
        code = 'str s = "hello"\ns -= 1'
        with pytest.raises((TypeErrorLyric, RuntimeErrorLyric)):
            ast = parse(code, interactive=True)
            evaluate(ast)

    def test_divide_assign_str_error(self):
        code = 'str s = "hello"\ns /= 2'
        with pytest.raises((TypeErrorLyric, RuntimeErrorLyric)):
            ast = parse(code, interactive=True)
            evaluate(ast)

    def test_modulo_assign_str_error(self):
        code = 'str s = "hello"\ns %= 2'
        with pytest.raises((TypeErrorLyric, RuntimeErrorLyric)):
            ast = parse(code, interactive=True)
            evaluate(ast)


# --- Member compound assignment ---

class TestMemberCompoundAssignment:
    def test_member_plus_assign(self):
        code = '''class Counter
    def init() {
        self.count = 0
    }
    def increment() {
        self.count += 1
    }
    def get() {
        return self.count
    }
+++

var c = Counter()
c.increment()
c.increment()
c.increment()
print(c.get())'''
        output = run_code_capture(code)
        assert output.strip() == "3"

    def test_member_multiply_assign(self):
        code = '''class Doubler
    def init() {
        self.value = 1
    }
    def double() {
        self.value *= 2
    }
    def get() {
        return self.value
    }
+++

var d = Doubler()
d.double()
d.double()
d.double()
print(d.get())'''
        output = run_code_capture(code)
        assert output.strip() == "8"


# --- Index compound assignment ---

class TestIndexCompoundAssignment:
    def test_index_plus_assign(self):
        code = 'arr a = [10, 20, 30]\na[0] += 5\nprint(a[0])'
        output = run_code_capture(code)
        assert output.strip() == "15"

    def test_index_multiply_assign(self):
        code = 'arr a = [2, 3, 4]\na[1] *= 10\nprint(a[1])'
        output = run_code_capture(code)
        assert output.strip() == "30"

    def test_index_minus_assign(self):
        code = 'arr a = [100, 200, 300]\na[2] -= 50\nprint(a[2])'
        output = run_code_capture(code)
        assert output.strip() == "250"


# --- Member+index compound assignment ---

class TestMemberIndexCompoundAssignment:
    def test_member_index_plus_assign(self):
        code = '''class Bag
    def init() {
        self.items = {"a": 1, "b": 2}
    }
    def bump(str key) {
        self.items[key] += 10
    }
    def get(str key) {
        return self.items[key]
    }
+++

var bag = Bag()
bag.bump("a")
print(bag.get("a"))'''
        output = run_code_capture(code)
        assert output.strip() == "11"

    def test_member_index_assign(self):
        code = '''class Store
    def init() {
        self.data = {}
    }
    def set(str key, int val) {
        self.data[key] = val
    }
    def get(str key) {
        return self.data[key]
    }
+++

var s = Store()
s.set("x", 42)
print(s.get("x"))'''
        output = run_code_capture(code)
        assert output.strip() == "42"

    def test_member_index_word_counter(self):
        code = '''class Counter
    def init() {
        self.counts = {}
    }
    def add(str word) {
        if word in self.counts
            self.counts[word] += 1
        else
            self.counts[word] = 1
        end
    }
    def get(str word) {
        return self.counts[word]
    }
+++

var wc = Counter()
wc.add("hello")
wc.add("world")
wc.add("hello")
print(wc.get("hello"))
print(wc.get("world"))'''
        output = run_code_capture(code)
        assert output.strip() == "2\n1"


# --- Loop usage ---

class TestLoopCompoundAssignment:
    def test_accumulate_in_loop(self):
        code = '''int total = 0
var i
for i in [1, 2, 3, 4, 5]
    total += i
done
print(total)'''
        output = run_code_capture(code)
        assert output.strip() == "15"

    def test_multiply_in_loop(self):
        code = '''int product = 1
var i
for i in [1, 2, 3, 4, 5]
    product *= i
done
print(product)'''
        output = run_code_capture(code)
        assert output.strip() == "120"

    def test_string_concat_in_loop(self):
        code = '''str result = ""
var word
for word in ["hello", " ", "world"]
    result += word
done
print(result)'''
        output = run_code_capture(code)
        assert output.strip() == "hello world"


# --- Division by zero ---

class TestDivisionByZeroCompound:
    def test_divide_assign_by_zero(self):
        code = 'int x = 10\nx /= 0'
        with pytest.raises((ZeroDivisionErrorLyric, RuntimeErrorLyric)):
            ast = parse(code, interactive=True)
            evaluate(ast)

    def test_modulo_assign_by_zero(self):
        code = 'int x = 10\nx %= 0'
        with pytest.raises((ZeroDivisionErrorLyric, RuntimeErrorLyric)):
            ast = parse(code, interactive=True)
            evaluate(ast)


# --- Lexer token tests ---

class TestCompoundAssignmentTokens:
    def test_plus_assign_token(self):
        tokens = tokenize("x += 5")
        types = [t.type for t in tokens]
        assert 'PLUS_ASSIGN' in types

    def test_minus_assign_token(self):
        tokens = tokenize("x -= 5")
        types = [t.type for t in tokens]
        assert 'MINUS_ASSIGN' in types

    def test_multiply_assign_token(self):
        tokens = tokenize("x *= 5")
        types = [t.type for t in tokens]
        assert 'MULTIPLY_ASSIGN' in types

    def test_divide_assign_token(self):
        tokens = tokenize("x /= 5")
        types = [t.type for t in tokens]
        assert 'DIVIDE_ASSIGN' in types

    def test_percent_assign_token(self):
        tokens = tokenize("x %= 5")
        types = [t.type for t in tokens]
        assert 'PERCENT_ASSIGN' in types

    def test_plus_not_confused_with_plus_assign(self):
        tokens = tokenize("x + 5")
        types = [t.type for t in tokens]
        assert 'PLUS' in types
        assert 'PLUS_ASSIGN' not in types

    def test_triple_plus_not_confused(self):
        tokens = tokenize("+++")
        types = [t.type for t in tokens]
        assert 'CLASS_END' in types
        assert 'PLUS_ASSIGN' not in types
