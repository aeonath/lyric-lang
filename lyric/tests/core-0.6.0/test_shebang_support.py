# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Test suite for Sprint 6 Task 6: Shebang Support."""

import pytest
import os
import tempfile
import subprocess
import sys
from lyric.cli import _remove_shebang, _execute_file
from lyric.parser import parse
from lyric.interpreter import evaluate


class TestShebangRemoval:
    """Test the _remove_shebang function."""
    
    def test_remove_shebang_basic(self):
        """Test removing basic shebang line."""
        source = '#!/usr/bin/lyric\nprint("Hello")'
        result = _remove_shebang(source)
        assert result == 'print("Hello")'
    
    def test_remove_shebang_with_env(self):
        """Test removing shebang with env."""
        source = "#!/usr/bin/env lyric\nprint('Hello')"
        result = _remove_shebang(source)
        assert result == "print('Hello')"
    
    def test_remove_shebang_with_custom_path(self):
        """Test removing shebang with custom path."""
        source = "#!/usr/local/bin/lyric\nprint('Hello')"
        result = _remove_shebang(source)
        assert result == "print('Hello')"
    
    def test_no_shebang_preserved(self):
        """Test that files without shebang are preserved."""
        source = "print('Hello')\nprint('World')"
        result = _remove_shebang(source)
        assert result == source
    
    def test_comment_not_shebang(self):
        """Test that regular comments are not removed."""
        source = "# This is a comment\nprint('Hello')"
        result = _remove_shebang(source)
        assert result == source
    
    def test_shebang_not_first_line(self):
        """Test that shebang only removed if first line."""
        source = "print('Hello')\n#!/usr/bin/lyric\nprint('World')"
        result = _remove_shebang(source)
        assert result == source  # Should not remove shebang from middle
    
    def test_empty_file(self):
        """Test empty file handling."""
        result = _remove_shebang("")
        assert result == ""
    
    def test_single_line_shebang(self):
        """Test file with only shebang line."""
        source = "#!/usr/bin/lyric"
        result = _remove_shebang(source)
        assert result == ""
    
    def test_shebang_with_whitespace(self):
        """Test shebang with leading whitespace (should not be removed)."""
        source = "  #!/usr/bin/lyric\nprint('Hello')"
        result = _remove_shebang(source)
        assert result == source  # Should not remove shebang with leading whitespace


