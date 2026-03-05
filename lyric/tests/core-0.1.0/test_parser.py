# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for parser module."""

import pytest
from lyric.parser import parse
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, ReturnNode, PrintNode
)
from lyric.errors import ParseError


def test_parse_function_definition():
    """Test parsing function definition: def main() { print("Hello, Lyric!") }"""
    source = 'def main() { print("Hello, Lyric!") }'
    
    ast = parse(source)
    
    # Verify AST structure
    assert isinstance(ast, ProgramNode)
    assert len(ast.statements) == 1
    
    func = ast.statements[0]
    assert isinstance(func, FunctionNode)
    assert func.name == "main"
    assert func.params == []
    assert len(func.body_statements) == 1
    
    call = func.body_statements[0]
    assert isinstance(call, CallNode)
    assert call.func_name == "print"
    assert len(call.args) == 1
    assert isinstance(call.args[0], LiteralNode)
    assert call.args[0].value == "Hello, Lyric!"


def test_parse_if_else_statement():
    """Test parsing if/else statement."""
    source = '''def main() {
x = 5
if x > 0:
print("positive")
else:
print("non-positive")
end
}'''
    
    ast = parse(source)
    
    # Verify AST structure
    assert isinstance(ast, ProgramNode)
    assert len(ast.statements) == 1
    
    func = ast.statements[0]
    assert isinstance(func, FunctionNode)
    assert func.name == "main"
    assert len(func.body_statements) == 2
    
    # Check assignment
    assign = func.body_statements[0]
    assert isinstance(assign, AssignNode)
    assert assign.name == "x"
    assert isinstance(assign.expr, LiteralNode)
    assert assign.expr.value == 5
    
    # Check if statement
    if_stmt = func.body_statements[1]
    assert isinstance(if_stmt, IfNode)
    
    # Check condition: x > 0
    assert isinstance(if_stmt.condition, BinaryOpNode)
    assert if_stmt.condition.op == ">"
    assert isinstance(if_stmt.condition.left, IdentifierNode)
    assert if_stmt.condition.left.name == "x"
    assert isinstance(if_stmt.condition.right, LiteralNode)
    assert if_stmt.condition.right.value == 0
    
    # Check then body
    assert len(if_stmt.then_body) == 1
    then_call = if_stmt.then_body[0]
    assert isinstance(then_call, CallNode)
    assert then_call.func_name == "print"
    assert isinstance(then_call.args[0], LiteralNode)
    assert then_call.args[0].value == "positive"
    
    # Check else body
    assert if_stmt.else_body is not None
    assert len(if_stmt.else_body) == 1
    else_call = if_stmt.else_body[0]
    assert isinstance(else_call, CallNode)
    assert else_call.func_name == "print"
    assert isinstance(else_call.args[0], LiteralNode)
    assert else_call.args[0].value == "non-positive"
    
    # Check no elifs
    assert len(if_stmt.elifs) == 0


def test_parse_loop_statement():
    """Test parsing loop statement: for i in range(3): print(i) done"""
    source = '''def main() {
int i
for i in range(3):
print(i)
done
}'''
    
    ast = parse(source)
    
    # Verify AST structure
    assert isinstance(ast, ProgramNode)
    assert len(ast.statements) == 1
    
    func = ast.statements[0]
    assert isinstance(func, FunctionNode)
    assert func.name == "main"
    assert len(func.body_statements) == 2

    # Check loop statement (second statement after int i declaration)
    loop = func.body_statements[1]
    assert isinstance(loop, LoopNode)
    assert loop.loop_kind == "iterator"  # Should detect range() call
    
    # Check condition/iterator: i in range(3)
    # Note: This is a simplified check - in a real implementation,
    # we might need to handle "i in range(3)" as a special iterator expression
    assert isinstance(loop.condition_or_iter, CallNode)
    assert loop.condition_or_iter.func_name == "range"
    assert len(loop.condition_or_iter.args) == 1
    assert isinstance(loop.condition_or_iter.args[0], LiteralNode)
    assert loop.condition_or_iter.args[0].value == 3
    
    # Check loop body
    assert len(loop.body) == 1
    call = loop.body[0]
    assert isinstance(call, CallNode)
    assert call.func_name == "print"
    assert len(call.args) == 1
    assert isinstance(call.args[0], IdentifierNode)
    assert call.args[0].name == "i"


def test_parse_class_definition():
    """Test parsing class definition: class Player name = "Guest" def greet() { print("Hello,", self.name) } +++"""
    source = '''class Player
name = "Guest"
def greet() {
print("Hello,", self.name)
}
+++'''
    
    ast = parse(source)
    
    # Verify AST structure
    assert isinstance(ast, ProgramNode)
    assert len(ast.statements) == 1
    
    class_node = ast.statements[0]
    assert isinstance(class_node, ClassNode)
    assert class_node.name == "Player"
    assert len(class_node.members_statements) == 2
    
    # Check assignment member
    assign = class_node.members_statements[0]
    assert isinstance(assign, AssignNode)
    assert assign.name == "name"
    assert isinstance(assign.expr, LiteralNode)
    assert assign.expr.value == "Guest"
    
    # Check function member
    func = class_node.members_statements[1]
    assert isinstance(func, FunctionNode)
    assert func.name == "greet"
    assert func.params == []
    assert len(func.body_statements) == 1
    
    # Check function body
    call = func.body_statements[0]
    assert isinstance(call, CallNode)
    assert call.func_name == "print"
    assert len(call.args) == 2
    assert isinstance(call.args[0], LiteralNode)
    assert call.args[0].value == "Hello,"
    assert isinstance(call.args[1], IdentifierNode)
    assert call.args[1].name == "self.name"


