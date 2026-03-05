# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for selective importpy syntax.

Tests:
- importpy module; Name1, Name2  — binds named attributes directly into scope
- importpy module  (unchanged)   — binds whole module proxy as before
- Classes and functions both wrapped correctly so arg conversion works
- AttributeError on unknown name
- Blacklisted module still blocked
- Both forms can coexist in the same program
"""

import pytest
import sys
import io
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.pyproxy import PyCallableProxy
from lyric.errors import RuntimeErrorLyric


def parse(source: str, interactive: bool = False):
    tokens = tokenize(source)
    parser = Parser(tokens)
    if interactive:
        parser._interactive_mode = True
        parser.is_top_level = False
    return parser.parse()


def evaluate(ast):
    interpreter = Interpreter()
    interpreter.evaluate(ast)
    return interpreter


def run_code_capture(code: str) -> str:
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        ast = parse(code, interactive=True)
        interp = Interpreter()
        interp.evaluate(ast)
    finally:
        sys.stdout = old_stdout
    return captured.getvalue().strip()


class TestImportPySelective:
    """Test selective importpy: importpy module; Name1, Name2"""

    # --- Parser / AST ---

    def test_parse_selective_stores_names(self):
        """Parser captures the selective name list in ImportPyNode."""
        from lyric.ast_nodes import ImportPyNode
        ast = parse("importpy math; sqrt, pi", interactive=True)
        node = ast.statements[0]
        assert isinstance(node, ImportPyNode)
        assert node.module_name == 'math'
        assert node.names == ['sqrt', 'pi']

    def test_parse_whole_module_names_is_none(self):
        """Whole-module form sets names=None."""
        from lyric.ast_nodes import ImportPyNode
        ast = parse("importpy math", interactive=True)
        node = ast.statements[0]
        assert isinstance(node, ImportPyNode)
        assert node.names is None

    def test_parse_single_name(self):
        """Single name after semicolon is captured."""
        from lyric.ast_nodes import ImportPyNode
        ast = parse("importpy math; sqrt", interactive=True)
        node = ast.statements[0]
        assert node.names == ['sqrt']

    def test_parse_dotted_module_selective(self):
        """Dotted module name works with selective list."""
        from lyric.ast_nodes import ImportPyNode
        ast = parse("importpy http.server; HTTPServer, SimpleHTTPRequestHandler", interactive=True)
        node = ast.statements[0]
        assert node.module_name == 'http.server'
        assert node.names == ['HTTPServer', 'SimpleHTTPRequestHandler']

    # --- Runtime: selective binding ---

    def test_selective_function_bound_directly(self):
        """Selectively imported function is bound directly in scope."""
        interp = evaluate(parse("importpy math; sqrt", interactive=True))
        assert 'sqrt' in interp.global_scope
        assert 'math' not in interp.global_scope

    def test_selective_constant_bound_directly(self):
        """Selectively imported constant (pi) is bound in scope."""
        interp = evaluate(parse("importpy math; pi", interactive=True))
        import math
        assert abs(interp.global_scope['pi'] - math.pi) < 1e-10

    def test_selective_callable_is_proxied(self):
        """Selectively imported callable is wrapped in PyCallableProxy."""
        interp = evaluate(parse("importpy math; sqrt", interactive=True))
        assert isinstance(interp.global_scope['sqrt'], PyCallableProxy)

    def test_selective_class_is_proxied(self):
        """Selectively imported class is also wrapped in PyCallableProxy."""
        interp = evaluate(parse("importpy http.server; HTTPServer", interactive=True))
        assert isinstance(interp.global_scope['HTTPServer'], PyCallableProxy)

    def test_selective_function_callable(self):
        """Selectively imported sqrt() can be called."""
        output = run_code_capture("importpy math; sqrt\nprint sqrt(25.0)")
        assert output == '5.0'

    def test_selective_multiple_names(self):
        """Multiple names all bound correctly."""
        code = "importpy math; sqrt, floor, ceil\nprint sqrt(9.0)\nprint floor(2.9)\nprint ceil(2.1)"
        output = run_code_capture(code)
        assert output == '3.0\n2\n3'

    def test_selective_http_server_class(self):
        """HTTPServer class imported selectively can be instantiated."""
        code = """
importpy http.server; HTTPServer, SimpleHTTPRequestHandler
var httpd = HTTPServer(("127.0.0.1", 9999), SimpleHTTPRequestHandler)
print "ok"
"""
        assert run_code_capture(code) == 'ok'

    # --- Whole-module form unchanged ---

    def test_whole_module_still_works(self):
        """Whole-module importpy still binds to the last component name."""
        interp = evaluate(parse("importpy math", interactive=True))
        assert 'math' in interp.global_scope
        assert 'sqrt' not in interp.global_scope

    def test_both_forms_coexist(self):
        """Selective and whole-module imports can coexist."""
        code = "importpy math; sqrt\nimportpy math\nprint sqrt(16.0)\nprint math.floor(3.7)"
        output = run_code_capture(code)
        assert output == '4.0\n3'

    # --- Error handling ---

    def test_unknown_name_raises(self):
        """Importing a name that doesn't exist in the module raises RuntimeError."""
        with pytest.raises(RuntimeErrorLyric):
            evaluate(parse("importpy math; nonexistent_function", interactive=True))

    def test_blacklisted_module_still_blocked(self):
        """Selective import from a blacklisted module is still rejected."""
        with pytest.raises(RuntimeErrorLyric):
            evaluate(parse("importpy pdb; run", interactive=True))
