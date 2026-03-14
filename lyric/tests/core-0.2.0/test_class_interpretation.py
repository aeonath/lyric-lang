# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for class interpretation in Lyric language."""

from lyric.parser import parse
from lyric.interpreter import evaluate
import pytest
import io
import sys


def test_class_definition_and_instantiation_a12():
    """Test defining a class and creating an instance (A12)."""
    source = """class Person
    var name = "Guest"
    var age = 25
+++

def main() {
    var person = Person()
    print("Created person instance")
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Created person instance" in output
    finally:
        sys.stdout = old_stdout


def test_class_method_call_a13():
    """Test calling an instance method (A13)."""
    source = """class Player
    var name = "Guest"
    def greet() {
        print("Hello,", self.name)
    }
+++

def main() {
    var player = Player()
    player.greet()
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Hello, Guest" in output
    finally:
        sys.stdout = old_stdout


def test_instance_variables_a14():
    """Test instance variables are stored in each object dictionary (A14)."""
    source = """class Person
    var name = "Default"
    def set_name(new_name) {
        self.name = new_name
    }
    def get_name() {
        return self.name
    }
+++

def main() {
    var person1 = Person()
    var person2 = Person()
    
    person1.set_name("Alice")
    person2.set_name("Bob")
    
    print("Person1:", person1.get_name())
    print("Person2:", person2.get_name())
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Person1: Alice" in output
        assert "Person2: Bob" in output
    finally:
        sys.stdout = old_stdout


def test_class_without_methods():
    """Test simple class with just attributes."""
    source = """class Point
    var x = 0
    var y = 0
+++

def main() {
    var point = Point()
    print("Point created:", point.x, point.y)
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Point created: 0 0" in output
    finally:
        sys.stdout = old_stdout


def test_class_instantiation_syntax():
    """Test class instantiation syntax like player = Player()."""
    source = """class Calculator
    def add(a, b) {
        return a + b
    }
+++

def main() {
    var calc = Calculator()
    var result = calc.add(5, 3)
    print("Result:", result)
}"""
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Result: 8" in output
    finally:
        sys.stdout = old_stdout
