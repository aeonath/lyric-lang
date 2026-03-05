# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for the obj type — Sprint 10 Task 5.

obj is a primitive type in Lyric for holding class instances, similar to how
int, str, arr, and map are primitive types for their respective values.

Valid usage:
  obj account = BankAccount(100)

var continues to work for dynamic typing and is unaffected.
"""

import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


def parse(source: str, interactive: bool = False):
    tokens = tokenize(source)
    parser = Parser(tokens)
    if interactive:
        parser._interactive_mode = True
        parser.is_top_level = False
    return parser.parse()


def run(source: str):
    ast = parse(source, interactive=True)
    interp = Interpreter()
    interp.evaluate(ast)
    return interp


# ---------------------------------------------------------------------------
# Positive tests — obj type must work correctly
# ---------------------------------------------------------------------------

class TestObjTypeBasic:

    def test_obj_declaration_and_method_call(self):
        """obj variable can hold a class instance and call methods."""
        code = """
class BankAccount
    def init(balance) {
        self.balance = balance
    }
    def get_balance() {
        return self.balance
    }
+++
obj account = BankAccount(500)
int result = account.get_balance()
"""
        interp = run(code)
        assert interp.global_scope.get('result') == 500

    def test_obj_method_modifies_state(self):
        """Methods called on an obj variable correctly modify instance state."""
        code = """
class BankAccount
    def init(balance) {
        self.balance = balance
    }
    def deposit(amount) {
        self.balance = self.balance + amount
    }
    def get_balance() {
        return self.balance
    }
+++
obj account = BankAccount(100)
account.deposit(50)
account.deposit(25)
int result = account.get_balance()
"""
        interp = run(code)
        assert interp.global_scope.get('result') == 175

    def test_obj_instance_variable_access(self):
        """Instance variables on obj-typed variables are accessible via dot notation."""
        code = """
class Point
    def init(x, y) {
        self.x = x
        self.y = y
    }
+++
obj p = Point(3, 7)
int px = p.x
int py = p.y
"""
        interp = run(code)
        assert interp.global_scope.get('px') == 3
        assert interp.global_scope.get('py') == 7

    def test_multiple_obj_variables(self):
        """Multiple obj variables can hold different class instances independently."""
        code = """
class Counter
    def init(start) {
        self.count = start
    }
    def increment() {
        self.count = self.count + 1
    }
    def get() {
        return self.count
    }
+++
obj c1 = Counter(0)
obj c2 = Counter(10)
c1.increment()
c1.increment()
c2.increment()
int r1 = c1.get()
int r2 = c2.get()
"""
        interp = run(code)
        assert interp.global_scope.get('r1') == 2
        assert interp.global_scope.get('r2') == 11

    def test_obj_with_string_methods(self):
        """obj variable works correctly when methods return strings."""
        code = """
class Greeter
    def init(name) {
        self.name = name
    }
    def greet() {
        return "Hello, " + self.name + "!"
    }
+++
obj g = Greeter("Alice")
str msg = g.greet()
"""
        interp = run(code)
        assert interp.global_scope.get('msg') == "Hello, Alice!"

    def test_obj_with_inheritance(self):
        """obj variable can hold a subclass instance and call overridden methods."""
        code = """
class Animal
    def init(name) {
        self.name = name
    }
    def speak() {
        return self.name + " makes a sound"
    }
+++

class Dog extends Animal
    def init(name) {
        self.name = name
    }
    def speak() {
        return self.name + " says woof"
    }
+++
obj d = Dog("Rex")
str result = d.speak()
"""
        interp = run(code)
        assert interp.global_scope.get('result') == "Rex says woof"

    def test_obj_reassignment_to_new_instance(self):
        """An obj variable can be reassigned to a new instance of the same class."""
        code = """
class Box
    def init(value) {
        self.value = value
    }
    def get() {
        return self.value
    }
+++
obj b = Box(1)
b = Box(99)
int result = b.get()
"""
        interp = run(code)
        assert interp.global_scope.get('result') == 99

    def test_obj_returned_from_function(self):
        """A function that returns a class instance can be stored in an obj variable."""
        code = """
class Token
    def init(kind, value) {
        self.kind = kind
        self.value = value
    }
    def get_value() {
        return self.value
    }
+++

def make_token(k, v) {
    obj t = Token(k, v)
    return t
}
obj tok = make_token("num", 42)
int result = tok.get_value()
"""
        interp = run(code)
        assert interp.global_scope.get('result') == 42

    def test_obj_in_main_function(self):
        """obj variable works correctly inside a main() function."""
        code = """
class Accumulator
    def init() {
        self.total = 0
    }
    def add(n) {
        self.total = self.total + n
    }
    def get() {
        return self.total
    }
+++

def main() {
    obj acc = Accumulator()
    acc.add(10)
    acc.add(20)
    acc.add(5)
    return acc.get()
}
"""
        ast = parse(code)
        from lyric.interpreter import evaluate
        result = evaluate(ast)
        assert result == 35


# ---------------------------------------------------------------------------
# Regression tests — var continues to work unchanged
# ---------------------------------------------------------------------------

class TestVarRegressionWithObjType:

    def test_var_still_holds_class_instance(self):
        """var can still hold a class instance after obj is introduced."""
        code = """
class Circle
    def init(radius) {
        self.radius = radius
    }
    def area() {
        return self.radius * self.radius
    }
+++
var c = Circle(5)
int result = c.area()
"""
        interp = run(code)
        assert interp.global_scope.get('result') == 25

    def test_var_holds_mixed_types(self):
        """var continues to accept any type (int, str, class instance)."""
        code = """
var x = 42
var y = "hello"
var z = 3.14
"""
        interp = run(code)
        assert interp.global_scope.get('x') == 42
        assert interp.global_scope.get('y') == "hello"
        assert abs(interp.global_scope.get('z') - 3.14) < 0.001


# ---------------------------------------------------------------------------
# Negative tests — type enforcement for obj
# ---------------------------------------------------------------------------

class TestObjTypeEnforcement:

    def test_obj_rejects_int(self):
        """Assigning an int to an obj variable raises a type error."""
        code = """
obj x = 42
"""
        with pytest.raises(RuntimeErrorLyric):
            run(code)

    def test_obj_rejects_str(self):
        """Assigning a str to an obj variable raises a type error."""
        code = """
obj x = "hello"
"""
        with pytest.raises(RuntimeErrorLyric):
            run(code)

    def test_obj_rejects_arr(self):
        """Assigning an arr to an obj variable raises a type error."""
        code = """
obj x = [1, 2, 3]
"""
        with pytest.raises(RuntimeErrorLyric):
            run(code)

    def test_obj_rejects_map(self):
        """Assigning a map to an obj variable raises a type error."""
        code = """
obj x = {1: 2}
"""
        with pytest.raises(RuntimeErrorLyric):
            run(code)

    def test_obj_rejects_float(self):
        """Assigning a float to an obj variable raises a type error."""
        code = """
obj x = 3.14
"""
        with pytest.raises(RuntimeErrorLyric):
            run(code)

    def test_obj_rejects_bool(self):
        """Assigning a bool to an obj variable raises a type error."""
        code = """
obj x = true
"""
        with pytest.raises(RuntimeErrorLyric):
            run(code)
