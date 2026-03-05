# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for multi-variable declarations in Lyric 0.4.0."""

import pytest
from lyric.lexer import tokenize
from lyric.parser import parse
from lyric.interpreter import Interpreter
from lyric.errors import ParseError, RuntimeErrorLyric


class TestMultiVariableDeclarations:
    """Test multi-variable declaration functionality."""
    
    def test_basic_multi_declaration(self):
        """Test basic multi-variable declaration parsing."""
        source = "var x, int y, str z"
        tokens = tokenize(source)
        ast = parse(source, interactive=True)
        
        # Should parse successfully
        assert ast is not None
        assert len(ast.statements) == 1
        
        # Check that it's a MultiDeclarationNode
        from lyric.ast_nodes import MultiDeclarationNode
        assert isinstance(ast.statements[0], MultiDeclarationNode)
        
        # Check declarations
        declarations = ast.statements[0].declarations
        assert len(declarations) == 3
        assert declarations[0] == ('var', 'x')
        assert declarations[1] == ('int', 'y')
        assert declarations[2] == ('str', 'z')
    
    def test_multi_declaration_execution(self):
        """Test multi-variable declaration execution."""
        source = """
        var x, int y, str z
        x = 3.14
        y = 42
        z = "hello"
        """
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        interpreter.evaluate(ast)
        
        # Check that variables are declared and can be assigned
        assert interpreter.global_scope['x'] == 3.14
        assert interpreter.global_scope['y'] == 42
        assert interpreter.global_scope['z'] == "hello"
        
        # Check that types are stored
        assert interpreter.variable_types['x'] == 'var'
        assert interpreter.variable_types['y'] == 'int'
        assert interpreter.variable_types['z'] == 'str'
    
    def test_multi_declaration_uninitialized(self):
        """Test that multi-declared variables start as None."""
        source = "var x, int y, str z"
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        interpreter.evaluate(ast)
        
        # Check that variables are declared but uninitialized
        assert interpreter.global_scope['x'] is None
        assert interpreter.global_scope['y'] is None
        assert interpreter.global_scope['z'] is None
    
    def test_mixed_types_multi_declaration(self):
        """Test multi-declaration with all supported types."""
        source = "var a, int b, str c, flt d"
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        interpreter.evaluate(ast)
        
        # Check that all variables are declared
        assert 'a' in interpreter.global_scope
        assert 'b' in interpreter.global_scope
        assert 'c' in interpreter.global_scope
        assert 'd' in interpreter.global_scope
        
        # Check that types are stored correctly
        assert interpreter.variable_types['a'] == 'var'
        assert interpreter.variable_types['b'] == 'int'
        assert interpreter.variable_types['c'] == 'str'
        assert interpreter.variable_types['d'] == 'flt'
    
    def test_single_variable_declaration(self):
        """Test that single variable declaration still works."""
        source = "var x"
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        interpreter.evaluate(ast)
        
        # Check that single variable is declared
        assert 'x' in interpreter.global_scope
        assert interpreter.global_scope['x'] is None
        assert interpreter.variable_types['x'] == 'var'
    
    def test_type_enforcement_after_multi_declaration(self):
        """Test that type enforcement works after multi-declaration."""
        source = """
        int x, str y
        x = 42
        y = "hello"
        """
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        interpreter.evaluate(ast)
        
        # Should work fine
        assert interpreter.global_scope['x'] == 42
        assert interpreter.global_scope['y'] == "hello"
    
    def test_type_enforcement_error_after_multi_declaration(self):
        """Test that type enforcement errors are caught after multi-declaration."""
        source = """
        int x, str y
        x = "hello"
        """
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        assert "Type mismatch" in str(exc_info.value)
        assert "cannot assign str to variable 'x' declared as int" in str(exc_info.value)
    
    def test_pyobject_not_allowed_in_multi_declaration(self):
        """Test that pyobject is not allowed in multi-declarations."""
        source = "pyobject x, int y"
        
        with pytest.raises(ParseError) as exc_info:
            parse(source, interactive=True)
        
        assert "Type 'pyobject' is internal only" in str(exc_info.value)
    
    def test_invalid_type_in_multi_declaration(self):
        """Test that invalid types are rejected in multi-declarations."""
        source = "invalid_type x, int y"
        
        with pytest.raises(ParseError) as exc_info:
            parse(source, interactive=True)
        
        assert "Unknown type 'invalid_type'" in str(exc_info.value)
    
    def test_multi_declaration_with_assignment_error(self):
        """Test that multi-declaration doesn't allow assignment in same line."""
        source = "var x = 5, int y"
        
        with pytest.raises(ParseError) as exc_info:
            parse(source, interactive=True)
        
        # Should fail because multi-declaration doesn't support assignment
        assert "Expected" in str(exc_info.value)
    
    def test_multi_declaration_in_function(self):
        """Test multi-declaration inside functions."""
        source = """
        def test_function() {
            var x, int y, str z
            x = 3.14
            y = 42
            z = "hello"
            return x
        }
        """
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        interpreter.evaluate(ast)
        
        # Call the function
        result = interpreter._call_function("test_function", [])
        assert result == 3.14
    
    def test_multi_declaration_in_class(self):
        """Test multi-declaration inside classes."""
        source = """
        class TestClass
            var x, int y, str z
            def init(self) {
                self.x = 3.14
                self.y = 42
                self.z = "hello"
            }
        +++
        """
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        interpreter.evaluate(ast)
        
        # Check that the class is defined correctly
        assert 'TestClass' in interpreter.classes
        class_def = interpreter.classes['TestClass']
        
        # Check that the class has the multi-declared variables
        assert 'x' in class_def
        assert 'y' in class_def
        assert 'z' in class_def
        
        # Check that the variables are uninitialized (None)
        assert class_def['x'] is None
        assert class_def['y'] is None
        assert class_def['z'] is None
    
    def test_multi_declaration_with_duplicate_names(self):
        """Test that duplicate variable names are handled correctly."""
        source = """
        var x, int x
        """
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        interpreter.evaluate(ast)
        
        # The second declaration should overwrite the first
        assert interpreter.variable_types['x'] == 'int'
        assert interpreter.global_scope['x'] is None
    
    def test_multi_declaration_empty(self):
        """Test that empty multi-declaration is handled."""
        source = "var x"
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        interpreter.evaluate(ast)
        
        # Should work fine with single variable
        assert 'x' in interpreter.global_scope
        assert interpreter.global_scope['x'] is None
    
    def test_multi_declaration_with_whitespace(self):
        """Test multi-declaration with various whitespace patterns."""
        source = "var x , int y , str z"
        
        interpreter = Interpreter()
        ast = parse(source, interactive=True)
        interpreter.evaluate(ast)
        
        # Should parse successfully
        assert len(ast.statements) == 1
        from lyric.ast_nodes import MultiDeclarationNode
        assert isinstance(ast.statements[0], MultiDeclarationNode)
        
        declarations = ast.statements[0].declarations
        assert len(declarations) == 3
        assert declarations[0] == ('var', 'x')
        assert declarations[1] == ('int', 'y')
        assert declarations[2] == ('str', 'z')
    
    def test_multi_declaration_line_position(self):
        """Test that line and column information is preserved."""
        source = "var x, int y, str z"
        
        ast = parse(source, interactive=True)
        multi_decl = ast.statements[0]
        
        # Should have line and column information
        assert multi_decl.line >= 0
        assert multi_decl.column >= 0
