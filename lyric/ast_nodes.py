# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""AST node definitions for Lyric language."""

from dataclasses import dataclass
from typing import List, Optional, Any, Union


class ASTNode:
    """Base class for all AST nodes with position tracking."""
    
    def get_position(self) -> tuple[int, int]:
        """Get the line and column position of this node."""
        return (getattr(self, 'line', 0), getattr(self, 'column', 0))


@dataclass
class ProgramNode(ASTNode):
    """Represents the root of a Lyric program."""
    statements: List['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"ProgramNode(statements={len(self.statements)})"
    
    def to_dict(self):
        return {
            'type': 'ProgramNode',
            'statements': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.statements]
        }


@dataclass
class FunctionNode(ASTNode):
    """Represents a function definition."""
    name: str
    params: List[str]
    param_types: Optional[List[str]] = None  # Optional list of parameter types
    return_type: Optional[str] = None  # Optional return type (None means inferred)
    body_statements: List['ASTNode'] = None
    visibility: str = 'public'  # Access modifier: 'public', 'private', or 'protected'
    line: int = 0
    column: int = 0
    
    def __post_init__(self):
        if self.body_statements is None:
            self.body_statements = []
        if self.param_types is None:
            self.param_types = []
    
    def __repr__(self):
        return f"FunctionNode(name='{self.name}', params={self.params}, param_types={self.param_types}, return_type={self.return_type}, visibility={self.visibility}, body={len(self.body_statements)})"
    
    def to_dict(self):
        return {
            'type': 'FunctionNode',
            'name': self.name,
            'params': self.params,
            'param_types': self.param_types,
            'visibility': self.visibility,
            'body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.body_statements]
        }


@dataclass
class IfNode(ASTNode):
    """Represents an if/elif/else statement."""
    condition: 'ASTNode'
    then_body: List['ASTNode']
    elifs: List[tuple['ASTNode', List['ASTNode']]]  # List of (condition, body) tuples
    else_body: Optional[List['ASTNode']]
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        elif_count = len(self.elifs)
        else_present = self.else_body is not None
        return f"IfNode(condition={self.condition}, then={len(self.then_body)}, elifs={elif_count}, else={else_present})"
    
    def to_dict(self):
        return {
            'type': 'IfNode',
            'condition': self.condition.to_dict() if hasattr(self.condition, 'to_dict') else str(self.condition),
            'then_body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.then_body],
            'elifs': [(cond.to_dict() if hasattr(cond, 'to_dict') else str(cond), 
                      [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in body]) 
                     for cond, body in self.elifs],
            'else_body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.else_body] if self.else_body else None
        }


@dataclass
class LoopNode(ASTNode):
    """Represents a loop statement (given/done)."""
    condition_or_iter: 'ASTNode'
    loop_kind: str  # "iterator" or "while"
    body: List['ASTNode']
    iterator_var: Optional[str] = None  # Variable name for iterator loops
    iterator_type: Optional[str] = None  # Inline type declaration (e.g., "int", "str", "var")
    line: int = 0
    column: int = 0

    def __repr__(self):
        return f"LoopNode(kind='{self.loop_kind}', condition={self.condition_or_iter}, body={len(self.body)}, iterator_var={self.iterator_var}, iterator_type={self.iterator_type})"

    def to_dict(self):
        return {
            'type': 'LoopNode',
            'loop_kind': self.loop_kind,
            'condition_or_iter': self.condition_or_iter.to_dict() if hasattr(self.condition_or_iter, 'to_dict') else str(self.condition_or_iter),
            'body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.body],
            'iterator_var': self.iterator_var,
            'iterator_type': self.iterator_type
        }


@dataclass
class AssignNode(ASTNode):
    """Represents a variable assignment."""
    name: str
    expr: 'ASTNode'
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"AssignNode(name='{self.name}', expr={self.expr})"
    
    def to_dict(self):
        return {
            'type': 'AssignNode',
            'name': self.name,
            'expr': self.expr.to_dict() if hasattr(self.expr, 'to_dict') else str(self.expr)
        }


