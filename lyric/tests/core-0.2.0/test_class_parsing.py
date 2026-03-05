# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for class parsing in Lyric language."""

from lyric.parser import parse
from lyric.ast_nodes import ClassNode, AssignNode, FunctionNode
import pytest


def test_parse_class_with_method_a11():
    """Test class parsing with method (A11 from Sprint2 Task4)."""
    source = """class Player
    name = "Guest"
    def greet() { print("Hello,", self.name) }
+++"""
    
    ast = parse(source)
    
    # Should have one statement - the class definition
    assert len(ast.statements) == 1
    
    # Verify it's a class node
    class_node = ast.statements[0]
    assert isinstance(class_node, ClassNode)
    assert class_node.name == "Player"
    
    # Class should have 2 members: assignment and function
    assert len(class_node.members_statements) == 2
    
    # First member should be an assignment
    assert isinstance(class_node.members_statements[0], AssignNode)
    assert class_node.members_statements[0].name == "name"
    
    # Second member should be a function
    assert isinstance(class_node.members_statements[1], FunctionNode)
    assert class_node.members_statements[1].name == "greet"


def test_parse_simple_class():
    """Test simple class parsing."""
    source = """class Person
    age = 25
+++"""
    
    ast = parse(source)
    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], ClassNode)
    assert ast.statements[0].name == "Person"


def test_parse_class_with_multiple_methods():
    """Test class with multiple methods."""
    source = """class Calculator
    def add(a, b) { return a + b }
    def subtract(a, b) { return a - b }
+++"""
    
    ast = parse(source)
    assert len(ast.statements) == 1
    class_node = ast.statements[0]
    assert isinstance(class_node, ClassNode)
    assert len(class_node.members_statements) == 2


def test_parse_empty_class():
    """Test empty class parsing."""
    source = """class Empty
+++"""
    
    ast = parse(source)
    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], ClassNode)
    assert len(ast.statements[0].members_statements) == 0

