# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for Sprint 6 Task 5: Exception Type Binding in catch Clauses."""

import pytest
import sys
import io
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import IndexErrorLyric, KeyErrorLyric, TypeErrorLyric


def test_catch_with_type_specific():
    """Test catch clause with specific exception type."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch IndexError:
            return 1
        catch:
            return 2
        fade
        return 0
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    assert result == 1  # IndexError clause should match


def test_catch_with_type_binding():
    """Test catch clause with exception variable binding."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch IndexError as e:
            return str(e)
        fade
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    assert "Index out of range" in result


def test_catch_bare_fallback():
    """Test that bare catch acts as fallback."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch KeyError:
            return 1
        catch:
            return 2
        fade
        return 0
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    assert result == 2  # Should fall through to bare catch


def test_catch_multiple_typed_clauses():
    """Test multiple typed catch clauses."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch IndexError:
            return "index"
        catch KeyError:
            return "key"
        catch:
            return "other"
        fade
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    assert result == "index"


def test_catch_with_string_concatenation():
    """Test that exception variables can be concatenated with strings."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch IndexError as e:
            return "Caught: " + str(e)
        fade
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    assert "Caught:" in result
    assert "Index out of range" in result


def test_catch_nested_try():
    """Test nested try/catch with type binding."""
    source = '''
    def main() {
        var result = ""
        try:
            try:
                var items = [1, 2, 3]
                var x = items[10]
            catch KeyError:
                result = "inner-key"
            fade
        catch IndexError as e:
            result = "outer-index"
        fade
        return result
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    # The inner try should not catch IndexError, so it propagates to outer
    assert result == "outer-index"


def test_catch_type_only_no_binding():
    """Test catch with type but no variable binding."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch IndexError:
            return "caught-index"
        fade
        return "no-catch"
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    assert result == "caught-index"


def test_catch_binding_only_no_type():
    """Test catch with binding but no type (bare catch with variable)."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch as e:
            return "caught"
        fade
        return "no-catch"
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    assert result == "caught"


def test_exception_type_hierarchy():
    """Test that exception type hierarchy works correctly."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch IndexError:
            return "index-specific"
        catch Error:
            return "generic-error"
        fade
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    # Should match the more specific IndexError first
    assert result == "index-specific"


def test_key_error_matching():
    """Test KeyError matching in dictionary access."""
    source = '''
    def main() {
        try:
            var dict = {"a": 1}
            var x = dict["missing"]
        catch KeyError as e:
            return "key-error"
        catch:
            return "other"
        fade
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    assert result == "key-error"


def test_type_error_matching():
    """Test TypeError matching."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items["not-an-int"]
        catch TypeError:
            return "type-error"
        catch IndexError:
            return "index-error"
        catch:
            return "other"
        fade
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    assert result == "type-error"


def test_exception_propagation_with_typing():
    """Test that unmatched exceptions propagate correctly."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch KeyError:
            return "key"
        fade
    }'''
    
    ast = parse(source, interactive=True)
    with pytest.raises(IndexErrorLyric):
        evaluate(ast)


def test_multiple_catch_clauses_order():
    """Test that catch clauses are checked in order."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch:
            return "first"
        catch IndexError:
            return "second"
        fade
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    # First catch (bare) should match, second should not be checked
    assert result == "first"


def test_exception_binding_scope():
    """Test that exception variable is available in catch scope."""
    source = '''
    def main() {
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch IndexError as error:
            var msg = str(error)
            return msg
        fade
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    assert "Index out of range" in result


def test_catch_with_finally():
    """Test exception type binding with finally clause."""
    source = '''
    def main() {
        var result1 = ""
        try:
            var items = [1, 2, 3]
            var x = items[10]
        catch IndexError as e:
            result = "caught"
        finally:
            result = "finally"
        fade
        return result
    }'''
    
    ast = parse(source, interactive=True)
    result = evaluate(ast)
    # Finally should execute after catch
    assert result == "finally"