@dataclass
class CallNode(ASTNode):
    """Represents a function call."""
    func_name: str
    args: List['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"CallNode(func='{self.func_name}', args={len(self.args)})"
    
    def to_dict(self):
        return {
            'type': 'CallNode',
            'func_name': self.func_name,
            'args': [arg.to_dict() if hasattr(arg, 'to_dict') else str(arg) for arg in self.args]
        }


@dataclass
class BinaryOpNode(ASTNode):
    """Represents a binary operation."""
    op: str
    left: 'ASTNode'
    right: 'ASTNode'
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"BinaryOpNode(op='{self.op}', left={self.left}, right={self.right})"
    
    def to_dict(self):
        return {
            'type': 'BinaryOpNode',
            'op': self.op,
            'left': self.left.to_dict() if hasattr(self.left, 'to_dict') else str(self.left),
            'right': self.right.to_dict() if hasattr(self.right, 'to_dict') else str(self.right)
        }


@dataclass
class UnaryOpNode(ASTNode):
    """Represents a unary operation."""
    op: str
    operand: 'ASTNode'
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"UnaryOpNode(op='{self.op}', operand={self.operand})"
    
    def to_dict(self):
        return {
            'type': 'UnaryOpNode',
            'op': self.op,
            'operand': self.operand.to_dict() if hasattr(self.operand, 'to_dict') else str(self.operand)
        }


@dataclass
class LiteralNode(ASTNode):
    """Represents a literal value."""
    value: Any
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"LiteralNode(value={repr(self.value)})"
    
    def to_dict(self):
        return {
            'type': 'LiteralNode',
            'value': self.value
        }


@dataclass
class IdentifierNode(ASTNode):
    """Represents an identifier (variable name)."""
    name: str
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"IdentifierNode(name='{self.name}')"
    
    def to_dict(self):
        return {
            'type': 'IdentifierNode',
            'name': self.name
        }


@dataclass
class ClassNode(ASTNode):
    """Represents a class definition."""
    name: str
    members_statements: List['ASTNode']
    constructor_method: Optional['FunctionNode'] = None  # Constructor method (name matches class name)
    base_class: Optional[str] = None  # Name of base class for inheritance
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        constructor_info = f", constructor={self.constructor_method.name if self.constructor_method else 'None'}"
        base_info = f", base_class={self.base_class}" if self.base_class else ""
        return f"ClassNode(name='{self.name}', members={len(self.members_statements)}{constructor_info}{base_info})"
    
    def to_dict(self):
        return {
            'type': 'ClassNode',
            'name': self.name,
            'members': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.members_statements],
            'constructor': self.constructor_method.to_dict() if self.constructor_method and hasattr(self.constructor_method, 'to_dict') else None,
            'base_class': self.base_class
        }


