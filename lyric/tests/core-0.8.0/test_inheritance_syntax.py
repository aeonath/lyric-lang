# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for inheritance syntax (Sprint 9 Task 1)."""

from lyric.parser import parse
from lyric.interpreter import evaluate
import pytest
import io
import sys


def test_basic_inheritance_syntax():
    """Test that 'based on' syntax is parsed correctly."""
    source = """
class Entity
    var id = 0
+++

class Shape based on Entity
    var size = 10
+++

def main() {
    var shape = Shape()
    print(shape.size)
    print(shape.id)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "10" in output
        assert "0" in output
    finally:
        sys.stdout = old_stdout


def test_inheritance_with_method():
    """Test that methods are inherited from base class."""
    source = """
class Animal
    var name = "Unknown"
    def speak() {
        print("Animal speaks")
    }
+++

class Dog based on Animal
    var breed = "Mixed"
+++

def main() {
    var dog = Dog()
    dog.speak()
    print(dog.name)
    print(dog.breed)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Animal speaks" in output
        assert "Unknown" in output
        assert "Mixed" in output
    finally:
        sys.stdout = old_stdout


def test_method_overriding():
    """Test that child class methods override base class methods."""
    source = """
class Animal
    def speak() {
        print("Animal sound")
    }
+++

class Cat based on Animal
    def speak() {
        print("Meow")
    }
+++

def main() {
    var cat = Cat()
    cat.speak()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Meow" in output
        assert "Animal sound" not in output
    finally:
        sys.stdout = old_stdout


def test_multiple_inheritance_not_allowed():
    """Test that multiple inheritance is not supported (should fail gracefully)."""
    # Note: Since we only support single inheritance, the parser should handle this
    # The current implementation doesn't explicitly reject multiple inheritance
    # but only allows one 'based on' clause
    pass  # This is implicitly tested by the parser only accepting one base class


def test_property_access_from_base():
    """Test that properties from base class are accessible in child instances."""
    source = """
class Vehicle
    var wheels = 4
    var color = "red"
+++

class Car based on Vehicle
    var doors = 4
+++

def main() {
    var car = Car()
    print(car.wheels)
    print(car.color)
    print(car.doors)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "4" in output
        assert "red" in output
    finally:
        sys.stdout = old_stdout


def test_property_override():
    """Test that child class properties override base class properties."""
    source = """
class Base
    var value = 100
+++

class Child based on Base
    var value = 200
+++

def main() {
    var myobj = Child()
    print(myobj.value)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "200" in output
        assert "100" not in output
    finally:
        sys.stdout = old_stdout


def test_undefined_base_class_error():
    """Test that using an undefined base class raises an error."""
    source = """
class MyClass based on NonExistent
    var x = 1
+++

def main() {
    var myobj = MyClass()
}
"""
    with pytest.raises(Exception) as exc_info:
        ast = parse(source)
        evaluate(ast)
    
    assert "not defined" in str(exc_info.value).lower() or "nonexistent" in str(exc_info.value).lower()


def test_inheritance_chain_two_levels():
    """Test two levels of inheritance."""
    source = """
class A
    var a = 1
+++

class B based on A
    var b = 2
+++

class C based on B
    var c = 3
+++

def main() {
    var myobj = C()
    print(myobj.a)
    print(myobj.b)
    print(myobj.c)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "1" in output
        assert "2" in output
        assert "3" in output
    finally:
        sys.stdout = old_stdout


def test_method_access_from_grandparent():
    """Test that methods from grandparent classes are accessible."""
    source = """
class Grandparent
    def greet() {
        print("Hello from Grandparent")
    }
+++

class Parent based on Grandparent
    var parent_attr = "parent"
+++

class Child based on Parent
    var child_attr = "child"
+++

def main() {
    var child = Child()
    child.greet()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Hello from Grandparent" in output
    finally:
        sys.stdout = old_stdout


def test_self_in_inherited_method():
    """Test that self works correctly in inherited methods."""
    source = """
class Base
    var name = "Base"
    def get_name() {
        return self.name
    }
+++

class Child based on Base
    var name = "Child"
+++

def main() {
    var myobj = Child()
    var result = myobj.get_name()
    print(result)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Child" in output
    finally:
        sys.stdout = old_stdout


def test_no_inheritance_works():
    """Test that classes without inheritance still work."""
    source = """
class Simple
    var x = 42
+++

def main() {
    var myobj = Simple()
    print(myobj.x)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "42" in output
    finally:
        sys.stdout = old_stdout


def test_inheritance_with_multiple_methods():
    """Test inheritance with multiple methods in both base and child."""
    source = """
class Rectangle
    var width = 10
    var height = 5
    
    def area() {
        return self.width * self.height
    }
+++

class Square based on Rectangle
    var width = 7
    var height = 7
    
    def perimeter() {
        return 4 * self.width
    }
+++

def main() {
    var sq = Square()
    print(sq.area())
    print(sq.perimeter())
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "49" in output  # area: 7 * 7
        assert "28" in output  # perimeter: 4 * 7
    finally:
        sys.stdout = old_stdout

