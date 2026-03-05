# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""def main() {\n    
Comprehensive test suite for range() built-in function edge cases.
Tests negative steps, zero step errors, negative values, and type validation.
\n}"""

import pytest
from lyric.parser import parse
from lyric.interpreter import Interpreter, evaluate
from lyric.errors import RuntimeErrorLyric, TypeErrorLyric


class TestRangeNegativeStep:
    """def main() {\n    Test range() with negative step values (countdown).\n}"""
    
    def test_range_negative_step_countdown(self):
        """def main() {\n    Test range countdown from 5 to 1.\n}"""
        code = """
var count = 0
int i
for i in range(5, 0, -1):
    count = count + 1
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(5, 0, -1) should produce [5, 4, 3, 2, 1] = 5 iterations
        assert interpreter.global_scope['count'] == 5
    
    def test_range_negative_step_with_negatives(self):
        """def main() {\n    Test range with negative start/stop and negative step.\n}"""
        code = """
var items = []
int i
for i in range(-1, -6, -1):
    items = items + [i]
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(-1, -6, -1) should produce [-1, -2, -3, -4, -5]
        assert items.elements == [-1, -2, -3, -4, -5]
    
    def test_range_negative_step_by_two(self):
        """def main() {\n    Test range with negative step of -2.\n}"""
        code = """
var items = []
int i
for i in range(10, 0, -2):
    items = items + [i]
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(10, 0, -2) should produce [10, 8, 6, 4, 2]
        assert items.elements == [10, 8, 6, 4, 2]


class TestRangeZeroStep:
    """def main() {\n    Test range() with zero step (should raise error).\n}"""
    
    def test_range_zero_step_raises_error(self):
        """def main() {\n    Test that range with step=0 raises a ValueError.\n}"""
        code = """
var items = []
int i
for i in range(0, 5, 0):
    items = items + [i]
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        
        # Python's range(0, 5, 0) raises ValueError: range() arg 3 must not be zero
        with pytest.raises((ValueError, RuntimeErrorLyric)):
            interpreter.evaluate(ast)


class TestRangeNegativeValues:
    """def main() {\n    Test range() with negative start/stop values.\n}"""
    
    def test_range_negative_to_positive(self):
        """def main() {\n    Test range from negative to positive.\n}"""
        code = """
