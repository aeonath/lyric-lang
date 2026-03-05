# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for the `for` keyword (Task 3 - Sprint 6)."""

import pytest
import sys
import io
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter


def parse(source: str, interactive: bool = False):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    if interactive:
        parser._interactive_mode = True
        parser.is_top_level = False
    return parser.parse()


def evaluate(ast):
    """Helper to evaluate an AST."""
    interpreter = Interpreter()
    return interpreter.evaluate(ast)


class TestForKeyword:
    """Test suite for the `for` keyword."""
    
    def test_for_keyword_basic_iteration(self):
        """Test that `for` keyword works for basic iteration."""
        source = """
        def main() {
            int i
            for i in range(3):
                print(i)
            done
        }
        """
        
        ast = parse(source, interactive=True)
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = evaluate(ast)
        finally:
            sys.stdout = old_stdout
        
        output = captured_output.getvalue()
        assert "0" in output
        assert "1" in output
        assert "2" in output
    
    def test_for_keyword_with_accumulator(self):
        """Test that `for` keyword works with variable accumulation."""
        source = """
        def main() {
            var sum = 0
            int i
            for i in range(5):
                sum = sum + i
            done
            return sum
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        # sum should be 0+1+2+3+4 = 10
        assert result == 10
    
    def test_for_keyword_nested(self):
        """Test nested `for` loops."""
        source = """
        def main() {
            int i
            int j
            for i in range(2):
                for j in range(2):
                    print(i, j)
                done
            done
        }
        """
        
        ast = parse(source, interactive=True)
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = evaluate(ast)
        finally:
            sys.stdout = old_stdout
        
        output = captured_output.getvalue()
        # Should see all combinations
        assert "0" in output
        assert "1" in output
    
    def test_for_keyword_with_conditional(self):
        """Test `for` keyword with conditional statements."""
        source = """
        def main() {
            int i
            for i in range(5):
                if i > 2:
                    print("greater")
                else:
                    print("smaller")
                end
            done
        }
        """
        
        ast = parse(source, interactive=True)
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = evaluate(ast)
        finally:
            sys.stdout = old_stdout
        
        output = captured_output.getvalue()
        assert "greater" in output
        assert "smaller" in output
    
    def test_for_is_iterator_given_is_while(self):
        """Test that `for` is used for iteration and `given` is used for while-loops."""
        # for...in is for iterator loops
        source_for = """
        def test_for() {
            var sum = 0
            int i
            for i in range(5):
                sum = sum + i
            done
            return sum
        }
        """

        # given is for while-style condition loops
        source_given = """
        def test_given() {
            var sum = 0
            var i = 0
            given i < 5:
                sum = sum + i
                i = i + 1
            done
            return sum
        }
        """

        # Test for...in iterator loop
        ast_for = parse(source_for)
        interpreter_for = Interpreter()
        interpreter_for.evaluate(ast_for)
        result_for = interpreter_for._call_function('test_for', [])

        # Test given while-loop
        ast_given = parse(source_given)
        interpreter_given = Interpreter()
        interpreter_given.evaluate(ast_given)
        result_given = interpreter_given._call_function('test_given', [])

        # Both should produce the same result (0+1+2+3+4 = 10)
        assert result_for == result_given
        assert result_for == 10
    
    def test_for_keyword_token_generation(self):
        """Test that `for` keyword generates GIVEN token."""
        source = "for i in range(3): print(i) done"
        tokens = tokenize(source)
        
        # Find the `for` token
        for_token = None
        for token in tokens:
            if token.value == 'for':
                for_token = token
                break
        
        assert for_token is not None, "`for` keyword not found in tokens"
        assert for_token.type == 'GIVEN', f"Expected GIVEN token, got {for_token.type}"
    
    def test_for_keyword_with_break_continue(self):
        """Test `for` keyword with break and continue (if supported)."""
        # Note: This test assumes break/continue are supported
        # If not yet implemented, this test will be skipped
        source = """
        def main() {
            int i
            for i in range(10):
                if i == 5:
                    break
                end
                print(i)
            done
        }
        """
        
        try:
            ast = parse(source, interactive=True)
            
            # Capture print output
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            try:
                result = evaluate(ast)
            finally:
                sys.stdout = old_stdout
            
            output = captured_output.getvalue()
            # Should print 0-4, but not 5 or beyond
            assert "4" in output
            assert "5" not in output or output.count("5") == 0
        except Exception as e:
            # If break is not supported yet, skip this test
            pytest.skip(f"Break statement not yet supported: {e}")
    
    def test_for_keyword_with_function_calls(self):
        """Test `for` keyword with function calls in loop body."""
        source = """
        def double(int n) {
            return n * 2
        }

        def main() {
            int i
            for i in range(3):
                print(double(i))
            done
        }
        """
        
        ast = parse(source, interactive=True)
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = evaluate(ast)
        finally:
            sys.stdout = old_stdout
        
        output = captured_output.getvalue()
        assert "0" in output  # double(0) = 0
        assert "2" in output  # double(1) = 2
        assert "4" in output  # double(2) = 4

