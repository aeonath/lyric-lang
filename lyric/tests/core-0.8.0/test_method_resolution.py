# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for method resolution and overriding (Sprint 9 Task 3)."""

from lyric.parser import parse
from lyric.interpreter import evaluate
import pytest
import io
import sys


def test_simple_method_override():
    """Test that child method replaces base method with same name."""
    source = """
class Base
    def greet() {
        print("Base greeting")
    }
+++

class Child based on Base
    def greet() {
        print("Child greeting")
    }
+++

def main() {
    var myobj = Child()
    myobj.greet()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Child greeting" in output
        assert "Base greeting" not in output
    finally:
        sys.stdout = old_stdout


def test_method_override_with_same_signature():
    """Test method override with identical parameter signature."""
    source = """
class Animal
    def make_sound(str sound) {
        print("Animal says:", sound)
    }
+++

class Dog based on Animal
    def make_sound(str sound) {
        print("Dog barks:", sound)
    }
+++

def main() {
    var dog = Dog()
    dog.make_sound("woof")
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Dog barks: woof" in output
        assert "Animal says" not in output
    finally:
        sys.stdout = old_stdout


def test_partial_method_override():
    """Test that only overridden methods are replaced, others inherited."""
    source = """
class Base
    def method1() {
        print("Base method1")
    }
    def method2() {
        print("Base method2")
    }
    def method3() {
        print("Base method3")
    }
+++

class Child based on Base
    def method2() {
        print("Child method2")
    }
+++

def main() {
    var myobj = Child()
    myobj.method1()
    myobj.method2()
    myobj.method3()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Base method1" in output
        assert "Child method2" in output
        assert "Base method3" in output
        assert "Base method2" not in output
    finally:
        sys.stdout = old_stdout


def test_method_override_three_levels():
    """Test method override across three levels of inheritance."""
    source = """
class A
    def process() {
        print("A process")
    }
+++

class B based on A
    def process() {
        print("B process")
    }
+++

class C based on B
    def process() {
        print("C process")
    }
+++

def main() {
    var myobj = C()
    myobj.process()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "C process" in output
        assert "B process" not in output
        assert "A process" not in output
    finally:
        sys.stdout = old_stdout


def test_method_override_middle_level():
    """Test method override in middle level of three-level inheritance."""
    source = """
class Grandparent
    def display() {
        print("Grandparent")
    }
+++

class Parent based on Grandparent
    def display() {
        print("Parent")
    }
+++

class Child based on Parent
    var x = 1
+++

def main() {
    var myobj = Child()
    myobj.display()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Parent" in output
        assert "Grandparent" not in output
    finally:
        sys.stdout = old_stdout


def test_method_lookup_depth_one():
    """Test method lookup at depth 1 (direct parent)."""
    source = """
class Parent
    def inherited_method() {
        print("From parent")
    }
+++

class Child based on Parent
    var data = 42
+++

def main() {
    var myobj = Child()
    myobj.inherited_method()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "From parent" in output
    finally:
        sys.stdout = old_stdout


def test_method_lookup_depth_two():
    """Test method lookup at depth 2 (grandparent)."""
    source = """
class Grandparent
    def old_method() {
        print("From grandparent")
    }
+++

class Parent based on Grandparent
    var x = 1
+++

class Child based on Parent
    var y = 2
+++

def main() {
    var myobj = Child()
    myobj.old_method()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "From grandparent" in output
    finally:
        sys.stdout = old_stdout


def test_method_lookup_depth_three():
    """Test method lookup at depth 3 (great-grandparent)."""
    source = """
class A
    def root_method() {
        print("From A")
    }
+++

class B based on A
    var b = 1
+++

class C based on B
    var c = 2
+++

class D based on C
    var d = 3
+++

def main() {
    var myobj = D()
    myobj.root_method()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "From A" in output
    finally:
        sys.stdout = old_stdout


def test_overridden_method_with_self():
    """Test that overridden methods correctly use self."""
    source = """
class Base
    var value = 100
    def get_value() {
        return self.value
    }
+++

class Child based on Base
    var value = 200
    def get_value() {
        return self.value * 2
    }
+++

def main() {
    var myobj = Child()
    var result = myobj.get_value()
    print(result)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "400" in output  # 200 * 2
    finally:
        sys.stdout = old_stdout


def test_method_override_with_different_logic():
    """Test that child can completely change method logic."""
    source = """
class Calculator
    def add(int a, int b) {
        return a + b
    }
+++

class SpecialCalculator based on Calculator
    def add(int a, int b) {
        return a + b + 100
    }
+++

def main() {
    var calc = SpecialCalculator()
    var result = calc.add(5, 3)
    print(result)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "108" in output  # 5 + 3 + 100
    finally:
        sys.stdout = old_stdout


def test_multiple_method_overrides():
    """Test multiple methods being overridden in same class."""
    source = """
class Base
    def method_a() {
        print("Base A")
    }
    def method_b() {
        print("Base B")
    }
    def method_c() {
        print("Base C")
    }
+++

class Child based on Base
    def method_a() {
        print("Child A")
    }
    def method_b() {
        print("Child B")
    }
    def method_c() {
        print("Child C")
    }
+++

def main() {
    var myobj = Child()
    myobj.method_a()
    myobj.method_b()
    myobj.method_c()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Child A" in output
        assert "Child B" in output
        assert "Child C" in output
        assert "Base A" not in output
        assert "Base B" not in output
        assert "Base C" not in output
    finally:
        sys.stdout = old_stdout


def test_method_resolution_with_constructors():
    """Test that method resolution works correctly with constructor chaining."""
    source = """
class Base
    var name = ""
    def Base() {
        self.name = "Base"
    }
    def identify() {
        print("I am", self.name)
    }
+++

class Child based on Base
    def Child() {
        self.name = "Child"
    }
    def identify() {
        print("Child named", self.name)
    }
+++

def main() {
    var myobj = Child()
    myobj.identify()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Child named Child" in output
        assert "I am" not in output
    finally:
        sys.stdout = old_stdout


def test_inherited_method_calls_other_inherited_method():
    """Test inherited method calling another inherited method."""
    source = """
class Base
    def helper() {
        print("Helper")
    }
    def main_method() {
        self.helper()
        print("Main")
    }
+++

class Child based on Base
    var x = 1
+++

def main() {
    var myobj = Child()
    myobj.main_method()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Helper" in output
        assert "Main" in output
    finally:
        sys.stdout = old_stdout


def test_overridden_method_calls_other_method():
    """Test that overridden method can call other inherited methods."""
    source = """
class Base
    def utility() {
        return 42
    }
    def calculate() {
        return self.utility()
    }
+++

class Child based on Base
    def calculate() {
        var base_result = self.utility()
        return base_result * 2
    }
+++

def main() {
    var myobj = Child()
    var result = myobj.calculate()
    print(result)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "84" in output  # 42 * 2
    finally:
        sys.stdout = old_stdout