var items = []
int i
for i in range(-5, 5):
    items = items + [i]
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(-5, 5) should produce [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
        assert items.elements == [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
    
    def test_range_negative_start(self):
        """def main() {\n    Test range starting from negative number.\n}"""
        code = """
var items = []
int i
for i in range(-3, 2):
    items = items + [i]
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(-3, 2) should produce [-3, -2, -1, 0, 1]
        assert items.elements == [-3, -2, -1, 0, 1]
    
    def test_range_both_negative(self):
        """def main() {\n    Test range with both negative start and stop.\n}"""
        code = """
var items = []
int i
for i in range(-10, -5):
    items = items + [i]
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(-10, -5) should produce [-10, -9, -8, -7, -6]
        assert items.elements == [-10, -9, -8, -7, -6]
    
    def test_range_negative_with_step(self):
        """def main() {\n    Test range with negative start and positive step.\n}"""
        code = """
var items = []
int i
for i in range(-10, 0, 2):
    items = items + [i]
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        from lyric.interpreter import ArrObject
        items = interpreter.global_scope['items']
        assert isinstance(items, ArrObject)
        # range(-10, 0, 2) should produce [-10, -8, -6, -4, -2]
        assert items.elements == [-10, -8, -6, -4, -2]


class TestRangeEmptyRanges:
    """def main() {\n    Test range() that should produce empty sequences.\n}"""
    
    def test_range_empty_start_equals_stop(self):
        """def main() {\n    Test range where start equals stop.\n}"""
        code = """
var count = 0
int i
for i in range(5, 5):
    count = count + 1
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(5, 5) should be empty
        assert interpreter.global_scope['count'] == 0
    
    def test_range_empty_start_greater_than_stop_positive_step(self):
        """def main() {\n    Test range where start > stop with positive step.\n}"""
        code = """
var count = 0
int i
for i in range(10, 5, 1):
    count = count + 1
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(10, 5, 1) should be empty (can't count up from 10 to 5)
        assert interpreter.global_scope['count'] == 0
    
    def test_range_empty_start_less_than_stop_negative_step(self):
        """def main() {\n    Test range where start < stop with negative step.\n}"""
        code = """
var count = 0
int i
for i in range(5, 10, -1):
    count = count + 1
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(5, 10, -1) should be empty (can't count down from 5 to 10)
        assert interpreter.global_scope['count'] == 0
    
    def test_range_single_arg_zero(self):
        """def main() {\n    Test range(0) produces empty sequence.\n}"""
        code = """
var count = 0
int i
for i in range(0):
    count = count + 1
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(0) should be empty
        assert interpreter.global_scope['count'] == 0
    
    def test_range_single_arg_negative(self):
        """def main() {\n    Test range with negative single argument produces empty sequence.\n}"""
        code = """
var count = 0
int i
for i in range(-5):
    count = count + 1
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(-5) should be empty
        assert interpreter.global_scope['count'] == 0


class TestRangeTypeValidation:
    """def main() {\n    Test range() type validation and error handling.\n}"""
    
    def test_range_with_float_argument(self):
        """def main() {\n    Test that range rejects float arguments.\n}"""
        code = """
var items = []
int i
for i in range(5.5):
    items = items + [i]
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        
        # Python's range() requires integers
        with pytest.raises((TypeError, RuntimeErrorLyric)):
            interpreter.evaluate(ast)
    
    def test_range_with_string_argument(self):
        """def main() {\n    Test that range rejects string arguments.\n}"""
        code = """
var items = []
int i
for i in range("5"):
    items = items + [i]
done
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        
        # Python's range() requires integers
        with pytest.raises((TypeError, RuntimeErrorLyric)):
            interpreter.evaluate(ast)
    
    def test_range_no_arguments_error(self):
        """def main() {\n    Test that range with no arguments raises error.\n}"""
        code = """
var items = range()
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Invalid range() arguments" in error_msg or "takes 1-3 arguments" in error_msg
    
    def test_range_too_many_arguments_error(self):
        """def main() {\n    Test that range with > 3 arguments raises error.\n}"""
        code = """
var items = range(1, 2, 3, 4)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Invalid range() arguments" in error_msg
        assert "takes 1-3 arguments" in error_msg


class TestRangeLargeValues:
    """def main() {\n    Test range() with large values.\n}"""
    
    def test_range_large_single_argument(self):
        """def main() {\n    Test range with large single argument.\n}"""
        code = """
var items = range(10000)
var count = items.len()
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(10000) should produce 10000 items
        assert interpreter.global_scope['count'] == 10000
    
    def test_range_large_span(self):
        """def main() {\n    Test range with large span.\n}"""
        code = """
var items = range(0, 5000, 10)
var count = items.len()
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(0, 5000, 10) should produce 500 items
        assert interpreter.global_scope['count'] == 500
    
    def test_range_large_negative_step(self):
        """def main() {\n    Test range with large negative step.\n}"""
        code = """
var items = range(1000, 0, -10)
var count = items.len()
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(1000, 0, -10) should produce 100 items
        assert interpreter.global_scope['count'] == 100


class TestRangeInExpressions:
    """def main() {\n    Test range() used in various expression contexts.\n}"""
    
    def test_range_direct_indexing(self):
        """def main() {\n    Test indexing directly into range result.\n}"""
        code = """
var items = range(10, 20)
var first = items[0]
var last = items[9]
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(10, 20) produces [10, 11, ..., 19]
        assert interpreter.global_scope['first'] == 10
        assert interpreter.global_scope['last'] == 19
    
    def test_range_in_list_concatenation(self):
        """def main() {\n    Test using range result in concatenation.\n}"""
        code = """
var prefix = [0, 1]
var combined = prefix + range(2, 5)
var length = combined.len()
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # [0, 1] + [2, 3, 4] = 5 items
        assert interpreter.global_scope['length'] == 5
    
    def test_range_with_arr_methods(self):
        """def main() {\n    Test that range result supports arr methods.\n}"""
        code = """
var items = range(5, 10)
var max_val = items.max()
var min_val = items.min()
var total = items.sum()
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        # range(5, 10) = [5, 6, 7, 8, 9]
        assert interpreter.global_scope['max_val'] == 9
        assert interpreter.global_scope['min_val'] == 5
        assert interpreter.global_scope['total'] == 35  # 5+6+7+8+9
