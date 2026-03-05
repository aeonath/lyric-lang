# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for automatic constructor chaining (Sprint 9 Task 2)."""

from lyric.parser import parse
from lyric.interpreter import evaluate
import pytest
import io
import sys


def test_basic_constructor_chaining():
    """Test that constructors are called in base→child order."""
    source = """
class A
    def A() {
        print("A")
    }
+++

class B based on A
    def B() {
        print("B")
    }
+++

class C based on B
    def C() {
        print("C")
    }
+++

def main() {
    var myobj = C()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        lines = output.strip().split('\n')
        assert len(lines) == 3
        assert lines[0] == "A"
        assert lines[1] == "B"
        assert lines[2] == "C"
    finally:
        sys.stdout = old_stdout


def test_constructor_chaining_two_levels():
    """Test constructor chaining with two levels of inheritance."""
    source = """
class Base
    def Base() {
        print("Base constructor")
    }
+++

class Derived based on Base
    def Derived() {
        print("Derived constructor")
    }
+++

def main() {
    var myobj = Derived()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Base constructor" in output
        assert "Derived constructor" in output
        # Check order
        assert output.index("Base constructor") < output.index("Derived constructor")
    finally:
        sys.stdout = old_stdout


def test_missing_base_constructor():
    """Test that missing base constructors are skipped gracefully."""
    source = """
class A
    var x = 1
+++

class B based on A
    def B() {
        print("B constructor")
    }
+++

def main() {
    var myobj = B()
    print(myobj.x)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "B constructor" in output
        assert "1" in output
    finally:
        sys.stdout = old_stdout


def test_missing_child_constructor():
    """Test that child class without constructor still calls base constructor."""
    source = """
class Base
    def Base() {
        print("Base constructor")
    }
+++

class Child based on Base
    var y = 2
+++

def main() {
    var myobj = Child()
    print(myobj.y)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Base constructor" in output
        assert "2" in output
    finally:
        sys.stdout = old_stdout


def test_no_constructors_in_chain():
    """Test that classes without any constructors work fine."""
    source = """
class A
    var x = 10
+++

class B based on A
    var y = 20
+++

def main() {
    var myobj = B()
    print(myobj.x)
    print(myobj.y)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "10" in output
        assert "20" in output
    finally:
        sys.stdout = old_stdout


def test_constructor_with_self_reference():
    """Test that constructors can use self to set instance variables."""
    source = """
class A
    var value = 0
    def A() {
        self.value = 100
    }
+++

class B based on A
    var other = 0
    def B() {
        self.other = 200
    }
+++

def main() {
    var myobj = B()
    print(myobj.value)
    print(myobj.other)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "100" in output
        assert "200" in output
    finally:
        sys.stdout = old_stdout


def test_constructor_modifying_inherited_attributes():
    """Test that child constructor can modify inherited attributes."""
    source = """
class Base
    var count = 0
    def Base() {
        self.count = 1
    }
+++

class Child based on Base
    def Child() {
        self.count = self.count + 10
    }
+++

def main() {
    var myobj = Child()
    print(myobj.count)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "11" in output  # Base sets to 1, Child adds 10
    finally:
        sys.stdout = old_stdout


def test_multiple_instances_independent_constructors():
    """Test that multiple instances have independent constructor calls."""
    source = """
class Counter
    var value = 0
    def Counter() {
        self.value = 42
        print("Constructor called")
    }
+++

def main() {
    var obj1 = Counter()
    var obj2 = Counter()
    print(obj1.value)
    print(obj2.value)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert output.count("Constructor called") == 2
        assert output.count("42") == 2
    finally:
        sys.stdout = old_stdout


def test_constructor_chaining_with_methods():
    """Test that constructor chaining works alongside method inheritance."""
    source = """
class Animal
    var name = ""
    def Animal() {
        self.name = "Generic Animal"
    }
    def speak() {
        print(self.name, "makes a sound")
    }
+++

class Dog based on Animal
    def Dog() {
        self.name = "Dog"
    }
+++

def main() {
    var dog = Dog()
    dog.speak()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Dog makes a sound" in output
    finally:
        sys.stdout = old_stdout


def test_three_level_partial_constructors():
    """Test three-level inheritance with some constructors missing."""
    source = """
class A
    def A() {
        print("A")
    }
+++

class B based on A
    var x = 1
+++

class C based on B
    def C() {
        print("C")
    }
+++

def main() {
    var myobj = C()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        lines = output.strip().split('\n')
        assert len(lines) == 2
        assert lines[0] == "A"
        assert lines[1] == "C"
    finally:
        sys.stdout = old_stdout


def test_constructor_with_print_statements():
    """Test constructor chaining with various print statements."""
    source = """
class Grandparent
    def Grandparent() {
        print("Grandparent initialized")
    }
+++

class Parent based on Grandparent
    def Parent() {
        print("Parent initialized")
    }
+++

class Child based on Parent
    def Child() {
        print("Child initialized")
    }
+++

def main() {
    print("Creating instance:")
    var myobj = Child()
    print("Instance created")
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        lines = output.strip().split('\n')
        assert lines[0] == "Creating instance:"
        assert lines[1] == "Grandparent initialized"
        assert lines[2] == "Parent initialized"
        assert lines[3] == "Child initialized"
        assert lines[4] == "Instance created"
    finally:
        sys.stdout = old_stdout