def test_parse_else_if_sequence():
    """Test parsing else-if sequence."""
    source = '''def main() {
x = 5
if x > 10:
print("high")
elif x > 5:
print("medium")
elif x > 0:
print("low")
else:
print("zero or negative")
end
}'''
    
    ast = parse(source)
    
    # Verify AST structure
    func = ast.statements[0]
    if_stmt = func.body_statements[1]
    
    assert isinstance(if_stmt, IfNode)
    
    # Check then body
    assert len(if_stmt.then_body) == 1
    assert if_stmt.then_body[0].args[0].value == "high"
    
    # Check elifs
    assert len(if_stmt.elifs) == 2
    
    # First elif: x > 5
    elif1_cond, elif1_body = if_stmt.elifs[0]
    assert isinstance(elif1_cond, BinaryOpNode)
    assert elif1_cond.op == ">"
    assert elif1_cond.right.value == 5
    assert len(elif1_body) == 1
    assert elif1_body[0].args[0].value == "medium"
    
    # Second elif: x > 0
    elif2_cond, elif2_body = if_stmt.elifs[1]
    assert isinstance(elif2_cond, BinaryOpNode)
    assert elif2_cond.op == ">"
    assert elif2_cond.right.value == 0
    assert len(elif2_body) == 1
    assert elif2_body[0].args[0].value == "low"
    
    # Check else body
    assert if_stmt.else_body is not None
    assert len(if_stmt.else_body) == 1
    assert if_stmt.else_body[0].args[0].value == "zero or negative"


def test_parse_binary_operations():
    """Test parsing binary operations with precedence."""
    source = '''def main() {
result = 2 + 3 * 4 - 1
}'''
    
    ast = parse(source)
    
    func = ast.statements[0]
    assign = func.body_statements[0]
    
    assert isinstance(assign, AssignNode)
    assert assign.name == "result"
    
    # Check expression: 2 + 3 * 4 - 1
    # Should be parsed as: (2 + (3 * 4)) - 1
    expr = assign.expr
    assert isinstance(expr, BinaryOpNode)
    assert expr.op == "-"
    
    # Left side: 2 + (3 * 4)
    left = expr.left
    assert isinstance(left, BinaryOpNode)
    assert left.op == "+"
    assert isinstance(left.left, LiteralNode)
    assert left.left.value == 2
    
    # Right side: 3 * 4
    right_mult = left.right
    assert isinstance(right_mult, BinaryOpNode)
    assert right_mult.op == "*"
    assert isinstance(right_mult.left, LiteralNode)
    assert right_mult.left.value == 3
    assert isinstance(right_mult.right, LiteralNode)
    assert right_mult.right.value == 4
    
    # Right side of main expression: 1
    assert isinstance(expr.right, LiteralNode)
    assert expr.right.value == 1


def test_parse_function_with_parameters():
    """Test parsing function with parameters."""
    source = '''def add(x, y) {
return x + y
}'''
    
    ast = parse(source)
    
    func = ast.statements[0]
    assert isinstance(func, FunctionNode)
    assert func.name == "add"
    assert func.params == ["x", "y"]
    assert len(func.body_statements) == 1
    
    # Now "return" is implemented, so this should be a return statement
    return_stmt = func.body_statements[0]
    assert isinstance(return_stmt, ReturnNode)
    assert return_stmt.value is not None
    expr = return_stmt.value
    assert isinstance(expr, BinaryOpNode)
    assert expr.op == "+"
    assert isinstance(expr.left, IdentifierNode)
    assert expr.left.name == "x"
    assert isinstance(expr.right, IdentifierNode)
    assert expr.right.name == "y"


def test_parse_error_handling():
    """Test parser error handling."""
    # Test missing closing brace
    with pytest.raises(ParseError):
        parse('def main() { print("hello")')
    
    # Test missing function name
    with pytest.raises(ParseError):
        parse('def () { print("hello") }')
    
    # Test missing class terminator
    with pytest.raises(ParseError):
        parse('class Player name = "test"')


def test_parse_complex_nested_structure():
    """Test parsing a complex nested structure."""
    source = '''def main() {
x = 10
if x > 5:
y = x * 2
if y > 15:
print("nested if")
else:
print("nested else")
end
else:
print("outer else")
end
}'''
    
    ast = parse(source)
    
    func = ast.statements[0]
    assert len(func.body_statements) == 2  # assign, if
    
    # Check nested if structure
    outer_if = func.body_statements[1]
    assert isinstance(outer_if, IfNode)
    assert len(outer_if.then_body) == 2  # assign, nested if
    
    nested_if = outer_if.then_body[1]
    assert isinstance(nested_if, IfNode)
    assert len(nested_if.then_body) == 1
    assert len(nested_if.else_body) == 1
    assert len(nested_if.elifs) == 0