@dataclass
class ReturnNode(ASTNode):
    """Represents a return statement."""
    value: Optional['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"ReturnNode(value={self.value})"
    
    def to_dict(self):
        return {
            'type': 'ReturnNode',
            'value': self.value.to_dict() if self.value and hasattr(self.value, 'to_dict') else str(self.value)
        }


@dataclass
class BreakNode(ASTNode):
    """Represents a break statement."""
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"BreakNode()"
    
    def to_dict(self):
        return {
            'type': 'BreakNode'
        }


@dataclass
class ContinueNode(ASTNode):
    """Represents a continue statement."""
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"ContinueNode()"
    
    def to_dict(self):
        return {
            'type': 'ContinueNode'
        }


@dataclass
class ListLiteralNode(ASTNode):
    """Represents a list literal."""
    elements: List['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"ListLiteralNode(elements={len(self.elements)})"
    
    def to_dict(self):
        return {
            'type': 'ListLiteralNode',
            'elements': [elem.to_dict() if hasattr(elem, 'to_dict') else str(elem) for elem in self.elements]
        }


@dataclass
class TupleLiteralNode(ASTNode):
    """Represents a tuple literal: (elem1, elem2, ...)"""
    elements: List['ASTNode']
    line: int = 0
    column: int = 0

    def __repr__(self):
        return f"TupleLiteralNode(elements={len(self.elements)})"

    def to_dict(self):
        return {
            'type': 'TupleLiteralNode',
            'elements': [elem.to_dict() if hasattr(elem, 'to_dict') else str(elem) for elem in self.elements]
        }


@dataclass
class DictLiteralNode(ASTNode):
    """Represents a dictionary literal."""
    pairs: List[tuple['ASTNode', 'ASTNode']]  # List of (key, value) pairs
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"DictLiteralNode(pairs={len(self.pairs)})"
    
    def to_dict(self):
        return {
            'type': 'DictLiteralNode',
            'pairs': [(key.to_dict() if hasattr(key, 'to_dict') else str(key),
                      value.to_dict() if hasattr(value, 'to_dict') else str(value))
                     for key, value in self.pairs]
        }


@dataclass
class IndexNode(ASTNode):
    """Represents an indexing operation (list[index] or dict[key])."""
    obj: 'ASTNode'  # The object being indexed
    index: 'ASTNode'  # The index/key
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"IndexNode(obj={self.obj}, index={self.index})"
    
    def to_dict(self):
        return {
            'type': 'IndexNode',
            'obj': self.obj.to_dict() if hasattr(self.obj, 'to_dict') else str(self.obj),
            'index': self.index.to_dict() if hasattr(self.index, 'to_dict') else str(self.index)
        }


@dataclass
class TypeDeclarationNode(ASTNode):
    """Represents a typed variable declaration."""
    type_name: str
    name: str
    expr: 'ASTNode'
    visibility: str = 'public'  # Access modifier: 'public', 'private', or 'protected'
    line: int = 0
    column: int = 0

    def __repr__(self):
        return f"TypeDeclarationNode(type='{self.type_name}', name='{self.name}', expr={self.expr}, visibility={self.visibility})"

    def to_dict(self):
        return {
            'type': 'TypeDeclarationNode',
            'type_name': self.type_name,
            'name': self.name,
            'visibility': self.visibility,
            'expr': self.expr.to_dict() if hasattr(self.expr, 'to_dict') else str(self.expr)
        }


@dataclass
class PrintNode(ASTNode):
    """Represents a print statement (convenience node)."""
    args: List['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"PrintNode(args={len(self.args)})"
    
    def to_dict(self):
        return {
            'type': 'PrintNode',
            'args': [arg.to_dict() if hasattr(arg, 'to_dict') else str(arg) for arg in self.args]
        }


@dataclass
class CatchClauseNode(ASTNode):
    """Represents a catch clause with optional type and variable binding."""
    exception_type: Optional[str]  # None for bare catch, str for typed catch
    variable_name: Optional[str]   # None for catch without binding, str for catch as var
    body: List['ASTNode']
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        type_str = f" {self.exception_type}" if self.exception_type else ""
        var_str = f" as {self.variable_name}" if self.variable_name else ""
        return f"CatchClauseNode({type_str}{var_str}, body={len(self.body)})"
    
    def to_dict(self):
        return {
            'type': 'CatchClauseNode',
            'exception_type': self.exception_type,
            'variable_name': self.variable_name,
            'body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.body]
        }


@dataclass
class TryNode(ASTNode):
    """Represents a try/catch/finally statement."""
    try_body: List['ASTNode']
    catch_clauses: List[CatchClauseNode]  # List of catch clauses instead of single catch_body
    finally_body: Optional[List['ASTNode']]
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        catch_count = len(self.catch_clauses)
        finally_present = self.finally_body is not None
        return f"TryNode(try={len(self.try_body)}, catch_clauses={catch_count}, finally={finally_present})"
    
    def to_dict(self):
        return {
            'type': 'TryNode',
            'try_body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.try_body],
            'catch_clauses': [clause.to_dict() for clause in self.catch_clauses],
            'finally_body': [stmt.to_dict() if hasattr(stmt, 'to_dict') else str(stmt) for stmt in self.finally_body] if self.finally_body else None
        }


@dataclass
class RaiseNode(ASTNode):
    """Represents a raise statement."""
    exception_name: str
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"RaiseNode(exception='{self.exception_name}')"
    
    def to_dict(self):
        return {
            'type': 'RaiseNode',
            'exception_name': self.exception_name
        }


@dataclass
class MultiDeclarationNode(ASTNode):
    """Represents multiple variable declarations in a single line."""
    declarations: List[tuple[str, str]]  # List of (type_name, variable_name) tuples
    visibility: str = 'public'  # Access modifier: 'public', 'private', or 'protected'
    line: int = 0
    column: int = 0

    def __repr__(self):
        return f"MultiDeclarationNode(declarations={self.declarations}, visibility={self.visibility})"

    def to_dict(self):
        return {
            'type': 'MultiDeclarationNode',
            'declarations': self.declarations,
            'visibility': self.visibility
        }


@dataclass
class ImportPyNode(ASTNode):
    """Represents an importpy statement."""
    module_name: str
    line: int = 0
    column: int = 0
    names: list = None  # None = whole module; [...] = selective names (importpy mod; A, B)

    def __repr__(self):
        if self.names:
            return f"ImportPyNode(module='{self.module_name}', names={self.names})"
        return f"ImportPyNode(module='{self.module_name}')"

    def to_dict(self):
        d = {'type': 'ImportPyNode', 'module_name': self.module_name}
        if self.names:
            d['names'] = self.names
        return d


@dataclass
class ImportNode(ASTNode):
    """Represents an import statement for Lyric modules."""
    module_name: str
    symbols: list = None  # List of (symbol_name, alias) tuples for selective imports
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        if self.symbols:
            symbols_str = ', '.join([f"{name} as {alias}" if alias else name for name, alias in self.symbols])
            return f"ImportNode(module='{self.module_name}', symbols=[{symbols_str}])"
        return f"ImportNode(module='{self.module_name}')"
    
    def to_dict(self):
        result = {
            'type': 'ImportNode',
            'module_name': self.module_name
        }
        if self.symbols:
            result['symbols'] = self.symbols
        return result


@dataclass
class RexNode(ASTNode):
    """Represents a regex literal."""
    pattern: str
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"RexNode(pattern='{self.pattern}')"
    
    def to_dict(self):
        return {
            'type': 'RexNode',
            'pattern': self.pattern
        }


@dataclass
class SliceNode(ASTNode):
    """Represents a slice operation: obj[start:end:step]."""
    obj: 'ASTNode'
    start: Optional['ASTNode'] = None
    end: Optional['ASTNode'] = None
    step: Optional['ASTNode'] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        start_str = str(self.start) if self.start else ""
        end_str = str(self.end) if self.end else ""
        step_str = f":{self.step}" if self.step else ""
        return f"SliceNode({self.obj}[{start_str}:{end_str}{step_str}])"
    
    def to_dict(self):
        return {
            'type': 'SliceNode',
            'obj': self.obj.to_dict() if self.obj else None,
            'start': self.start.to_dict() if self.start else None,
            'end': self.end.to_dict() if self.end else None,
            'step': self.step.to_dict() if self.step else None,
            'line': self.line,
            'column': self.column
        }


@dataclass
class FileOpNode(ASTNode):
    """Represents a file I/O operation: var > file, var >> file, var < file."""
    operator: str  # '>', '>>', or '<'
    left: 'ASTNode'  # Source variable or expression
    right: 'ASTNode'  # Target variable (usually a DskObject)
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"FileOpNode(left={self.left}, op='{self.operator}', right={self.right})"
    
    def to_dict(self):
        return {
            'type': 'FileOpNode',
            'operator': self.operator,
            'left': self.left.to_dict() if hasattr(self.left, 'to_dict') else str(self.left),
            'right': self.right.to_dict() if hasattr(self.right, 'to_dict') else str(self.right),
            'line': self.line,
            'column': self.column
        }


@dataclass
class ExecChainNode(ASTNode):
    """Represents a chain of exec() calls with pipe operators.
    
    Examples:
        exec('ls') | exec('grep test')
        exec('cmd') | print
        exec('cmd1') && exec('cmd2')
        print "text" | exec('grep x')
    """
    elements: List['ASTNode']  # List of CallNode (exec/print) or PrintNode
    operators: List[str]  # List of '|', '&&', '||' operators between elements
    input_source: Optional['ASTNode'] = None  # Optional <- input source
    output_target: Optional['ASTNode'] = None  # Optional -> output target
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        ops_str = ' '.join(self.operators)
        return f"ExecChainNode(elements={len(self.elements)}, ops=[{ops_str}])"
    
    def to_dict(self):
        return {
            'type': 'ExecChainNode',
            'elements': [e.to_dict() if hasattr(e, 'to_dict') else str(e) for e in self.elements],
            'operators': self.operators,
            'input_source': self.input_source.to_dict() if self.input_source and hasattr(self.input_source, 'to_dict') else None,
            'output_target': self.output_target.to_dict() if self.output_target and hasattr(self.output_target, 'to_dict') else None,
            'line': self.line,
            'column': self.column
        }


# Type alias for all AST nodes
ASTNode = Union[
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, ReturnNode, BreakNode, ContinueNode,
    ListLiteralNode, DictLiteralNode, IndexNode, SliceNode, TypeDeclarationNode, MultiDeclarationNode, PrintNode,
    TryNode, CatchClauseNode, RaiseNode, ImportPyNode, RexNode, FileOpNode, ExecChainNode
]