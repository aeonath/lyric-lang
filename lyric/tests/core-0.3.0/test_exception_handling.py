# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for Sprint 3 Task 5: Exception Handling."""

import pytest
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import RuntimeErrorLyric, ParseError


def test_basic_try_catch():
    """Test basic try/catch block functionality."""
    source = '''
    def main() {
        var result = 0
        try:
            result = 10
        catch:
            result = 20
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 10  # No exception, try block executes


def test_try_catch_with_exception():
    """Test try/catch block catching an exception."""
    source = '''
    def main() {
        var result = 0
        try:
            raise RuntimeErrorLyric
            result = 10
        catch:
            result = 20
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 20  # Exception caught, catch block executes


def test_try_catch_finally():
    """Test try/catch/finally block with all parts executing."""
    source = '''
    def main() {
        var result = 0
        try:
            result = 10
        catch:
            result = 20
        finally:
            result = result + 5
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 15  # try executes (10), finally adds 5


def test_try_catch_finally_with_exception():
    """Test try/catch/finally with exception being caught."""
    source = '''
    def main() {
        var result = 0
        try:
            raise RuntimeErrorLyric
            result = 10
        catch:
            result = 20
        finally:
            result = result + 5
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 25  # catch executes (20), finally adds 5


def test_finally_always_executes():
    """Test that finally block always executes."""
    source = '''
    def main() {
        var cleanup = 0
        try:
            cleanup = 1
        catch:
            cleanup = 2
        finally:
            cleanup = cleanup * 10
        fade
        return cleanup
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 10  # try sets to 1, finally multiplies by 10


def test_raise_index_error():
    """Test raising IndexErrorLyric."""
    source = '''
    def main() {
        var result = 0
        try:
            raise IndexErrorLyric
        catch:
            result = 100
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 100  # IndexError caught


def test_raise_type_error():
    """Test raising TypeErrorLyric."""
    source = '''
    def main() {
        var result = 0
        try:
            raise TypeErrorLyric
        catch:
            result = 200
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 200  # TypeError caught


def test_raise_value_error():
    """Test raising ValueErrorLyric."""
    source = '''
    def main() {
        var result = 0
        try:
            raise ValueErrorLyric
        catch:
            result = 300
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 300  # ValueError caught


def test_uncaught_exception_propagates():
    """Test that uncaught exceptions propagate outside try/catch."""
    source = '''
    def main() {
        var result = 0
        raise RuntimeErrorLyric
        return result
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric):
        evaluate(ast)


def test_exception_in_function_call():
    """Test exception handling with function calls."""
    source = '''
    def risky_function() {
        raise RuntimeErrorLyric
        return 10
    }
    
    def main() {
        var result = 0
        try:
            result = risky_function()
        catch:
            result = 99
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 99  # Exception from function call caught


def test_try_without_catch_syntax_error():
    """Test that try without catch raises a syntax error."""
    source = '''
    def main() {
        try:
            var x = 10
        finally:
            var y = 20
        fade
    }'''
    
    with pytest.raises(ParseError, match="try block must have at least one catch block"):
        parse(source)


def test_scope_isolation_try_block():
    """Test that try block can access and modify outer scope variables."""
    source = '''
    def main() {
        var x = 10
        try:
            var y = 20
            x = 30
        catch:
            var z = 40
        fade
        return x
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # x should be modified in the try block
    assert result == 30


def test_scope_isolation_catch_block():
    """Test that catch block can access and modify outer scope variables."""
    source = '''
    def main() {
        var x = 10
        try:
            raise RuntimeErrorLyric
        catch:
            var y = 20
            x = 30
        fade
        return x
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # x should be modified in the catch block
    assert result == 30


def test_scope_isolation_finally_block():
    """Test that finally block can access and modify outer scope variables."""
    source = '''
    def main() {
        var x = 10
        try:
            var y = 20
        catch:
            var z = 30
        finally:
            var w = 40
            x = 50
        fade
        return x
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    # x should be modified in the finally block
    assert result == 50


def test_multiple_statements_in_try():
    """Test multiple statements in try block."""
    source = '''
    def main() {
        var result = 0
        try:
            result = result + 10
            result = result + 5
            result = result * 2
        catch:
            result = 0
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 30  # (0 + 10 + 5) * 2


def test_multiple_statements_in_catch():
    """Test multiple statements in catch block."""
    source = '''
    def main() {
        var result = 0
        try:
            raise RuntimeErrorLyric
        catch:
            result = result + 10
            result = result + 5
            result = result * 2
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 30  # (0 + 10 + 5) * 2


def test_multiple_statements_in_finally():
    """Test multiple statements in finally block."""
    source = '''
    def main() {
        var result = 1
        try:
            result = result + 10
        catch:
            result = 0
        finally:
            result = result + 5
            result = result * 2
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 32  # (1 + 10 + 5) * 2


def test_raise_with_standard_python_name():
    """Test raising exceptions with standard Python names (without Lyric suffix)."""
    source = '''
    def main() {
        var result = 0
        try:
            raise IndexError
        catch:
            result = 100
        fade
        return result
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 100  # IndexError caught


def test_print_in_try_catch():
    """Test that print statements work in try/catch blocks."""
    source = '''
    def main() {
        try:
            print("In try block")
        catch:
            print("In catch block")
        finally:
            print("In finally block")
        fade
        return 42
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 42


def test_lexer_keywords():
    """Test that catch, fade, and raise are recognized as keywords."""
    from lyric.lexer import Lexer
    
    assert 'catch' in Lexer.KEYWORDS
    assert 'fade' in Lexer.KEYWORDS
    assert 'raise' in Lexer.KEYWORDS
    assert 'except' not in Lexer.KEYWORDS  # except should be removed


def test_try_catch_parse_structure():
    """Test that try/catch/finally/fade parses correctly into TryNode."""
    source = '''
    def main() {
        try:
            var x = 10
        catch:
            var y = 20
        finally:
            var z = 30
        fade
    }'''
    
    ast = parse(source)
    # Find the main function
    main_func = None
    for stmt in ast.statements:
        if hasattr(stmt, 'name') and stmt.name == 'main':
            main_func = stmt
            break
    
    assert main_func is not None
    # Check that the first statement in main is a TryNode
    from lyric.ast_nodes import TryNode
    assert len(main_func.body_statements) > 0
    assert isinstance(main_func.body_statements[0], TryNode)


def test_raise_parse_structure():
    """Test that raise statement parses correctly into RaiseNode."""
    source = '''
    def main() {
        raise RuntimeErrorLyric
    }'''
    
    ast = parse(source)
    # Find the main function
    main_func = None
    for stmt in ast.statements:
        if hasattr(stmt, 'name') and stmt.name == 'main':
            main_func = stmt
            break
    
    assert main_func is not None
    # Check that the first statement in main is a RaiseNode
    from lyric.ast_nodes import RaiseNode
    assert len(main_func.body_statements) > 0
    assert isinstance(main_func.body_statements[0], RaiseNode)
    assert main_func.body_statements[0].exception_name == 'RuntimeErrorLyric'