def test_parse_hello_example():
    """Test parsing the hello.ly example."""
    source = """def main() {
    print("Hello, Lyric!")
}"""
    
    ast = parse(source)
    
    # Should have one function definition
    assert len(ast.statements) == 1
    func = ast.statements[0]
    assert isinstance(func, FunctionNode)
    assert func.name == "main"
    
    # Should have one statement in main body
    assert len(func.body_statements) == 1
    print_stmt = func.body_statements[0]
    assert isinstance(print_stmt, CallNode)
    assert print_stmt.func_name == "print"
    assert len(print_stmt.args) == 1
    assert isinstance(print_stmt.args[0], LiteralNode)
    assert print_stmt.args[0].value == "Hello, Lyric!"


def test_parse_if_demo_example():
    """Test parsing the if_demo.ly example."""
    source = """def main() {
    x = 5
    if x > 0:
        print("positive")
    else:
        print("non-positive")
    end
}"""
    
    ast = parse(source)
    
    # Should have one function definition
    assert len(ast.statements) == 1
    func = ast.statements[0]
    assert isinstance(func, FunctionNode)
    assert func.name == "main"
    
    # Should have two statements in main body
    assert len(func.body_statements) == 2
    
    # First statement: assignment
    assign_stmt = func.body_statements[0]
    assert isinstance(assign_stmt, AssignNode)
    assert assign_stmt.name == "x"
    assert isinstance(assign_stmt.expr, LiteralNode)
    assert assign_stmt.expr.value == 5
    
    # Second statement: if-else
    if_stmt = func.body_statements[1]
    assert isinstance(if_stmt, IfNode)
    
    # Check condition
    assert isinstance(if_stmt.condition, BinaryOpNode)
    assert if_stmt.condition.op == ">"
    assert isinstance(if_stmt.condition.left, IdentifierNode)
    assert if_stmt.condition.left.name == "x"
    assert isinstance(if_stmt.condition.right, LiteralNode)
    assert if_stmt.condition.right.value == 0
    
    # Check then body
    assert len(if_stmt.then_body) == 1
    print_stmt = if_stmt.then_body[0]
    assert isinstance(print_stmt, CallNode)
    assert print_stmt.func_name == "print"
    assert print_stmt.args[0].value == "positive"
    
    # Check else body
    assert len(if_stmt.else_body) == 1
    print_stmt = if_stmt.else_body[0]
    assert isinstance(print_stmt, CallNode)
    assert print_stmt.func_name == "print"
    assert print_stmt.args[0].value == "non-positive"


def test_parse_loop_example():
    """Test parsing the loop.ly example."""
    source = """def main() {
    int i
    for i in range(3):
        print(i)
    done
}"""
    
    ast = parse(source)
    
    # Should have one function definition
    assert len(ast.statements) == 1
    func = ast.statements[0]
    assert isinstance(func, FunctionNode)
    assert func.name == "main"
    
    # Should have two statements: int i declaration + loop
    assert len(func.body_statements) == 2
    loop_stmt = func.body_statements[1]
    assert isinstance(loop_stmt, LoopNode)
    assert loop_stmt.loop_kind == "iterator"
    assert loop_stmt.iterator_var == "i"
    
    # Check the range call
    assert isinstance(loop_stmt.condition_or_iter, CallNode)
    assert loop_stmt.condition_or_iter.func_name == "range"
    assert len(loop_stmt.condition_or_iter.args) == 1
    assert isinstance(loop_stmt.condition_or_iter.args[0], LiteralNode)
    assert loop_stmt.condition_or_iter.args[0].value == 3
    
    # Check loop body
    assert len(loop_stmt.body) == 1
    print_stmt = loop_stmt.body[0]
    assert isinstance(print_stmt, CallNode)
    assert print_stmt.func_name == "print"
    assert len(print_stmt.args) == 1
    assert isinstance(print_stmt.args[0], IdentifierNode)
    assert print_stmt.args[0].name == "i"


def test_parse_class_example():
    """Test parsing a class definition example."""
    source = """class Player
def greet() {
    print("Hello!")
}
+++"""
    
    ast = parse(source)
    
    # Should have one class definition
    assert len(ast.statements) == 1
    class_stmt = ast.statements[0]
    assert isinstance(class_stmt, ClassNode)
    assert class_stmt.name == "Player"
    
    # Should have one method in the class
    assert len(class_stmt.members_statements) == 1
    method = class_stmt.members_statements[0]
    assert isinstance(method, FunctionNode)
    assert method.name == "greet"
    
    # Check method body
    assert len(method.body_statements) == 1
    print_stmt = method.body_statements[0]
    assert isinstance(print_stmt, CallNode)
    assert print_stmt.func_name == "print"
    assert print_stmt.args[0].value == "Hello!"