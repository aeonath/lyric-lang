# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Parser module for converting tokens to AST."""

from typing import List, Union
from lyric.lexer import Token, tokenize
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ClassNode, ReturnNode, BreakNode, ContinueNode,
    ListLiteralNode, TupleLiteralNode, DictLiteralNode, IndexNode, SliceNode, TypeDeclarationNode, MultiDeclarationNode, TryNode, CatchClauseNode, RaiseNode, ImportNode, ImportPyNode, FileOpNode, ExecChainNode
)
from lyric.errors import ParseError, SyntaxErrorLyric


class Parser:
    """Recursive descent parser for Lyric language."""

    # Compound assignment operator token types and their binary op equivalents
    COMPOUND_ASSIGN_TYPES = ('PLUS_ASSIGN', 'MINUS_ASSIGN', 'MULTIPLY_ASSIGN', 'DIVIDE_ASSIGN', 'PERCENT_ASSIGN')
    COMPOUND_ASSIGN_OPS = {
        'PLUS_ASSIGN': '+',
        'MINUS_ASSIGN': '-',
        'MULTIPLY_ASSIGN': '*',
        'DIVIDE_ASSIGN': '/',
        'PERCENT_ASSIGN': '%',
    }

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.loop_depth = 0  # Track nesting level for break/continue validation
        self.is_top_level = True  # Track if we're at module/top level
    
    def parse(self) -> ProgramNode:
        """Parse tokens into a ProgramNode."""
        statements = []
        # Preserve is_top_level if it was explicitly set (e.g., for interactive mode)
        # Otherwise, default to True for normal file parsing
        if not hasattr(self, '_interactive_mode'):
            self.is_top_level = True  # Start at top level by default
        
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return ProgramNode(statements)
    
    def _is_at_end(self) -> bool:
        """Check if we've reached the end of tokens."""
        return (self.current >= len(self.tokens) or 
                (self.current < len(self.tokens) and 
                 self.tokens[self.current].type == 'EOF'))
    
    def _peek(self) -> Token:
        """Look at the current token without advancing."""
        if self.current >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current]
    
    def _advance(self) -> Token:
        """Advance to the next token and return the previous one."""
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]
    
    def _check(self, *token_types: str) -> bool:
        """Check if current token matches any of the given types."""
        if self._is_at_end():
            return False
        return self._peek().type in token_types
    
    def _match(self, *token_types: str) -> bool:
        """Match and consume current token if it matches any of the given types."""
        if self._check(*token_types):
            self._advance()
            return True
        return False
    
    def _consume(self, token_type: str, message: str) -> Token:
        """Consume token of expected type or raise ParseError."""
        if self._check(token_type):
            return self._advance()
        raise ParseError(f"{message} at line {self._peek().line}, column {self._peek().col}")
    
    def _parse_statement(self):
        """Parse a single statement."""
        # Skip NEWLINE tokens
        while self._match('NEWLINE'):
            pass
        
        # If we're at EOF after skipping newlines, return None
        if self._is_at_end():
            return None
        
        # Check for visibility modifiers (PUBLIC, PRIVATE, PROTECTED)
        if self._check('PUBLIC', 'PRIVATE', 'PROTECTED'):
            # Could be method or variable declaration
            next_tok = self._peek_next()
            if next_tok.type in ('DEF', 'TYPE_OR_IDENT', 'VAR'):
                # Determine if it's a method or variable declaration
                if next_tok.type == 'DEF':
                    return self._parse_func_def()
                elif next_tok.type == 'VAR':
                    # Pattern: visibility var x, y
                    return self._parse_multi_declaration_with_visibility()
                elif next_tok.type == 'TYPE_OR_IDENT':
                    # Check if it's a typed method or variable declaration
                    next_next_tok = self._peek_next_next()
                    if next_next_tok.type == 'LPAREN':
                        # Pattern: visibility TYPE() - it's a method with no name? That's def funcname()
                        return self._parse_func_def()
                    elif next_next_tok.type == 'IDENT':
                        # Pattern: visibility TYPE IDENT
                        # Could be: visibility TYPE funcname() or visibility TYPE varname =
                        # Need to peek one more token
                        try:
                            third_tok_idx = self.current + 3
                            if third_tok_idx < len(self.tokens):
                                third_tok = self.tokens[third_tok_idx]
                                if third_tok.type == 'LPAREN':
                                    # It's a typed method: visibility TYPE funcname()
                                    return self._parse_func_def()
                                else:
                                    # It's a variable declaration: visibility TYPE varname =
                                    return self._parse_type_declaration_with_visibility()
                            else:
                                return self._parse_type_declaration_with_visibility()
                        except:
                            return self._parse_type_declaration_with_visibility()
                    elif next_next_tok.type in ('ASSIGN', 'COMMA'):
                        # It's a variable declaration
                        return self._parse_type_declaration_with_visibility()
                    else:
                        return self._parse_func_def()  # Default to method
        
        # Check for visibility modifiers as IDENT (backwards compatibility)
        if self._check('IDENT') and self._peek().value in ('public', 'private', 'protected'):
            # Peek ahead to see if this is followed by a method or variable definition
            next_tok = self._peek_next()
            if next_tok.type in ('DEF', 'TYPE_OR_IDENT'):
                # Check if it's a method or variable declaration
                if next_tok.type == 'DEF':
                    return self._parse_func_def()
                elif next_tok.type == 'TYPE_OR_IDENT':
                    # Check if it's a method or variable declaration
                    next_next_tok = self._peek_next_next()
                    if next_next_tok.type == 'LPAREN':
                        # It's a method
                        return self._parse_func_def()
                    elif next_next_tok.type in ('IDENT', 'ASSIGN', 'COMMA'):
                        # It's a variable declaration
                        return self._parse_type_declaration_with_visibility()
                    else:
                        return self._parse_func_def()  # Default to method
        
        # Check for typed function declaration: TYPE funcname(
        if self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT' and self._peek_next_next().type == 'LPAREN':
            return self._parse_func_def()
        # Reject old-style 'TYPE def funcname()' syntax — no longer valid
        elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'DEF':
            type_token = self._peek()
            raise ParseError(
                f"Invalid function syntax at line {type_token.line}: '{type_token.value} def' is not valid. "
                f"Use '{type_token.value} funcname()' for a typed function or 'def funcname()' for an untyped function."
            )
        # Check for untyped function: def funcname(
        elif self._check('DEF'):
            return self._parse_func_def()
        elif self._check('CLASS'):
            return self._parse_class_def()
        elif self._check('IF'):
            if self.is_top_level:
                token = self._peek()
                raise SyntaxErrorLyric(f"Control structures not allowed at module level. Only variable declarations, functions, and classes are allowed at the top level.", token.line, token.col)
            return self._parse_if_block()
        elif self._check('GIVEN'):
            if self.is_top_level:
                token = self._peek()
                raise SyntaxErrorLyric(f"Control structures not allowed at module level. Only variable declarations, functions, and classes are allowed at the top level.", token.line, token.col)
            return self._parse_loop_block()
        elif self._check('RETURN'):
            if self.is_top_level:
                token = self._peek()
                raise SyntaxErrorLyric(f"'return' statement not allowed at module level. Execution starts in main().", token.line, token.col)
            return self._parse_return_stmt()
        elif self._check('BREAK'):
            return self._parse_break_stmt()
        elif self._check('CONTINUE'):
            return self._parse_continue_stmt()
        elif self._check('TRY'):
            if self.is_top_level:
                token = self._peek()
                raise SyntaxErrorLyric(f"Control structures not allowed at module level. Only variable declarations, functions, and classes are allowed at the top level.", token.line, token.col)
            return self._parse_try_block()
        elif self._check('IMPORT'):
            return self._parse_import_stmt()
        elif self._check('IMPORTPY'):
            return self._parse_importpy_stmt()
        elif self._check('RAISE'):
            return self._parse_raise_stmt()
        elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT' and self._peek_next_next().type == 'COMMA':
            return self._parse_multi_declaration()
        elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT' and self._peek_next_next().type == 'ASSIGN':
            return self._parse_type_declaration()
        elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT':
            # Single variable declaration without assignment
            return self._parse_multi_declaration()
        elif self._check('IDENT') and self._peek_next().type == 'IDENT' and self._peek_next_next().type == 'COMMA':
            # Multi-declaration with invalid type - let multi-declaration parser handle the error
            return self._parse_multi_declaration()
        elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'ASSIGN':
            # Error: type keyword followed directly by assignment (missing variable name)
            type_token = self._advance()
            self._advance()  # consume '='
            raise ParseError(f"Expected variable name after type '{type_token.value}' at line {type_token.line}, column {type_token.col}")
        else:
            if self.is_top_level:
                token = self._peek()
                # Check if this might be a file operator statement before rejecting
                # File operators are allowed at top level for convenience
                if self._is_file_operator_ahead():
                    return self._parse_file_operator_stmt()
                raise SyntaxErrorLyric(f"Only variable declarations, functions, and classes are allowed at module level. Execution starts in main().", token.line, token.col)
            # Check for file operator statements: expr ->> expr, expr -> expr, expr <- expr
            # Let print statements handle their own file ops (print "text" ->> file)
            if self._is_file_operator_ahead() and not (self._check('IDENT') and self._peek().value == 'print'):
                return self._parse_file_operator_stmt()
            return self._parse_assignment_or_expr_stmt()
    
    def _parse_func_def(self) -> FunctionNode:
        """Parse function definition: [visibility] TYPE IDENT "(" param_list? ")" [":"] "{" statement* "}" 
           or: [visibility] def IDENT "(" param_list? ")" [":"] "{" statement* "}" """
        return_type = None
        visibility = 'public'  # Default visibility
        
        # Check for optional visibility modifier (PUBLIC, PRIVATE, PROTECTED tokens)
        if self._check('PUBLIC', 'PRIVATE', 'PROTECTED'):
            visibility_token = self._advance()
            visibility = visibility_token.type.lower()  # Convert PUBLIC to 'public', etc.
        # Also check for visibility as IDENT (backwards compatibility)
        elif self._check('IDENT'):
            next_token = self._peek()
            if next_token.value in ('public', 'private', 'protected'):
                visibility_token = self._advance()
                visibility = visibility_token.value
        
        # Check for new-style typed function: TYPE funcname(
        if self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT' and self._peek_next_next().type == 'LPAREN':
            type_token = self._advance()
            return_type = type_token.value.lower()
            name_token = self._advance()
            name = name_token.value
        # Reject old-style 'TYPE def funcname()' syntax — no longer valid
        elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'DEF':
            type_token = self._peek()
            raise ParseError(
                f"Invalid function syntax at line {type_token.line}: '{type_token.value} def' is not valid. "
                f"Use '{type_token.value} funcname()' for a typed function or 'def funcname()' for an untyped function."
            )
        # Untyped function: def funcname(
        else:
            def_token = self._consume('DEF', "Expected 'def'")
            name_token = self._consume('IDENT', "Expected function name")
            name = name_token.value
        
        self._consume('LPAREN', "Expected '(' after function name")
        
        params = []
        param_types = []
        if not self._check('RPAREN'):
            params, param_types = self._parse_param_list()
        
        self._consume('RPAREN', "Expected ')' after parameters")
        
        # Make colon optional after function signature
        self._match('COLON')  # Optional colon
        
        self._consume('LBRACE', "Expected '{' after function signature")
        
        # Save top-level state and set to False inside function body
        was_top_level = self.is_top_level
        self.is_top_level = False
        
        body_statements = []
        while not self._check('RBRACE') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('RBRACE'):
                break
            
            stmt = self._parse_statement()
            if stmt:
                body_statements.append(stmt)
        
        self._consume('RBRACE', "Expected '}' after function body")
        
        # Restore top-level state
        self.is_top_level = was_top_level
        
        # Use the line/col from whichever token started the function
        line = type_token.line if 'type_token' in locals() else (def_token.line if 'def_token' in locals() else name_token.line)
        col = type_token.col if 'type_token' in locals() else (def_token.col if 'def_token' in locals() else name_token.col)
        
        # Create FunctionNode with visibility
        func_node = FunctionNode(name, params, param_types, return_type, body_statements, visibility, line, col)
        return func_node
    
    def _parse_param_list(self) -> tuple[List[str], List[str]]:
        """Parse parameter list: (TYPE IDENT | IDENT) ("," (TYPE IDENT | IDENT))*"""
        params = []
        param_types = []
        
        # Parse first parameter
        if self._check('TYPE_OR_IDENT', 'IDENT'):
            if self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT':
                # Typed parameter: TYPE IDENT
                type_token = self._advance()
                param_token = self._advance()
                param_types.append(type_token.value.lower())
                params.append(param_token.value)
            elif self._check('TYPE_OR_IDENT') and self._peek_next().type == 'RPAREN':
                # Error: TYPE without parameter name
                type_token = self._advance()
                raise ParseError(
                    f"Expected parameter name after type '{type_token.value}' at line {type_token.line}, "
                    f"column {type_token.col}")
            else:
                # Untyped parameter: IDENT
                param_token = self._advance()
                param_types.append('var')  # Default to var type
                params.append(param_token.value)
            
            # Parse remaining parameters
            while self._match('COMMA'):
                if self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT':
                    # Typed parameter: TYPE IDENT
                    type_token = self._advance()
                    param_token = self._advance()
                    param_types.append(type_token.value.lower())
                    params.append(param_token.value)
                elif self._check('TYPE_OR_IDENT') and self._peek_next().type in ('RPAREN', 'COMMA'):
                    # Error: TYPE without parameter name
                    type_token = self._advance()
                    raise ParseError(
                        f"Expected parameter name after type '{type_token.value}' at line {type_token.line}, "
                        f"column {type_token.col}")
                elif self._check('IDENT'):
                    # Untyped parameter: IDENT
                    param_token = self._advance()
                    param_types.append('var')  # Default to var type
                    params.append(param_token.value)
                else:
                    raise ParseError(
                        f"Expected parameter name after ',' at line {self._peek().line}, "
                        f"column {self._peek().col}")
        
        return params, param_types
    
    def _parse_class_def(self) -> ClassNode:
        """Parse class definition: class IDENT [based on BASE_CLASS] [":"] statement* CLASS_END"""
        class_token = self._consume('CLASS', "Expected 'class'")
        
        name_token = self._consume('IDENT', "Expected class name")
        name = name_token.value
        
        # Check for inheritance: based on ClassName
        base_class = None
        if self._check('IDENT') and self._peek().value == 'based':
            self._advance()  # consume 'based'
            if not (self._check('IDENT') and self._peek().value == 'on'):
                raise ParseError(f"Expected 'on' after 'based' at line {self._peek().line}, column {self._peek().col}")
            self._advance()  # consume 'on'
            base_class_token = self._consume('IDENT', "Expected base class name after 'based on'")
            base_class = base_class_token.value
        
        # Make colon optional after class name/inheritance
        self._match('COLON')  # Optional colon
        
        # Save top-level state and set to False inside class body
        was_top_level = self.is_top_level
        self.is_top_level = False
        
        members_statements = []
        constructor_method = None
        
        while not self._check('CLASS_END') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('CLASS_END'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                # Check if this is a constructor method (method name matches class name)
                if isinstance(stmt, FunctionNode) and stmt.name == name:
                    if constructor_method is not None:
                        # Multiple constructors found - this is an error
                        raise ParseError(
                            f"Multiple constructors found for class '{name}'. Only one constructor method is allowed per class. "
                            f"Found constructor at line {constructor_method.line}, column {constructor_method.column} "
                            f"and another at line {stmt.line}, column {stmt.column}",
                            stmt.line, stmt.column
                        )
                    constructor_method = stmt
                else:
                    members_statements.append(stmt)
        
        self._consume('CLASS_END', "Expected '+++' after class body")
        
        # Restore top-level state
        self.is_top_level = was_top_level
        
        return ClassNode(name, members_statements, constructor_method, base_class, class_token.line, class_token.col)
    
    def _parse_if_block(self) -> IfNode:
        """Parse if block: if expression [":"] statement* ("else" "if" expression [":"] statement*)* ("else" [":"] statement*)? "end" """
        if_token = self._consume('IF', "Expected 'if'")
        
        condition = self._parse_expression()
        
        # Make colon optional after if condition
        self._match('COLON')  # Optional colon
        
        then_body = []
        while not self._check('ELSE', 'ELIF', 'END') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('ELSE', 'ELIF', 'END'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                then_body.append(stmt)
        
        elifs = []
        else_body = None
        
        while self._check('ELIF', 'ELSE'):
            # Handle elif keyword directly
            if self._match('ELIF'):
                # elif clause using 'elif' keyword
                elif_condition = self._parse_expression()
                
                # Make colon optional after elif condition
                self._match('COLON')  # Optional colon
                
                elif_body = []
                while not self._check('ELSE', 'ELIF', 'END') and not self._is_at_end():
                    # Skip NEWLINE tokens
                    while self._match('NEWLINE'):
                        pass
                    
                    if self._check('ELSE', 'ELIF', 'END'):
                        break
                        
                    stmt = self._parse_statement()
                    if stmt:
                        elif_body.append(stmt)
                
                elifs.append((elif_condition, elif_body))
            elif self._check('ELSE') and self._peek_next().type == 'IF':
                # 'else if' is deprecated - use 'elif' instead
                raise ParseError(
                    "Use 'elif' instead of 'else if'. 'else if' syntax has been removed for grammar clarity. "
                    f"at line {self._peek().line}, column {self._peek().col}"
                )
            else:
                # else clause - consume ELSE token here
                if not self._match('ELSE'):
                    break  # No else token, exit loop
                    
                # Make colon optional after else
                self._match('COLON')  # Optional colon
                
                else_body = []
                while not self._check('END') and not self._is_at_end():
                    # Skip NEWLINE tokens
                    while self._match('NEWLINE'):
                        pass
                    
                    if self._check('END'):
                        break
                        
                    stmt = self._parse_statement()
                    if stmt:
                        else_body.append(stmt)
                break
        
        self._consume('END', "Expected 'end' after if block")
        
        return IfNode(condition, then_body, elifs, else_body, if_token.line, if_token.col)
    
    def _parse_loop_block(self) -> LoopNode:
        """Parse loop block: given expression [":"] statement* "done" """
        given_token = self._consume('GIVEN', "Expected 'given'")

        iterator_var = None
        iterator_type = None

        # Handle "for int i in range(3)" pattern — typed inline declaration
        if self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT' and self._peek_at(2).type == 'IN':
            type_token = self._advance()        # consume type (e.g., "int")
            iterator_type = type_token.value
            iterator_var = self._advance().value # consume identifier (e.g., "i")
            self._consume('IN', "Expected 'in'")
            iterable = self._parse_expression()
            condition_or_iter = iterable
            loop_kind = "iterator"
        # Handle "for i in range(3)" pattern — bare identifier
        elif self._check('IDENT') and self._peek_next().type == 'IN':
            iterator_var = self._advance().value  # consume identifier
            self._consume('IN', "Expected 'in'")
            iterable = self._parse_expression()
            condition_or_iter = iterable
            loop_kind = "iterator"
        else:
            # While pattern: given x > 0:
            condition_or_iter = self._parse_expression()
            loop_kind = "while"
        
        # Make colon optional after given expression
        self._match('COLON')  # Optional colon
        
        # Increment loop depth for break/continue validation
        self.loop_depth += 1
        
        body = []
        while not self._check('DONE') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('DONE'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        
        # Decrement loop depth
        self.loop_depth -= 1
        
        self._consume('DONE', "Expected 'done' after loop body")
        
        return LoopNode(condition_or_iter, loop_kind, body, iterator_var, iterator_type, given_token.line, given_token.col)
    
    def _parse_assignment_or_expr_stmt(self):
        """Parse assignment or expression statement."""
        # Note: Don't check for exec chain here, as they can be part of assignments
        # They'll be parsed as expressions and handled by assignment logic
        
        if self._check('IDENT', 'TYPE_OR_IDENT'):
            # Check for print statement syntax: print <expr>
            if (self._peek().value == 'print' and 
                self._peek_next().type != 'LPAREN' and 
                not self._check('NEWLINE') and 
                not self._check('EOF')):
                # Parse print <expr> syntax (single or multiple arguments)
                print_token = self._advance()
                args = []
                
                # Parse first expression
                expr = self._parse_expression()
                args.append(expr)
                
                # Parse additional expressions separated by commas
                while self._match('COMMA'):
                    expr = self._parse_expression()
                    args.append(expr)
                
                # Check if a file operator follows: print "text" ->> file
                if self._check('FILE_APPEND', 'FILE_WRITE', 'FILE_READ'):
                    if self._check('FILE_APPEND'):
                        self._advance()
                        operator = '->>'
                    elif self._check('FILE_WRITE'):
                        self._advance()
                        operator = '->'
                    else:
                        self._advance()
                        operator = '<-'
                    right = self._parse_expression()
                    return FileOpNode(operator=operator, left=CallNode('print', args, print_token.line, print_token.col), right=right, line=print_token.line, column=print_token.col)

                # Create CallNode with arguments to match print(<expr>) AST
                return CallNode('print', args, print_token.line, print_token.col)
            
            # Check if it's an assignment
            elif self._peek_next().type == 'ASSIGN':
                # Assignment: IDENT "=" expression
                name_token = self._advance()
                name = name_token.value
                
                self._advance()  # consume '='
                expr = self._parse_expression()
                
                return AssignNode(name, expr, name_token.line, name_token.col)
            elif self._peek_next().type in self.COMPOUND_ASSIGN_TYPES:
                # Compound assignment: x += expr → x = x + expr
                name_token = self._advance()
                name = name_token.value
                op_token = self._advance()  # consume compound operator
                op = self.COMPOUND_ASSIGN_OPS[op_token.type]
                expr = self._parse_expression()
                desugared = BinaryOpNode(op, IdentifierNode(name, name_token.line, name_token.col), expr, name_token.line, name_token.col)
                return AssignNode(name, desugared, name_token.line, name_token.col)
            elif (self._peek_next().type == 'DOT' and
                  self._peek_next_next().type == 'IDENT' and
                  self._peek_next_next_next().type == 'ASSIGN'):
                # Assignment to member: obj.attr = expression
                obj_token = self._advance()
                obj_name = obj_token.value
                self._advance()  # consume '.'
                member_name = self._advance().value
                self._advance()  # consume '='
                
                full_name = f"{obj_name}.{member_name}"
                expr = self._parse_expression()
                
                return AssignNode(full_name, expr, obj_token.line, obj_token.col)
            elif (self._peek_next().type == 'DOT' and
                  self._peek_next_next().type == 'IDENT' and
                  self._peek_next_next_next().type in self.COMPOUND_ASSIGN_TYPES):
                # Compound member assignment: obj.attr += expr → obj.attr = obj.attr + expr
                obj_token = self._advance()
                obj_name = obj_token.value
                self._advance()  # consume '.'
                member_name = self._advance().value
                op_token = self._advance()  # consume compound operator
                op = self.COMPOUND_ASSIGN_OPS[op_token.type]

                full_name = f"{obj_name}.{member_name}"
                ident = IdentifierNode(full_name, obj_token.line, obj_token.col)
                expr = self._parse_expression()
                desugared = BinaryOpNode(op, ident, expr, obj_token.line, obj_token.col)
                return AssignNode(full_name, desugared, obj_token.line, obj_token.col)
            elif (self._peek_next().type == 'DOT' and
                  self._peek_next_next().type == 'IDENT' and
                  self._peek_at(3).type == 'LBRACKET' and
                  self._peek_at(4).type in ('STRING', 'INT', 'FLOAT', 'IDENT') and
                  self._peek_at(5).type == 'RBRACKET' and
                  self._peek_at(6).type == 'ASSIGN'):
                # Member+index assignment: obj.member[key] = expression
                obj_token = self._advance()
                obj_name = obj_token.value
                self._advance()  # consume '.'
                member_name = self._advance().value
                self._advance()  # consume '['
                index_token = self._advance()
                self._advance()  # consume ']'
                self._advance()  # consume '='

                full_name = f"{obj_name}.{member_name}"
                index_expr = LiteralNode(index_token.value) if index_token.type != 'IDENT' else IdentifierNode(index_token.value, index_token.line, index_token.col)
                indexed_expr = IndexNode(IdentifierNode(full_name, obj_token.line, obj_token.col), index_expr)
                expr = self._parse_expression()
                return AssignNode(f"{full_name}[{index_token.value}]", expr, obj_token.line, obj_token.col)
            elif (self._peek_next().type == 'DOT' and
                  self._peek_next_next().type == 'IDENT' and
                  self._peek_at(3).type == 'LBRACKET' and
                  self._peek_at(4).type in ('STRING', 'INT', 'FLOAT', 'IDENT') and
                  self._peek_at(5).type == 'RBRACKET' and
                  self._peek_at(6).type in self.COMPOUND_ASSIGN_TYPES):
                # Compound member+index assignment: obj.member[key] += expr
                obj_token = self._advance()
                obj_name = obj_token.value
                self._advance()  # consume '.'
                member_name = self._advance().value
                self._advance()  # consume '['
                index_token = self._advance()
                self._advance()  # consume ']'
                op_token = self._advance()  # consume compound operator
                op = self.COMPOUND_ASSIGN_OPS[op_token.type]

                full_name = f"{obj_name}.{member_name}"
                index_expr = LiteralNode(index_token.value) if index_token.type != 'IDENT' else IdentifierNode(index_token.value, index_token.line, index_token.col)
                indexed_expr = IndexNode(IdentifierNode(full_name, obj_token.line, obj_token.col), index_expr)
                expr = self._parse_expression()
                desugared = BinaryOpNode(op, indexed_expr, expr, obj_token.line, obj_token.col)
                return AssignNode(f"{full_name}[{index_token.value}]", desugared, obj_token.line, obj_token.col)
            elif (self._peek_next().type == 'LBRACKET' and
                  self._peek_next_next().type in ('STRING', 'INT', 'FLOAT', 'IDENT') and
                  self._peek_next_next_next().type == 'RBRACKET' and
                  self._peek_next_next_next_next().type == 'ASSIGN'):
                # Assignment to indexed expression: obj[index] = expression
                obj_token = self._advance()
                obj_name = obj_token.value
                self._advance()  # consume '['
                index_token = self._advance()
                self._advance()  # consume ']'
                self._advance()  # consume '='
                
                # Create the indexed assignment
                index_expr = LiteralNode(index_token.value) if index_token.type != 'IDENT' else IdentifierNode(index_token.value, index_token.line, index_token.col)
                indexed_expr = IndexNode(IdentifierNode(obj_name), index_expr)
                expr = self._parse_expression()
                
                return AssignNode(f"{obj_name}[{index_token.value}]", expr, obj_token.line, obj_token.col)
            elif (self._peek_next().type == 'LBRACKET' and
                  self._peek_next_next().type in ('STRING', 'INT', 'FLOAT', 'IDENT') and
                  self._peek_next_next_next().type == 'RBRACKET' and
                  self._peek_next_next_next_next().type in self.COMPOUND_ASSIGN_TYPES):
                # Compound index assignment: arr[i] += expr → arr[i] = arr[i] + expr
                obj_token = self._advance()
                obj_name = obj_token.value
                self._advance()  # consume '['
                index_token = self._advance()
                self._advance()  # consume ']'
                op_token = self._advance()  # consume compound operator
                op = self.COMPOUND_ASSIGN_OPS[op_token.type]

                index_expr = LiteralNode(index_token.value) if index_token.type != 'IDENT' else IdentifierNode(index_token.value, index_token.line, index_token.col)
                indexed_expr = IndexNode(IdentifierNode(obj_name), index_expr)
                expr = self._parse_expression()
                desugared = BinaryOpNode(op, indexed_expr, expr, obj_token.line, obj_token.col)
                return AssignNode(f"{obj_name}[{index_token.value}]", desugared, obj_token.line, obj_token.col)
            # Check for file operator statements
            elif self._peek_next().type in ('FILE_APPEND', 'FILE_WRITE', 'FILE_READ'):
                return self._parse_file_operator_stmt()
        
        # Expression statement
        return self._parse_expression()
    
    def _parse_return_stmt(self) -> ReturnNode:
        """Parse return statement: return expression? """
        return_token = self._consume('RETURN', "Expected 'return'")
        
        value = None
        if not self._check('NEWLINE') and not self._check('EOF'):
            value = self._parse_expression()
        
        return ReturnNode(value, return_token.line, return_token.col)
    
    def _parse_break_stmt(self) -> BreakNode:
        """Parse break statement: break """
        break_token = self._consume('BREAK', "Expected 'break'")
        
        # Validate that break is used within a loop context
        if self.loop_depth == 0:
            raise ParseError(f"'break' used outside of loop at line {break_token.line}, column {break_token.col}")
        
        return BreakNode(break_token.line, break_token.col)
    
    def _parse_continue_stmt(self) -> ContinueNode:
        """Parse continue statement: continue """
        continue_token = self._consume('CONTINUE', "Expected 'continue'")
        
        # Validate that continue is used within a loop context
        if self.loop_depth == 0:
            raise ParseError(f"'continue' used outside of loop at line {continue_token.line}, column {continue_token.col}")
        
        return ContinueNode(continue_token.line, continue_token.col)
    
    def _parse_expression(self):
        """Parse an expression with proper precedence."""
        return self._parse_logical_or()
    
    def _parse_logical_or(self):
        """Parse logical OR expressions."""
        expr = self._parse_logical_and()
        
        while self._match('OR'):
            operator = self._previous().value
            right = self._parse_logical_and()
            expr = BinaryOpNode(operator, expr, right)
        
        return expr
    
    def _parse_logical_and(self):
        """Parse logical AND expressions."""
        expr = self._parse_equality()
        
        while self._match('AND'):
            operator = self._previous().value
            right = self._parse_equality()
            line, col = self._get_position_from_token(self._previous())
            expr = BinaryOpNode(operator, expr, right, line, col)
        
        return expr
    
    def _parse_equality(self):
        """Parse equality expressions (==, !=)."""
        expr = self._parse_comparison()
        
        while self._match('==', '!='):
            operator = self._previous().value
            right = self._parse_comparison()
            line, col = self._get_position_from_token(self._previous())
            expr = BinaryOpNode(operator, expr, right, line, col)
        
        return expr
    
    def _parse_comparison(self):
        """Parse comparison expressions (<, <=, >, >=, in)."""
        expr = self._parse_term()
        
        while self._match('LT', '<=', 'GT', '>=', 'IN'):
            operator = self._previous().value
            right = self._parse_term()
            line, col = self._get_position_from_token(self._previous())
            expr = BinaryOpNode(operator, expr, right, line, col)
        
        return expr
    
    def _parse_term(self):
        """Parse addition and subtraction."""
        expr = self._parse_factor()
        
        while self._match('PLUS', 'MINUS'):
            operator = self._previous().value
            right = self._parse_factor()
            line, col = self._get_position_from_token(self._previous())
            expr = BinaryOpNode(operator, expr, right, line, col)
        
        return expr
    
    def _parse_factor(self):
        """Parse multiplication and division."""
        expr = self._parse_unary()
        
        while self._match('MULTIPLY', 'DIVIDE', 'PERCENT'):
            operator = self._previous().value
            right = self._parse_unary()
            line, col = self._get_position_from_token(self._previous())
            expr = BinaryOpNode(operator, expr, right, line, col)
        
        return expr
    
    def _parse_unary(self):
        """Parse unary expressions (-, !)."""
        if self._match('MINUS', 'NOT'):
            operator = self._previous().value
            right = self._parse_unary()
            line, col = self._get_position_from_token(self._previous())
            return UnaryOpNode(operator, right, line, col)
        
        return self._parse_exec_chain_or_primary()
    
    def _parse_exec_chain_or_primary(self):
        """Parse exec chains or primary expressions."""
        # Parse the first element
        expr = self._parse_primary()
        
        # Check if this is the start of an exec chain
        if isinstance(expr, CallNode) and expr.func_name == 'exec':
            # Check if followed by pipe operators
            if self._check('PIPE', 'AND', 'OR'):
                # This is an exec chain! Parse it as such
                elements = [expr]
                operators = []
                
                while self._check('PIPE', 'AND', 'OR'):
                    op_token = self._advance()
                    if op_token.type == 'PIPE':
                        operators.append('|')
                    elif op_token.type == 'AND':
                        operators.append('&&')
                    elif op_token.type == 'OR':
                        operators.append('||')
                    
                    # Parse next element (should be exec() or print)
                    next_elem = self._parse_exec_chain_element()
                    elements.append(next_elem)
                
                # Create ExecChainNode
                return ExecChainNode(
                    elements=elements,
                    operators=operators,
                    input_source=None,
                    output_target=None,
                    line=expr.line,
                    column=expr.column
                )
        
        return expr
    
    def _parse_primary(self):
        """Parse primary expressions."""
        if self._match('INT', 'FLOAT'):
            token = self._previous()
            return LiteralNode(token.value, token.line, token.col)
        
        if self._match('STRING'):
            token = self._previous()
            return LiteralNode(token.value, token.line, token.col)
        
        if self._match('BOOLEAN'):
            token = self._previous()
            return LiteralNode(token.value, token.line, token.col)
        
        if self._match('NONE'):
            token = self._previous()
            return LiteralNode(None, token.line, token.col)
        
        if self._match('IDENT', 'TYPE_OR_IDENT'):
            name_token = self._previous()
            name = name_token.value
            
            # Check if it's a function call
            if self._match('LPAREN'):
                args = []
                if not self._check('RPAREN'):
                    args = self._parse_argument_list()
                
                self._consume('RPAREN', "Expected ')' after arguments")
                return CallNode(name, args, name_token.line, name_token.col)
            
            # Handle member access: obj.member
            if self._match('DOT'):
                member_name = self._consume('IDENT', "Expected member name after '.'").value
                full_name = f"{name}.{member_name}"
                
                # Handle chained member access: obj.member.member
                while self._match('DOT'):
                    next_member = self._consume('IDENT', "Expected member name after '.'").value
                    full_name = f"{full_name}.{next_member}"
                
                # Check if it's a method call: obj.method()
                if self._match('LPAREN'):
                    args = []
                    if not self._check('RPAREN'):
                        args = self._parse_argument_list()

                    self._consume('RPAREN', "Expected ')' after arguments")
                    return self._parse_indexing_chain(CallNode(full_name, args, name_token.line, name_token.col))

                # Support indexing on member access: module.arr_var[0]
                return self._parse_indexing_chain(IdentifierNode(full_name, name_token.line, name_token.col))
            
            # Start with identifier and check for indexing
            expr = IdentifierNode(name, name_token.line, name_token.col)
            return self._parse_indexing_chain(expr)
        
        if self._match('LPAREN'):
            lparen_token = self._previous()
            # Empty tuple: ()
            if self._check('RPAREN'):
                self._advance()
                return self._parse_indexing_chain(TupleLiteralNode([], lparen_token.line, lparen_token.col))
            first_expr = self._parse_expression()
            if self._match('COMMA'):
                # Tuple literal: (expr, ...) or single-element (expr,)
                elements = [first_expr]
                while not self._check('RPAREN') and not self._check('EOF'):
                    while self._match('NEWLINE'):
                        pass
                    if self._check('RPAREN'):
                        break  # trailing comma allowed
                    elements.append(self._parse_expression())
                    if not self._match('COMMA'):
                        break
                while self._match('NEWLINE'):
                    pass
                self._consume('RPAREN', "Expected ')' after tuple elements")
                return self._parse_indexing_chain(TupleLiteralNode(elements, lparen_token.line, lparen_token.col))
            else:
                # Grouping expression: (expr)
                self._consume('RPAREN', "Expected ')' after expression")
                first_expr.line, first_expr.column = lparen_token.line, lparen_token.col
                return self._parse_indexing_chain(first_expr)
        
        if self._match('LBRACKET'):
            # List literal: [ expression* ]
            lbracket_token = self._previous()
            elements = []
            if not self._check('RBRACKET'):
                # Skip NEWLINE tokens
                while self._match('NEWLINE'):
                    pass
                
                elements.append(self._parse_expression())
                while self._match('COMMA'):
                    # Skip NEWLINE tokens
                    while self._match('NEWLINE'):
                        pass
                    elements.append(self._parse_expression())
            
            # Skip NEWLINE tokens before closing bracket
            while self._match('NEWLINE'):
                pass
            
            self._consume('RBRACKET', "Expected ']' after list elements")
            return self._parse_indexing_chain(ListLiteralNode(elements, lbracket_token.line, lbracket_token.col))
        
        if self._match('LBRACE'):
            # Dictionary literal: { key: value, ... }
            lbrace_token = self._previous()
            pairs = []
            if not self._check('RBRACE'):
                # Skip NEWLINE tokens
                while self._match('NEWLINE'):
                    pass
                
                # Parse first key-value pair
                key = self._parse_expression()
                self._consume('COLON', "Expected ':' after dictionary key")
                value = self._parse_expression()
                pairs.append((key, value))
                
                # Parse remaining pairs
                while self._match('COMMA'):
                    # Skip NEWLINE tokens
                    while self._match('NEWLINE'):
                        pass
                    key = self._parse_expression()
                    self._consume('COLON', "Expected ':' after dictionary key")
                    value = self._parse_expression()
                    pairs.append((key, value))
            
            # Skip NEWLINE tokens before closing brace
            while self._match('NEWLINE'):
                pass
            
            self._consume('RBRACE', "Expected '}' after dictionary pairs")
            return self._parse_indexing_chain(DictLiteralNode(pairs, lbrace_token.line, lbrace_token.col))
        
        token = self._peek()
        hints = {
            'LBRACE': "Unexpected '{'. Classes use '+++' as the closing delimiter, not braces. Braces are only used for function/method bodies.",
            'RBRACE': "Unexpected '}'. Check for mismatched braces in your function or method body.",
            'CLASS_END': "Unexpected '+++'. This class terminator appears outside of a class definition.",
            'END': "Unexpected 'end'. Check that your block structure is correct.",
            'DONE': "Unexpected 'done'. This loop terminator appears outside of a loop.",
            'FADE': "Unexpected 'fade'. This try/catch terminator appears outside of a try block.",
            'PLUS_ASSIGN': "Unexpected '+='. Compound assignment can only be used as a statement, not inside an expression.",
            'MINUS_ASSIGN': "Unexpected '-='. Compound assignment can only be used as a statement, not inside an expression.",
            'MULTIPLY_ASSIGN': "Unexpected '*='. Compound assignment can only be used as a statement, not inside an expression.",
            'DIVIDE_ASSIGN': "Unexpected '/='. Compound assignment can only be used as a statement, not inside an expression.",
            'PERCENT_ASSIGN': "Unexpected '%='. Compound assignment can only be used as a statement, not inside an expression.",
            'EOF': "Unexpected end of file. Check for unclosed blocks, missing 'end', 'done', 'fade', or '+++'.",
            'ASSIGN': "Unexpected '='. Did you mean '==' for comparison?",
        }
        hint = hints.get(token.type)
        if hint:
            raise SyntaxErrorLyric(hint, token.line, token.col)
        raise SyntaxErrorLyric(
            f"Unexpected token '{token.value}' (type: {token.type}). Expected an expression (variable, literal, function call, etc.).",
            token.line, token.col
        )
    
    def _parse_indexing_chain(self, expr):
        """Parse chained indexing operations: expr[index][index]... or expr[start:end:step]..."""
        while self._match('LBRACKET'):
            lbracket_token = self._previous()
            
            # Check if this is slicing syntax (contains colons)
            # Look ahead to see if there's a colon in the bracket
            is_slice = False
            temp_pos = self.current
            while temp_pos < len(self.tokens) and self.tokens[temp_pos].type != 'RBRACKET':
                if self.tokens[temp_pos].type == 'COLON':
                    is_slice = True
                    break
                temp_pos += 1
            
            if is_slice:
                # Parse slice: [start:end:step]
                start = None
                end = None
                step = None
                
                # Parse start (if present)
                if not self._check('COLON'):
                    start = self._parse_expression()
                
                # Parse first colon
                if self._match('COLON'):
                    # Parse end (if present)
                    if not self._check('COLON', 'RBRACKET'):
                        end = self._parse_expression()
                    
                    # Parse second colon and step (if present)
                    if self._match('COLON'):
                        if not self._check('RBRACKET'):
                            step = self._parse_expression()
                
                self._consume('RBRACKET', "Expected ']' after slice")
                expr = SliceNode(expr, start, end, step, lbracket_token.line, lbracket_token.col)
            else:
                # Parse simple index: [index]
                index = self._parse_expression()
                self._consume('RBRACKET', "Expected ']' after index")
                expr = IndexNode(expr, index, lbracket_token.line, lbracket_token.col)
        
        return expr
    
    def _parse_argument_list(self) -> List:
        """Parse argument list: expression ("," expression)*"""
        args = []
        
        args.append(self._parse_expression())
        
        while self._match('COMMA'):
            args.append(self._parse_expression())
        
        return args
    
    def _parse_type_declaration(self) -> TypeDeclarationNode:
        """Parse type declaration: TYPE IDENT "=" expression"""
        type_token = self._advance()  # Consume the type token (INT, STR, FLT, VAR)
        type_name = type_token.value.lower()  # Convert to lowercase (int, str, flt, var)
        
        name_token = self._consume('IDENT', "Expected variable name after type")
        name = name_token.value
        
        self._consume('ASSIGN', "Expected '=' after variable name")
        
        expr = self._parse_expression()
        
        return TypeDeclarationNode(type_name, name, expr)
    
    def _previous(self) -> Token:
        """Get the previous token."""
        return self.tokens[self.current - 1]
    
    def _get_position_from_token(self, token: Token) -> tuple[int, int]:
        """Get line and column position from a token."""
        return (token.line, token.col)
    
    def _peek_next(self) -> Token:
        """Look at the next token without advancing."""
        if self.current + 1 >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current + 1]
    
    def _peek_next_next(self) -> Token:
        """Look at the token after next without advancing."""
        if self.current + 2 >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current + 2]
    
    def _peek_next_next_next(self) -> Token:
        """Look at the token after next next without advancing."""
        if self.current + 3 >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current + 3]
    
    def _peek_next_next_next_next(self) -> Token:
        """Look at the token 4 positions ahead without advancing."""
        if self.current + 4 >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current + 4]

    def _peek_at(self, offset: int) -> Token:
        """Look at the token at the given offset from current without advancing."""
        if self.current + offset >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current + offset]

    def _parse_try_block(self) -> TryNode:
        """Parse try/catch/finally block: try [":"] ... catch [Type] [as var] [":"] ... finally [":"] ... fade"""
        try_token = self._consume('TRY', "Expected 'try'")
        
        # Make colon optional after try
        self._match('COLON')  # Optional colon
        
        # Parse try body
        try_body = []
        while not self._check('CATCH', 'FINALLY', 'FADE') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('CATCH', 'FINALLY', 'FADE'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                try_body.append(stmt)
        
        # Parse catch clauses (multiple allowed)
        catch_clauses = []
        while self._match('CATCH'):
            catch_clause = self._parse_catch_clause()
            catch_clauses.append(catch_clause)
        
        # Parse finally block (optional)
        finally_body = None
        if self._match('FINALLY'):
            # Make colon optional after finally
            self._match('COLON')  # Optional colon
            
            finally_body = []
            while not self._check('FADE') and not self._is_at_end():
                # Skip NEWLINE tokens
                while self._match('NEWLINE'):
                    pass
                
                if self._check('FADE'):
                    break
                    
                stmt = self._parse_statement()
                if stmt:
                    finally_body.append(stmt)
        
        # Consume fade
        self._consume('FADE', "Expected 'fade' to end try block")
        
        # Validate: try without catch is a syntax error
        if not catch_clauses:
            raise ParseError("try block must have at least one catch block at line {}, column {}".format(
                self._peek().line, self._peek().col))
        
        return TryNode(try_body, catch_clauses, finally_body, try_token.line, try_token.col)
    
    def _parse_catch_clause(self) -> CatchClauseNode:
        """Parse a single catch clause: catch [Type] [as identifier] [":"] ... """
        exception_type = None
        variable_name = None
        
        # Check for exception type (IDENT after CATCH)
        if self._check('IDENT'):
            exception_type = self._advance().value
        
        # Check for 'as' keyword
        if self._match('AS'):
            if self._check('IDENT'):
                variable_name = self._advance().value
            else:
                raise ParseError("Expected variable name after 'as' at line {}, column {}".format(
                    self._peek().line, self._peek().col))
        
        # Make colon optional after catch
        self._match('COLON')  # Optional colon
        
        # Parse catch body
        catch_body = []
        while not self._check('CATCH', 'FINALLY', 'FADE') and not self._is_at_end():
            # Skip NEWLINE tokens
            while self._match('NEWLINE'):
                pass
            
            if self._check('CATCH', 'FINALLY', 'FADE'):
                break
                
            stmt = self._parse_statement()
            if stmt:
                catch_body.append(stmt)
        
        return CatchClauseNode(exception_type, variable_name, catch_body, self._peek().line, self._peek().col)

    def _parse_raise_stmt(self) -> RaiseNode:
        """Parse raise statement: raise ExceptionName"""
        raise_token = self._consume('RAISE', "Expected 'raise'")
        
        # Parse exception name
        exception_token = self._consume('IDENT', "Expected exception name after 'raise'")
        exception_name = exception_token.value
        
        return RaiseNode(exception_name, raise_token.line, raise_token.col)

    def _parse_type_declaration_with_visibility(self) -> Union[TypeDeclarationNode, MultiDeclarationNode]:
        """Parse type declaration with visibility modifier: [visibility] TYPE IDENT "=" expression or [visibility] TYPE IDENT, TYPE IDENT"""
        visibility = 'public'  # Default
        
        # Check for visibility modifier (PUBLIC, PRIVATE, PROTECTED tokens)
        if self._check('PUBLIC', 'PRIVATE', 'PROTECTED'):
            visibility_token = self._advance()
            visibility = visibility_token.type.lower()  # Convert PUBLIC to 'public', etc.
        # Also check for visibility as IDENT (backwards compatibility)
        elif self._check('IDENT'):
            next_token = self._peek()
            if next_token.value in ('public', 'private', 'protected'):
                visibility_token = self._advance()
                visibility = visibility_token.value
        
        # Now check if it's a multi-declaration or single declaration
        if self._check('TYPE_OR_IDENT') and self._peek_next().type == 'IDENT':
            next_next = self._peek_next_next()
            if next_next.type == 'COMMA':
                # Multi-declaration
                return self._parse_multi_declaration_internal(visibility)
            elif next_next.type == 'ASSIGN':
                # Single declaration with assignment
                return self._parse_type_declaration_internal(visibility)
            else:
                # Single declaration without assignment
                return self._parse_multi_declaration_internal(visibility)
        elif self._check('TYPE_OR_IDENT'):
            # Could be just a type without variable name, or untyped var declaration
            # This handles cases like "private var" where we need to parse the full multi-decl
            return self._parse_multi_declaration_internal(visibility)
        else:
            raise ParseError(f"Expected type after visibility modifier at line {self._peek().line}, column {self._peek().col}")
    
    def _parse_multi_declaration_with_visibility(self) -> MultiDeclarationNode:
        """Parse multi-declaration with visibility modifier: [visibility] var x, y, z"""
        visibility = 'public'  # Default
        
        # Check for visibility modifier (PUBLIC, PRIVATE, PROTECTED tokens)
        if self._check('PUBLIC', 'PRIVATE', 'PROTECTED'):
            visibility_token = self._advance()
            visibility = visibility_token.type.lower()  # Convert PUBLIC to 'public', etc.
        # Also check for visibility as IDENT (backwards compatibility)
        elif self._check('IDENT'):
            next_token = self._peek()
            if next_token.value in ('public', 'private', 'protected'):
                visibility_token = self._advance()
                visibility = visibility_token.value
        
        # Now parse the multi-declaration
        return self._parse_multi_declaration_internal(visibility)
    
    def _parse_type_declaration_internal(self, visibility: str = 'public') -> TypeDeclarationNode:
        """Internal method to parse type declaration with given visibility."""
        type_token = self._advance()
        type_name = type_token.value.lower()
        
        # Validate that pyobject is not allowed as explicit type declaration
        if type_name == 'pyobject':
            raise ParseError(f"Type 'pyobject' is internal only and cannot be used in explicit declarations at line {type_token.line}, column {type_token.col}")
        
        # Validate that the type is a known type
        valid_types = {'int', 'str', 'flt', 'var', 'rex', 'god', 'bin', 'arr', 'map', 'obj', 'dsk', 'tup'}
        if type_name not in valid_types:
            raise ParseError(f"Unknown type '{type_name}' at line {type_token.line}, column {type_token.col}. Valid types are: {', '.join(valid_types)}")
        
        name_token = self._consume('IDENT', "Expected variable name after type")
        name = name_token.value
        
        self._consume('ASSIGN', "Expected '=' after variable name")
        expr = self._parse_expression()
        
        return TypeDeclarationNode(type_name, name, expr, visibility, type_token.line, type_token.col)
    
    def _parse_multi_declaration_internal(self, visibility: str = 'public') -> MultiDeclarationNode:
        """Internal method to parse multi-declaration with given visibility."""
        declarations = []
        line = self._peek().line
        column = self._peek().col
        
        while True:
            # Parse type and variable name
            if not self._check('TYPE_OR_IDENT', 'VAR'):
                raise ParseError(f"Expected type in variable declaration at line {self._peek().line}, column {self._peek().col}")
            
            type_token = self._advance()
            type_name = type_token.value.lower() if type_token.type == 'TYPE_OR_IDENT' else 'var'
            
            # Validate that pyobject is not allowed
            if type_name == 'pyobject':
                raise ParseError(f"Type 'pyobject' is internal only and cannot be used in explicit declarations at line {type_token.line}, column {type_token.col}")
            
            # Validate that the type is a known type
            valid_types = {'int', 'str', 'flt', 'var', 'rex', 'god', 'bin', 'arr', 'map', 'obj', 'dsk', 'tup'}
            if type_name not in valid_types:
                raise ParseError(f"Unknown type '{type_name}' at line {type_token.line}, column {type_token.col}. Valid types are: {', '.join(valid_types)}")
            
            if not self._check('IDENT'):
                raise ParseError(f"Expected variable name after type '{type_name}' at line {self._peek().line}, column {self._peek().col}")
            
            name_token = self._advance()
            name = name_token.value
            
            declarations.append((type_name, name))
            
            # Check for comma (more declarations) or end
            if self._match('COMMA'):
                continue
            else:
                break
        
        return MultiDeclarationNode(declarations, visibility, line, column)

    def _parse_type_declaration(self) -> TypeDeclarationNode:
        """Parse type declaration: TYPE IDENT "=" expression"""
        type_token = self._advance()
        type_name = type_token.value.lower()
        
        # Validate that pyobject is not allowed as explicit type declaration
        if type_name == 'pyobject':
            raise ParseError(f"Type 'pyobject' is internal only and cannot be used in explicit declarations at line {type_token.line}, column {type_token.col}")
        
        # Validate that the type is a known type
        valid_types = {'int', 'str', 'flt', 'var', 'rex', 'god', 'bin', 'arr', 'map', 'obj', 'dsk', 'tup'}
        if type_name not in valid_types:
            raise ParseError(f"Unknown type '{type_name}' at line {type_token.line}, column {type_token.col}. Valid types are: {', '.join(valid_types)}")
        
        name_token = self._consume('IDENT', "Expected variable name after type")
        name = name_token.value
        
        self._consume('ASSIGN', "Expected '=' after variable name")
        expr = self._parse_expression()
        
        return TypeDeclarationNode(type_name, name, expr, 'public', type_token.line, type_token.col)
    
    def _parse_multi_declaration(self) -> MultiDeclarationNode:
        """Parse multi-variable declaration: TYPE IDENT "," TYPE IDENT "," ... """
        declarations = []
        line = self._peek().line
        column = self._peek().col
        
        while True:
            # Parse type and variable name
            # Handle both TYPE_OR_IDENT and IDENT (for invalid types)
            if self._check('TYPE_OR_IDENT'):
                type_token = self._consume('TYPE_OR_IDENT', "Expected type keyword")
            else:
                type_token = self._consume('IDENT', "Expected type keyword")
            
            type_name = type_token.value.lower()
            
            # Validate that pyobject is not allowed as explicit type declaration
            if type_name == 'pyobject':
                raise ParseError(f"Type 'pyobject' is internal only and cannot be used in explicit declarations at line {type_token.line}, column {type_token.col}")
            
            # Validate that the type is a known type
            valid_types = {'int', 'str', 'flt', 'var', 'god', 'bin', 'arr', 'map', 'obj', 'tup'}
            if type_name not in valid_types:
                raise ParseError(f"Unknown type '{type_name}' at line {type_token.line}, column {type_token.col}. Valid types are: {', '.join(valid_types)}")
            
            name_token = self._consume('IDENT', "Expected variable name after type")
            name = name_token.value
            
            declarations.append((type_name, name))
            
            # Check if there's another declaration
            if self._match('COMMA'):
                continue
            else:
                break

        return MultiDeclarationNode(declarations, 'public', line, column)

    def _parse_import_stmt(self) -> ImportNode:
        """Parse import statement: import IDENT(.IDENT)* or import IDENT(.IDENT)*; symbol1, symbol2 as alias"""
        import_token = self._consume('IMPORT', "Expected 'import'")
        module_token = self._consume('IDENT', "Expected module name after 'import'")
        module_name = module_token.value

        # Consume additional dotted components: lyric.math, lyric.math.trig, etc.
        while self._check('DOT') and self._peek_next().type == 'IDENT':
            self._advance()  # consume the DOT
            part_token = self._consume('IDENT', "Expected module name component after '.'")
            module_name += '.' + part_token.value

        symbols = None

        # Check for selective import syntax: import module; symbol1, symbol2
        if self._check('SEMICOLON'):
            self._consume('SEMICOLON', "Expected ';'")
            symbols = []

            # Parse first symbol
            symbol_name = self._consume('IDENT', "Expected symbol name after ';'").value
            alias = None

            # Check for 'as' keyword
            if self._check('AS'):
                self._consume('AS', "Expected 'as'")
                alias = self._consume('IDENT', "Expected alias name after 'as'").value

            symbols.append((symbol_name, alias))

            # Parse additional symbols separated by commas
            while self._check('COMMA'):
                self._consume('COMMA', "Expected ','")
                symbol_name = self._consume('IDENT', "Expected symbol name after ','").value
                alias = None

                # Check for 'as' keyword
                if self._check('AS'):
                    self._consume('AS', "Expected 'as'")
                    alias = self._consume('IDENT', "Expected alias name after 'as'").value

                symbols.append((symbol_name, alias))

        return ImportNode(module_name, symbols, import_token.line, import_token.col)
    
    def _parse_importpy_stmt(self) -> ImportPyNode:
        """Parse importpy statement: importpy IDENT(.IDENT)* [; Name1, Name2, ...]

        Without semicolon list, the whole module proxy is bound to the last
        component of the dotted name (e.g. `importpy http.server` → `server.*`).

        With a semicolon list, each named attribute is bound directly into scope:
            importpy http.server; HTTPServer, SimpleHTTPRequestHandler
            importpy functools; partial
        """
        importpy_token = self._consume('IMPORTPY', "Expected 'importpy'")
        module_token = self._consume('IDENT', "Expected module name after 'importpy'")
        module_name = module_token.value

        # Consume additional dotted components: http.server, os.path, etc.
        while self._check('DOT') and self._peek_next().type == 'IDENT':
            self._advance()  # consume the DOT
            part_token = self._consume('IDENT', "Expected module name component after '.'")
            module_name += '.' + part_token.value

        # Optional selective import list: ; Name1, Name2, ...
        names = None
        if self._match('SEMICOLON'):
            names = []
            while True:
                if self._check('IDENT') or self._check('TYPE_OR_IDENT'):
                    name_token = self._advance()
                    names.append(name_token.value)
                else:
                    raise ParseError(
                        f"Expected identifier in importpy name list at line {self._peek().line}, column {self._peek().col}"
                    )
                if not self._match('COMMA'):
                    break

        return ImportPyNode(module_name, importpy_token.line, importpy_token.col, names)
    
    def _is_file_operator_ahead(self) -> bool:
        """Check if there's a file operator ahead in the token stream."""
        # Look ahead for FILE_APPEND, FILE_WRITE, or FILE_READ tokens
        # We need to scan forward but not consume tokens
        saved_pos = self.current
        try:
            # Skip the first token (it will be an expression)
            # Look for file operators in the next few tokens
            # Increased range to handle exec chains: exec() | exec() ->> file
            for i in range(30):  # Look ahead up to 30 tokens for exec chains
                if self.current + i >= len(self.tokens):
                    return False
                tok = self.tokens[self.current + i]
                if tok.type in ('FILE_APPEND', 'FILE_WRITE', 'FILE_READ'):
                    return True
                # Stop if we hit a statement terminator
                if tok.type in ('NEWLINE', 'EOF', 'RBRACE'):
                    return False
            return False
        finally:
            self.current = saved_pos
    
    def _parse_file_operator_stmt(self) -> FileOpNode:
        """Parse file operator statement: expr ->> expr, expr -> expr, or expr <- expr
        
        Note: File operators are NOT allowed in assignments or expressions.
        They are standalone statements.
        """
        line = self._peek().line
        column = self._peek().col
        
        # Parse left side expression
        left = self._parse_expression()
        
        # Check for file operator
        if self._check('FILE_APPEND'):
            op_token = self._advance()
            operator = '->>'
        elif self._check('FILE_WRITE'):
            op_token = self._advance()
            operator = '->'
        elif self._check('FILE_READ'):
            op_token = self._advance()
            operator = '<-'
        else:
            raise ParseError(f"Expected file operator (->> -> or <-) at line {self._peek().line}, column {self._peek().col}")
        
        # Parse right side expression
        right = self._parse_expression()
        
        return FileOpNode(operator=operator, left=left, right=right, line=line, column=column)
    
    def _is_exec_chain_ahead(self) -> bool:
        """Check if there's an exec chain pattern ahead (exec/print followed by |, &&, ||)."""
        saved_pos = self.current
        try:
            # Check if current token starts an exec chain
            curr = self._peek()
            
            # Must start with exec() call or print statement
            if curr.type == 'IDENT':
                if curr.value == 'exec':
                    # Look for opening paren
                    if self._peek_next().type == 'LPAREN':
                        # Scan ahead to find closing paren, then check for pipe operators
                        paren_depth = 1  # Start at 1 since we know there's an opening paren
                        for i in range(2, 20):  # Start at 2 (after the LPAREN)
                            if self.current + i >= len(self.tokens):
                                return False
                            tok = self.tokens[self.current + i]
                            if tok.type == 'LPAREN':
                                paren_depth += 1
                            elif tok.type == 'RPAREN':
                                paren_depth -= 1
                                if paren_depth == 0:
                                    # Found matching closing paren, check next token
                                    if self.current + i + 1 < len(self.tokens):
                                        next_tok = self.tokens[self.current + i + 1]
                                        return next_tok.type in ('PIPE', 'AND', 'OR')
                                    return False
                        return False
                elif curr.value == 'print':
                    # print statement - check if followed by pipe
                    for i in range(1, 10):
                        if self.current + i >= len(self.tokens):
                            return False
                        tok = self.tokens[self.current + i]
                        if tok.type == 'PIPE':
                            return True
                        if tok.type in ('NEWLINE', 'EOF', 'RBRACE'):
                            return False
                    return False
            return False
        finally:
            self.current = saved_pos
    
    def _parse_exec_chain_stmt(self):
        """Parse exec chain statement with pipes and short-circuit operators.
        
        Patterns:
            exec('cmd') | exec('cmd2')
            exec('cmd') | print
            print "text" | exec('cmd')
            exec('cmd1') && exec('cmd2')
            exec('cmd1') || exec('cmd2')
            exec('cmd') <- input | exec('cmd2') -> output
        """
        line = self._peek().line
        column = self._peek().col
        
        elements = []
        operators = []
        input_source = None
        output_target = None
        
        # Check for optional input source at the beginning
        # Pattern: exec('cmd') <- input | ...
        # We need to look ahead to see if there's a <- before the first pipe
        
        # Parse first element (exec() or print)
        first_elem = self._parse_exec_chain_element()
        
        # Check if first element is followed by <-
        if self._check('FILE_READ'):
            self._advance()  # consume <-
            input_source = self._parse_expression()
            # After <- input, there should be a pipe operator
            if not self._check('PIPE', 'AND', 'OR'):
                # This is just exec() <- input without chaining, treat as file op
                return FileOpNode(operator='<-', left=first_elem, right=input_source, line=line, column=column)
        
        elements.append(first_elem)
        
        # Parse chain operators and subsequent elements
        while self._check('PIPE', 'AND', 'OR'):
            op_token = self._advance()
            if op_token.type == 'PIPE':
                operators.append('|')
            elif op_token.type == 'AND':
                operators.append('&&')
            elif op_token.type == 'OR':
                operators.append('||')
            
            # Parse next element
            elem = self._parse_exec_chain_element()
            elements.append(elem)
        
        # Check for optional output target at the end
        # Pattern: ... | exec('cmd') -> output
        if self._check('FILE_WRITE', 'FILE_APPEND'):
            op_token = self._advance()
            output_target = self._parse_expression()
        
        # If we only have one element and no operators, this might not be a chain
        if len(elements) == 1 and len(operators) == 0:
            # Not really a chain, return as regular statement
            # This shouldn't happen due to _is_exec_chain_ahead check
            return elements[0]
        
        return ExecChainNode(
            elements=elements,
            operators=operators,
            input_source=input_source,
            output_target=output_target,
            line=line,
            column=column
        )
    
    def _parse_exec_chain_element(self):
        """Parse a single element in an exec chain (exec() call or print statement)."""
        curr = self._peek()
        
        if curr.type == 'IDENT' and curr.value == 'exec':
            # Parse exec() function call using primary parser
            return self._parse_primary()
        elif curr.type == 'IDENT' and curr.value == 'print':
            print_token = self._advance()
            
            # Check if it's print(...) or print expr or just print (for piped input)
            if self._check('LPAREN'):
                # Back up and parse as primary
                self.current -= 1
                return self._parse_primary()
            elif self._check('PIPE', 'AND', 'OR', 'NEWLINE', 'EOF', 'RBRACE'):
                # Just 'print' by itself - will print piped input
                # Create CallNode with no arguments
                return CallNode('print', [], print_token.line, print_token.col)
            else:
                # print expr statement
                args = []
                
                # Parse expression argument (but not beyond pipe operators)
                # We need to parse carefully to not consume the pipe
                saved_pos = self.current
                try:
                    expr = self._parse_comparison()  # Lower precedence to stop at pipe
                    args.append(expr)
                except:
                    self.current = saved_pos
                    expr = self._parse_term()
                    args.append(expr)
                
                # Create CallNode for print
                return CallNode('print', args, print_token.line, print_token.col)
        else:
            raise ParseError(f"Expected exec() or print in chain at line {curr.line}, column {curr.col}")


def parse(source: str, interactive: bool = False) -> ProgramNode:
    """Parse source code and return a ProgramNode.
    
    Args:
        source: Source code to parse
        interactive: If True, disables top-level restrictions (for REPL/tests)
    """
    tokens = tokenize(source)
    parser = Parser(tokens)
    if interactive:
        parser._interactive_mode = True
        parser.is_top_level = False
    return parser.parse()