# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""def main() {\n    
Test suite for bin() and god() casting functions.
Tests boolean conversion from various types.
\n}"""

import pytest
from lyric.parser import parse
from lyric.interpreter import Interpreter


class TestBinCasting:
    """def main() {\n    Test cases for bin() boolean casting function.\n}"""
    
    def test_bin_with_nonzero_int(self):
        """def main() {\n    Test bin() with non-zero integer returns True.\n}"""
        code = """
int x = 5
god result = bin(x)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_zero_int(self):
        """def main() {\n    Test bin() with zero integer returns False.\n}"""
        code = """
int y = 0
god result = bin(y)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_bin_with_negative_int(self):
        """def main() {\n    Test bin() with negative integer returns True.\n}"""
        code = """
int z = -10
god result = bin(z)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_nonzero_float(self):
        """def main() {\n    Test bin() with non-zero float returns True.\n}"""
        code = """
flt x = 3.14
god result = bin(x)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_zero_float(self):
        """def main() {\n    Test bin() with zero float returns False.\n}"""
        code = """
flt y = 0.0
god result = bin(y)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_bin_with_nonempty_string(self):
        """def main() {\n    Test bin() with non-empty string returns True.\n}"""
        code = """
str s = "hello"
god result = bin(s)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_empty_string(self):
        """def main() {\n    Test bin() with empty string returns False.\n}"""
        code = """
str s = ""
god result = bin(s)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_bin_with_nonempty_arr(self):
        """def main() {\n    Test bin() with non-empty array returns True.\n}"""
        code = """
arr items = [1, 2, 3]
god result = bin(items)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_empty_arr(self):
        """def main() {\n    Test bin() with empty array returns False.\n}"""
        code = """
arr items = []
god result = bin(items)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_bin_with_nonempty_map(self):
        """def main() {\n    Test bin() with non-empty map returns True.\n}"""
        code = """
map data = {"key": "value"}
god result = bin(data)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_empty_map(self):
        """def main() {\n    Test bin() with empty map returns False.\n}"""
        code = """
map data = {}
god result = bin(data)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_bin_with_true(self):
        """def main() {\n    Test bin() with True returns True.\n}"""
        code = """
god x = True
god result = bin(x)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_bin_with_false(self):
        """def main() {\n    Test bin() with False returns False.\n}"""
        code = """
god x = False
god result = bin(x)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False


class TestGodCasting:
    """def main() {\n    Test cases for god() boolean casting function.\n}"""
    
    def test_god_with_nonzero_int(self):
        """def main() {\n    Test god() with non-zero integer returns True.\n}"""
        code = """
int x = 5
god result = god(x)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_zero_int(self):
        """def main() {\n    Test god() with zero integer returns False.\n}"""
        code = """
int y = 0
god result = god(y)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_god_with_negative_int(self):
        """def main() {\n    Test god() with negative integer returns True.\n}"""
        code = """
int z = -10
god result = god(z)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_nonzero_float(self):
        """def main() {\n    Test god() with non-zero float returns True.\n}"""
        code = """
flt x = 3.14
god result = god(x)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_zero_float(self):
        """def main() {\n    Test god() with zero float returns False.\n}"""
        code = """
flt y = 0.0
god result = god(y)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_god_with_nonempty_string(self):
        """def main() {\n    Test god() with non-empty string returns True.\n}"""
        code = """
str s = "hello"
god result = god(s)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_empty_string(self):
        """def main() {\n    Test god() with empty string returns False.\n}"""
        code = """
str s = ""
god result = god(s)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_god_with_nonempty_arr(self):
        """def main() {\n    Test god() with non-empty array returns True.\n}"""
        code = """
arr items = [1, 2, 3]
god result = god(items)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_empty_arr(self):
        """def main() {\n    Test god() with empty array returns False.\n}"""
        code = """
arr items = []
god result = god(items)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_god_with_nonempty_map(self):
        """def main() {\n    Test god() with non-empty map returns True.\n}"""
        code = """
map data = {"key": "value"}
god result = god(data)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_empty_map(self):
        """def main() {\n    Test god() with empty map returns False.\n}"""
        code = """
map data = {}
god result = god(data)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False
    
    def test_god_with_true(self):
        """def main() {\n    Test god() with True returns True.\n}"""
        code = """
god x = True
god result = god(x)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is True
    
    def test_god_with_false(self):
        """def main() {\n    Test god() with False returns False.\n}"""
        code = """
god x = False
god result = god(x)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] is False