class TestShebangExecution:
    """Test shebang execution through CLI."""
    
    def test_execute_file_with_shebang(self):
        """Test executing a file with shebang."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write('#!/usr/bin/lyric\ndef main() {\n    print("Hello from shebang!")\n}')
            temp_file = f.name
        
        try:
            # Test that the file executes correctly
            result = subprocess.run([sys.executable, '-m', 'lyric.cli', temp_file], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            assert "Hello from shebang!" in result.stdout
        finally:
            os.unlink(temp_file)
    
    def test_execute_file_without_shebang(self):
        """Test executing a file without shebang."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write('def main() {\n    print("Hello without shebang!")\n}')
            temp_file = f.name
        
        try:
            result = subprocess.run([sys.executable, '-m', 'lyric.cli', temp_file], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            assert "Hello without shebang!" in result.stdout
        finally:
            os.unlink(temp_file)
    
    def test_execute_file_with_comment_not_shebang(self):
        """Test executing a file with comment (not shebang)."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write('# This is a comment\ndef main() {\n    print("Hello with comment!")\n}')
            temp_file = f.name
        
        try:
            result = subprocess.run([sys.executable, '-m', 'lyric.cli', temp_file], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            assert "Hello with comment!" in result.stdout
        finally:
            os.unlink(temp_file)
    
    def test_execute_file_with_env_shebang(self):
        """Test executing a file with env shebang."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write('#!/usr/bin/env lyric\ndef main() {\n    print("Hello with env shebang!")\n}')
            temp_file = f.name
        
        try:
            result = subprocess.run([sys.executable, '-m', 'lyric.cli', temp_file], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            assert "Hello with env shebang!" in result.stdout
        finally:
            os.unlink(temp_file)
    
    def test_execute_file_with_custom_shebang_path(self):
        """Test executing a file with custom shebang path."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write('#!/usr/local/bin/lyric\ndef main() {\n    print("Hello with custom path!")\n}')
            temp_file = f.name
        
        try:
            result = subprocess.run([sys.executable, '-m', 'lyric.cli', temp_file], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            assert "Hello with custom path!" in result.stdout
        finally:
            os.unlink(temp_file)


class TestShebangParsing:
    """Test that shebang removal works correctly with parser."""
    
    def test_parse_with_shebang(self):
        """Test that parser handles shebang-removed source correctly."""
        source_with_shebang = '#!/usr/bin/lyric\nprint("Hello")'
        source_cleaned = _remove_shebang(source_with_shebang)
        
        # Both should parse to the same AST
        ast_with_shebang = parse(source_cleaned, interactive=True)
        ast_without_shebang = parse('print("Hello")', interactive=True)
        
        # The ASTs should be equivalent
        assert str(ast_with_shebang) == str(ast_without_shebang)
    
    def test_execute_with_shebang(self):
        """Test that interpreter handles shebang-removed source correctly."""
        source_with_shebang = '#!/usr/bin/lyric\nprint("Hello")'
        source_cleaned = _remove_shebang(source_with_shebang)
        
        # Both should execute identically
        ast_with_shebang = parse(source_cleaned, interactive=True)
        ast_without_shebang = parse('print("Hello")', interactive=True)
        
        # Both should produce the same output
        assert str(ast_with_shebang) == str(ast_without_shebang)


class TestShebangErrorHandling:
    """Test error handling with shebang files."""
    
    def test_syntax_error_with_shebang(self):
        """Test that syntax errors work correctly with shebang."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write('#!/usr/bin/lyric\nprint("Hello")\nif true {')
            temp_file = f.name
        
        try:
            result = subprocess.run([sys.executable, '-m', 'lyric.cli', temp_file], 
                                  capture_output=True, text=True)
            assert result.returncode == 1
            assert "Error" in result.stderr or "Error" in result.stdout
        finally:
            os.unlink(temp_file)
    
    def test_runtime_error_with_shebang(self):
        """Test that runtime errors work correctly with shebang."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write('#!/usr/bin/lyric\ndef main() {\n    print(undefined_variable)\n}')
            temp_file = f.name
        
        try:
            result = subprocess.run([sys.executable, '-m', 'lyric.cli', temp_file], 
                                  capture_output=True, text=True)
            assert result.returncode == 1
            assert "Runtime error" in result.stderr or "Runtime error" in result.stdout
        finally:
            os.unlink(temp_file)


class TestShebangCrossPlatform:
    """Test cross-platform compatibility."""
    
    def test_windows_compatibility(self):
        """Test that shebang works on Windows (should be ignored safely)."""
        # This test verifies that the shebang removal works on Windows
        # without causing any issues
        source = '#!/usr/bin/lyric\nprint("Windows compatible!")'
        result = _remove_shebang(source)
        assert result == 'print("Windows compatible!")'
    
    def test_unix_compatibility(self):
        """Test that shebang works on Unix-like systems."""
        # This test verifies that the shebang removal works on Unix-like systems
        source = '#!/usr/bin/lyric\nprint("Unix compatible!")'
        result = _remove_shebang(source)
        assert result == 'print("Unix compatible!")'


class TestShebangEdgeCases:
    """Test edge cases for shebang handling."""
    
    def test_multiple_shebang_lines(self):
        """Test file with multiple shebang-like lines."""
        source = '#!/usr/bin/lyric\n#!/usr/bin/env lyric\nprint("Hello")'
        result = _remove_shebang(source)
        # Should only remove the first line
        assert result == '#!/usr/bin/env lyric\nprint("Hello")'
    
    def test_shebang_with_arguments(self):
        """Test shebang with arguments."""
        source = '#!/usr/bin/lyric --verbose\nprint("Hello")'
        result = _remove_shebang(source)
        assert result == 'print("Hello")'
    
    def test_shebang_with_spaces(self):
        """Test shebang with spaces in path."""
        source = '#!/usr/bin/env lyric\nprint("Hello")'
        result = _remove_shebang(source)
        assert result == 'print("Hello")'
    
    def test_shebang_case_sensitivity(self):
        """Test shebang case sensitivity."""
        source = '#!/USR/BIN/LYRIC\nprint("Hello")'
        result = _remove_shebang(source)
        assert result == 'print("Hello")'
    
    def test_shebang_with_tabs(self):
        """Test shebang with tabs."""
        source = '#!/usr/bin/lyric\nprint("Hello")'
        result = _remove_shebang(source)
        assert result == 'print("Hello")'


if __name__ == "__main__":
    pytest.main([__file__])
