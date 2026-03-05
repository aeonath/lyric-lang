# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for stdlib import infrastructure and reserved import names.

Tests that reserved names (lyric, lyrical, ly) resolve from the stdlib
lib/ directory and cannot be shadowed by user modules.
"""

import os
import tempfile
import pytest
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter, LyricModuleNamespace
from lyric.errors import RuntimeErrorLyric


def parse(source: str):
    """Helper to parse source code."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


def evaluate(ast, source_file=None):
    """Helper to evaluate an AST. Returns the interpreter instance."""
    interpreter = Interpreter(source_file=source_file)
    interpreter.evaluate(ast)
    return interpreter


class TestDottedImportParsing:
    """Tests that the parser handles dotted import names."""

    def test_parse_simple_import(self):
        """import mymodule parses as module_name='mymodule'"""
        ast = parse('import mymodule')
        node = ast.statements[0]
        assert node.module_name == 'mymodule'

    def test_parse_dotted_import(self):
        """import lyric.math parses as module_name='lyric.math'"""
        ast = parse('import lyric.math')
        node = ast.statements[0]
        assert node.module_name == 'lyric.math'

    def test_parse_deep_dotted_import(self):
        """import lyric.math.trig parses correctly"""
        ast = parse('import lyric.math.trig')
        node = ast.statements[0]
        assert node.module_name == 'lyric.math.trig'

    def test_parse_dotted_import_with_selective(self):
        """import lyric.math; sin, cos parses correctly"""
        ast = parse('import lyric.math; sin, cos')
        node = ast.statements[0]
        assert node.module_name == 'lyric.math'
        assert node.symbols == [('sin', None), ('cos', None)]

    def test_parse_dotted_import_with_alias(self):
        """import lyric.math; sin as sine parses correctly"""
        ast = parse('import lyric.math; sin as sine')
        node = ast.statements[0]
        assert node.module_name == 'lyric.math'
        assert node.symbols == [('sin', 'sine')]


class TestStdlibResolution:
    """Tests that reserved names resolve from stdlib lib/ directory."""

    def test_import_lyric_succeeds(self):
        """import lyric should load from lib/lyric/lyric.ly"""
        ast = parse('import lyric')
        interp = evaluate(ast)
        assert 'lyric' in interp.global_scope
        assert isinstance(interp.global_scope['lyric'], LyricModuleNamespace)

    def test_import_lyric_math_succeeds(self):
        """import lyric.math should load from lib/lyric/math.ly"""
        ast = parse('import lyric.math')
        interp = evaluate(ast)
        assert 'lyric' in interp.global_scope
        ns = interp.global_scope['lyric']
        assert isinstance(ns, LyricModuleNamespace)
        assert 'math' in ns._scope
        assert isinstance(ns._scope['math'], LyricModuleNamespace)

    def test_nonexistent_stdlib_module_error(self):
        """import lyric.nonexistent should fail with stdlib error"""
        ast = parse('import lyric.nonexistent')
        with pytest.raises(RuntimeErrorLyric, match="not available in the current version"):
            evaluate(ast)

    def test_stdlib_error_mentions_standard_library(self):
        """Error for missing stdlib module should mention 'standard library'"""
        ast = parse('import lyric.nonexistent')
        with pytest.raises(RuntimeErrorLyric, match="standard library"):
            evaluate(ast)

    def test_import_lyrical_not_yet_available(self):
        """import lyrical should fail (no lyrical dir/file in stdlib yet)"""
        ast = parse('import lyrical')
        with pytest.raises(RuntimeErrorLyric, match="not available in the current version"):
            evaluate(ast)


class TestReservedNameProtection:
    """Tests that reserved names cannot be shadowed by user modules."""

    def test_import_ly_reserved(self):
        """import ly should still be reserved"""
        ast = parse('import ly')
        with pytest.raises(RuntimeErrorLyric, match="reserved module name"):
            evaluate(ast)

    def test_import_ly_dotted_reserved(self):
        """import ly.math should still be reserved"""
        ast = parse('import ly.math')
        with pytest.raises(RuntimeErrorLyric, match="reserved module name"):
            evaluate(ast)

    def test_lyric_not_shadowed_by_user_file(self):
        """User lyric.ly in cwd should NOT override stdlib import lyric"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a user lyric.ly with a distinct variable
            user_file = os.path.join(tmpdir, 'lyric.ly')
            with open(user_file, 'w') as f:
                f.write('var user_shadow = 42\n')

            script_path = os.path.join(tmpdir, 'test.ly')

            ast = parse('import lyric')
            interp = evaluate(ast, source_file=script_path)

            ns = interp.global_scope['lyric']
            # Should NOT have user_shadow — loaded from stdlib, not user file
            assert not ns.has_variable('user_shadow')


class TestImportDepthCap:
    """Tests that import depth is capped."""

    def test_depth_exceeds_max(self):
        """Import with more than 8 levels should fail"""
        code = 'import a.b.c.d.e.f.g.h.i'
        ast = parse(code)
        with pytest.raises(RuntimeErrorLyric, match="import depth exceeds maximum"):
            evaluate(ast)
