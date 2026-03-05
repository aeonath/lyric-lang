# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for Lyric module imports.
"""

import pytest


class TestImports:
    """Test cases for module imports."""
    
    def test_main_package_import(self):
        """Test that main lyric package can be imported."""
        import lyric
        assert lyric is not None
    
    def test_cli_module_import(self):
        """Test that CLI module can be imported."""
        import lyric.cli
        assert hasattr(lyric.cli, 'main')
    
    def test_errors_module_import(self):
        """Test that errors module can be imported."""
        import lyric.errors
        assert hasattr(lyric.errors, 'LexError')
        assert hasattr(lyric.errors, 'ParseError')
        assert hasattr(lyric.errors, 'RuntimeErrorLyric')
    
    def test_lexer_module_import(self):
        """Test that lexer module can be imported."""
        import lyric.lexer
        assert lyric.lexer is not None
    
    def test_parser_module_import(self):
        """Test that parser module can be imported."""
        import lyric.parser
        assert lyric.parser is not None
    
    def test_ast_module_import(self):
        """Test that AST module can be imported."""
        import lyric.ast_nodes
        assert lyric.ast_nodes is not None
    
    def test_interpreter_module_import(self):
        """Test that interpreter module can be imported."""
        import lyric.interpreter
        assert lyric.interpreter is not None
    
    def test_runtime_module_import(self):
        """Test that runtime module can be imported."""
        import lyric.runtime
        assert lyric.runtime is not None
    
    def test_all_modules_import_together(self):
        """Test that all modules can be imported together."""
        import lyric
        import lyric.cli
        import lyric.errors
        import lyric.lexer
        import lyric.parser
        import lyric.ast_nodes
        import lyric.interpreter
        import lyric.runtime
        
        # Verify all modules are accessible
        assert lyric is not None
        assert lyric.cli is not None
        assert lyric.errors is not None
        assert lyric.lexer is not None
        assert lyric.parser is not None
        assert lyric.ast_nodes is not None
        assert lyric.interpreter is not None
        assert lyric.runtime is not None
