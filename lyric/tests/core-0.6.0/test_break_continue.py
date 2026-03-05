# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Comprehensive tests for break and continue keywords (Sprint 6 Pivot 6.5.1)."""

import pytest
import sys
import io
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import ParseError


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


class TestBreakKeyword:
    """Test suite for the break keyword."""
    
    def test_break_exits_loop(self):
        """Test that break exits the loop immediately."""
        source = """
        def main() {
            var count = 0
            int i
            for i in range(10):
                count = count + 1
                if i == 5:
                    break
                end
            done
            return count
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        # Loop should exit when i==5, so count should be 6 (0,1,2,3,4,5)
        assert result == 6
    
    def test_break_with_print_output(self):
        """Test break with print statements to verify early exit."""
        source = """
        def main() {
            int i
            for i in range(10):
                if i == 3:
                    break
                end
                print(i)
            done
        }
        """
        
        ast = parse(source, interactive=True)
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            evaluate(ast)
        finally:
            sys.stdout = old_stdout
        
        output = captured_output.getvalue()
        # Should print 0, 1, 2 but not 3 or beyond
        assert "0" in output
        assert "1" in output
        assert "2" in output
        assert "3" not in output
        assert "4" not in output
    
    def test_break_in_nested_loop_only_exits_inner(self):
        """Test that break only exits the innermost loop."""
        source = """
        def main() {
            var outer_count = 0
            var inner_count = 0
            int i
            int j

            for i in range(3):
                outer_count = outer_count + 1
                for j in range(5):
                    inner_count = inner_count + 1
                    if j == 2:
                        break
                    end
                done
            done

            return inner_count
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        # Inner loop breaks at j==2, so it runs 3 times (j=0,1,2) per outer iteration
        # Outer loop runs 3 times, so inner_count = 3 * 3 = 9
        assert result == 9
    
    def test_break_outside_loop_raises_error(self):
        """Test that break outside a loop raises ParseError."""
        source = """
        def main() {
            break
        }
        """
        
        with pytest.raises(ParseError, match="'break' used outside of loop"):
            parse(source, interactive=True)
    
    def test_break_in_while_loop(self):
        """Test break in a while-style loop."""
        source = """
        def main() {
            var count = 0
            given count < 100:
                count = count + 1
                if count == 10:
                    break
                end
            done
            return count
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        assert result == 10


class TestContinueKeyword:
    """Test suite for the continue keyword."""
    
    def test_continue_skips_iteration(self):
        """Test that continue skips the rest of the current iteration."""
        source = """
        def main() {
            var sum = 0
            int i
            for i in range(10):
                if i == 5:
                    continue
                end
                sum = sum + i
            done
            return sum
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        # Sum of 0+1+2+3+4+6+7+8+9 = 40 (skipping 5)
        assert result == 40
    
    def test_continue_with_print_output(self):
        """Test continue with print statements to verify skipping."""
        source = """
        def main() {
            int i
            for i in range(6):
                if i == 2:
                    continue
                end
                if i == 4:
                    continue
                end
                print(i)
            done
        }
        """
        
        ast = parse(source, interactive=True)
        
        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            evaluate(ast)
        finally:
            sys.stdout = old_stdout
        
        output = captured_output.getvalue()
        # Should print 0, 1, 3, 5 (skipping 2 and 4)
        assert "0" in output
        assert "1" in output
        assert "2" not in output
        assert "3" in output
        assert "4" not in output
        assert "5" in output
    
    def test_continue_in_nested_loop_only_affects_inner(self):
        """Test that continue only affects the innermost loop."""
        source = """
        def main() {
            var total = 0
            int i
            int j

            for i in range(3):
                for j in range(5):
                    if j == 2:
                        continue
                    end
                    total = total + 1
                done
            done

            return total
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        # Inner loop runs 5 times but skips once (j==2), so 4 increments per outer iteration
        # Outer loop runs 3 times, so total = 3 * 4 = 12
        assert result == 12
    
    def test_continue_outside_loop_raises_error(self):
        """Test that continue outside a loop raises ParseError."""
        source = """
        def main() {
            continue
        }
        """
        
        with pytest.raises(ParseError, match="'continue' used outside of loop"):
            parse(source, interactive=True)
    
    def test_continue_in_while_loop(self):
        """Test continue in a while-style loop."""
        source = """
        def main() {
            var count = 0
            var sum = 0
            given count < 10:
                count = count + 1
                if count == 5:
                    continue
                end
                sum = sum + count
            done
            return sum
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        # Sum of 1+2+3+4+6+7+8+9+10 = 50 (skipping 5)
        assert result == 50


class TestBreakContinueTogether:
    """Test cases combining break and continue."""
    
    def test_break_and_continue_in_same_loop(self):
        """Test using both break and continue in the same loop."""
        source = """
        def main() {
            var sum = 0
            int i
            for i in range(20):
                if i == 15:
                    break
                end
                if i == 2:
                    continue
                end
                if i == 5:
                    continue
                end
                if i == 8:
                    continue
                end
                sum = sum + i
            done
            return sum
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        # Sum of 0+1+3+4+6+7+9+10+11+12+13+14 = 90 (skipping 2,5,8)
        assert result == 90
    
    def test_nested_loops_with_both_keywords(self):
        """Test break and continue in nested loops."""
        source = """
        def main() {
            var result = 0
            int i
            int j

            for i in range(5):
                if i == 3:
                    break
                end

                for j in range(5):
                    if j == 2:
                        continue
                    end
                    result = result + 1
                done
            done

            return result
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        # Outer loop runs 3 times (0,1,2, breaks at 3)
        # Inner loop runs 4 times per outer iteration (0,1,3,4, skips 2)
        # Total: 3 * 4 = 12
        assert result == 12


class TestBreakContinueWithTryCatch:
    """Test break and continue interaction with try/catch blocks."""
    
    def test_break_inside_try_block(self):
        """Test that break works inside a try block."""
        source = """
        def main() {
            var count = 0
            int i
            for i in range(10):
                try:
                    count = count + 1
                    if i == 5:
                        break
                    end
                catch:
                    print("error")
                fade
            done
            return count
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        assert result == 6
    
    def test_continue_inside_try_block(self):
        """Test that continue works inside a try block."""
        source = """
        def main() {
            var sum = 0
            int i
            for i in range(10):
                try:
                    if i == 5:
                        continue
                    end
                    sum = sum + i
                catch:
                    print("error")
                fade
            done
            return sum
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        # Sum of 0+1+2+3+4+6+7+8+9 = 40
        assert result == 40


class TestBreakContinueEdgeCases:
    """Test edge cases for break and continue."""
    
    def test_break_first_iteration(self):
        """Test break on the very first iteration."""
        source = """
        def main() {
            var count = 0
            int i
            for i in range(10):
                count = count + 1
                break
            done
            return count
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        assert result == 1
    
    def test_continue_all_iterations(self):
        """Test continue that skips all iterations."""
        source = """
        def main() {
            var executed = 0
            int i
            for i in range(5):
                continue
                executed = executed + 1
            done
            return executed
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        assert result == 0
    
    def test_break_with_return(self):
        """Test break followed by return (break should be reached first)."""
        source = """
        def main() {
            int i
            for i in range(10):
                if i == 3:
                    break
                end
            done
            return 42
        }
        """
        
        ast = parse(source, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        result = interpreter._call_function('main', [])
        
        assert result == 42

