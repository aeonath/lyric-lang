# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for AST node definitions."""

import pytest
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, PrintNode
)


def test_ast_nodes_can_be_instantiated():
    """Test that all AST nodes can be instantiated (A6 requirement)."""
    
    # Create sample nodes
    literal = LiteralNode(42)
    identifier = IdentifierNode("x")
    binary_op = BinaryOpNode("+", literal, identifier)
    unary_op = UnaryOpNode("-", literal)
    assign = AssignNode("y", binary_op)
    call = CallNode("print", [literal, identifier])
    print_node = PrintNode([literal])
    
    function = FunctionNode("main", [], [assign, call])
    if_node = IfNode(identifier, [assign], [], None)
    loop = LoopNode(identifier, "while", [assign])
    class_node = ClassNode("Player", [assign, function])
    
    program = ProgramNode([function, if_node, loop, class_node])
    
    # Verify all nodes were created successfully
    assert isinstance(literal, LiteralNode)
    assert isinstance(identifier, IdentifierNode)
    assert isinstance(binary_op, BinaryOpNode)
    assert isinstance(unary_op, UnaryOpNode)
    assert isinstance(assign, AssignNode)
    assert isinstance(call, CallNode)
    assert isinstance(print_node, PrintNode)
    assert isinstance(function, FunctionNode)
    assert isinstance(if_node, IfNode)
    assert isinstance(loop, LoopNode)
    assert isinstance(class_node, ClassNode)
    assert isinstance(program, ProgramNode)


def test_ast_nodes_repr_methods():
    """Test that AST nodes have proper __repr__ methods for debugging."""
    
    literal = LiteralNode(42)
    identifier = IdentifierNode("x")
    binary_op = BinaryOpNode("+", literal, identifier)
    assign = AssignNode("y", binary_op)
    function = FunctionNode("main", ["x", "y"], [assign])
    
    # Test repr methods return strings
    assert isinstance(repr(literal), str)
    assert isinstance(repr(identifier), str)
    assert isinstance(repr(binary_op), str)
    assert isinstance(repr(assign), str)
    assert isinstance(repr(function), str)
    
    # Test that repr contains expected information
    assert "LiteralNode" in repr(literal)
    assert "42" in repr(literal)
    assert "IdentifierNode" in repr(identifier)
    assert "x" in repr(identifier)
    assert "BinaryOpNode" in repr(binary_op)
    assert "+" in repr(binary_op)
    assert "AssignNode" in repr(assign)
    assert "y" in repr(assign)
    assert "FunctionNode" in repr(function)
    assert "main" in repr(function)


def test_ast_nodes_to_dict_methods():
    """Test that AST nodes have proper to_dict methods for debugging."""
    
    literal = LiteralNode(42)
    identifier = IdentifierNode("x")
    binary_op = BinaryOpNode("+", literal, identifier)
    assign = AssignNode("y", binary_op)
    function = FunctionNode("main", ["x"], [assign])
    
    # Test to_dict methods return dictionaries
    literal_dict = literal.to_dict()
    identifier_dict = identifier.to_dict()
    binary_op_dict = binary_op.to_dict()
    assign_dict = assign.to_dict()
    function_dict = function.to_dict()
    
    assert isinstance(literal_dict, dict)
    assert isinstance(identifier_dict, dict)
    assert isinstance(binary_op_dict, dict)
    assert isinstance(assign_dict, dict)
    assert isinstance(function_dict, dict)
    
    # Test that dictionaries contain expected structure
    assert literal_dict['type'] == 'LiteralNode'
    assert literal_dict['value'] == 42
    
    assert identifier_dict['type'] == 'IdentifierNode'
    assert identifier_dict['name'] == 'x'
    
    assert binary_op_dict['type'] == 'BinaryOpNode'
    assert binary_op_dict['op'] == '+'
    assert 'left' in binary_op_dict
    assert 'right' in binary_op_dict
    
    assert assign_dict['type'] == 'AssignNode'
    assert assign_dict['name'] == 'y'
    assert 'expr' in assign_dict
    
    assert function_dict['type'] == 'FunctionNode'
    assert function_dict['name'] == 'main'
    assert function_dict['params'] == ['x']
    assert 'body' in function_dict


def test_complex_ast_structure():
    """Test creating a complex AST structure similar to real Lyric code."""
    
    # Create AST for: def main() { x = 5; if x > 0 print("positive") end }
    
    # Literals and identifiers
    five = LiteralNode(5)
    zero = LiteralNode(0)
    x_id = IdentifierNode("x")
    positive_str = LiteralNode("positive")
    
    # Assignment: x = 5
    assign_x = AssignNode("x", five)
    
    # Binary operation: x > 0
    x_gt_zero = BinaryOpNode(">", x_id, zero)
    
    # Function call: print("positive")
    print_call = CallNode("print", [positive_str])
    
    # If statement: if x > 0 print("positive") end
    if_stmt = IfNode(x_gt_zero, [print_call], [], None)
    
    # Function definition: def main() { x = 5; if x > 0 print("positive") end }
    main_func = FunctionNode("main", [], [], None, [assign_x, if_stmt])
    
    # Program: def main() { ... }
    program = ProgramNode([main_func])
    
    # Verify the structure
    assert len(program.statements) == 1
    assert program.statements[0].name == "main"
    assert len(program.statements[0].body_statements) == 2
    
    # Test that the entire structure can be converted to dict
    program_dict = program.to_dict()
    assert program_dict['type'] == 'ProgramNode'
    assert len(program_dict['statements']) == 1
    
    func_dict = program_dict['statements'][0]
    assert func_dict['type'] == 'FunctionNode'
    assert func_dict['name'] == 'main'
    assert len(func_dict['body']) == 2


def test_if_node_with_elifs_and_else():
    """Test IfNode with elifs and else clauses."""
    
    # Create conditions
    x = IdentifierNode("x")
    y = IdentifierNode("y")
    
    # Create bodies
    body1 = [AssignNode("result", LiteralNode(1))]
    body2 = [AssignNode("result", LiteralNode(2))]
    body3 = [AssignNode("result", LiteralNode(3))]
    else_body = [AssignNode("result", LiteralNode(0))]
    
    # Create if with elifs and else
    if_node = IfNode(
        condition=x,
        then_body=body1,
        elifs=[(y, body2), (x, body3)],
        else_body=else_body
    )
    
    # Verify structure
    assert len(if_node.elifs) == 2
    assert if_node.else_body is not None
    assert len(if_node.else_body) == 1
    
    # Test to_dict
    if_dict = if_node.to_dict()
    assert if_dict['type'] == 'IfNode'
    assert len(if_dict['elifs']) == 2
    assert if_dict['else_body'] is not None


def test_loop_node_iterator_and_while():
    """Test LoopNode with both iterator and while loop kinds."""
    
    # Iterator loop: for i in range(3) print(i) done
    range_call = CallNode("range", [LiteralNode(3)])
    i_id = IdentifierNode("i")
    print_call = CallNode("print", [i_id])
    
    iterator_loop = LoopNode(
        condition_or_iter=range_call,
        loop_kind="iterator",
        body=[print_call]
    )
    
    # While loop: given x > 0 x = x - 1 done
    x_id = IdentifierNode("x")
    zero = LiteralNode(0)
    one = LiteralNode(1)
    x_gt_zero = BinaryOpNode(">", x_id, zero)
    x_minus_one = BinaryOpNode("-", x_id, one)
    assign_x = AssignNode("x", x_minus_one)
    
    while_loop = LoopNode(
        condition_or_iter=x_gt_zero,
        loop_kind="while",
        body=[assign_x]
    )
    
    # Verify both loop types
    assert iterator_loop.loop_kind == "iterator"
    assert while_loop.loop_kind == "while"
    
    # Test to_dict
    iterator_dict = iterator_loop.to_dict()
    while_dict = while_loop.to_dict()
    
    assert iterator_dict['loop_kind'] == "iterator"
    assert while_dict['loop_kind'] == "while"
