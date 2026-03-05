# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""
Test suite for Lyric CLI functionality.
"""

import pytest
import sys
import os
import re
from unittest.mock import patch


class TestCLI:
    """Test cases for CLI functionality."""
    
    def test_cli_import(self):
        """Test that CLI module can be imported."""
        import lyric.cli
        assert hasattr(lyric.cli, 'main')
    
    def test_version_command(self):
        """Test --version command."""
        with patch('sys.argv', ['lyric', '--version']):
            with patch('sys.exit') as mock_exit:
                with patch('builtins.print') as mock_print:
                    from lyric.cli import main
                    main()
                    # Verify version format matches semantic versioning (e.g., 0.8.3, 1.12.1, 10.10.10)
                    mock_print.assert_called_once()
                    call_args = mock_print.call_args[0][0]
                    assert re.match(r'^Lyric \d+\.\d+\.\d+(\.\d+)?$', call_args), \
                        f"Version output '{call_args}' does not match expected format 'Lyric X.Y.Z' or 'Lyric X.Y.Z.W'"
    
    def test_run_command_valid_file(self):
        """Test run command with valid .ly file."""
        with patch('sys.argv', ['lyric', 'run', 'examples/hello.ly']):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', create=True) as mock_open:
                    with patch('lyric.cli.parse') as mock_parse:
                        with patch('lyric.cli.evaluate') as mock_evaluate:
                            # Mock file content
                            mock_open.return_value.__enter__.return_value.read.return_value = 'def main() { print("Hello, Lyric!") }'
                            
                            from lyric.cli import main
                            main()
                            
                            # Verify file was read
                            mock_open.assert_called_once_with('examples/hello.ly', 'r', encoding='utf-8')
                            # Verify parse was called
                            mock_parse.assert_called_once()
                            # Verify evaluate was called
                            mock_evaluate.assert_called_once()
    
    def test_run_command_file_not_found(self):
        """Test run command with non-existent file."""
        import tempfile
        import os
        
        # Create a temporary file and then delete it
        with tempfile.NamedTemporaryFile(suffix='.ly', delete=False) as tmp:
            temp_path = tmp.name
        
        # Delete the file so it doesn't exist
        os.unlink(temp_path)
        
        with patch('sys.argv', ['lyric', 'run', temp_path]):
            with patch('builtins.print') as mock_print:
                from lyric.cli import main
                try:
                    main()
                except SystemExit:
                    pass  # Expected due to sys.exit(1)
                # The CLI should print the file not found error
                mock_print.assert_called_with(f"Error: File '{temp_path}' not found")
    
    def test_run_command_invalid_extension(self):
        """Test run command with non-.ly file."""
        import tempfile
        
        # Create a temporary file with .txt extension
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            temp_path = tmp.name
        
        try:
            with patch('sys.argv', ['lyric', 'run', temp_path]):
                with patch('sys.exit') as mock_exit:
                    with patch('builtins.print') as mock_print:
                        from lyric.cli import main
                        try:
                            main()
                        except SystemExit:
                            pass  # Expected due to sys.exit(1)
                        # The CLI should print the invalid extension error
                        mock_print.assert_called_with(f"Error: File '{temp_path}' is not a .ly file")
                        mock_exit.assert_called_with(1)
        finally:
            # Clean up
            import os
            os.unlink(temp_path)
    
    def test_run_command_lexical_error(self):
        """Test run command with lexical error."""
        with patch('sys.argv', ['lyric', 'run', 'examples/error.ly']):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', create=True) as mock_open:
                    with patch('sys.exit') as mock_exit:
                        with patch('builtins.print') as mock_print:
                            # Mock file content with lexical error
                            mock_open.return_value.__enter__.return_value.read.return_value = 'def main() { print("unterminated string) }'
                            
                            from lyric.cli import main
                            try:
                                main()
                            except SystemExit:
                                pass  # Expected due to sys.exit(1)
                            
                            # Verify error was printed
                            mock_print.assert_called()
                            mock_exit.assert_called_with(1)
    
    def test_run_command_parse_error(self):
        """Test run command with parse error."""
        with patch('sys.argv', ['lyric', 'run', 'examples/error.ly']):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', create=True) as mock_open:
                    with patch('sys.exit') as mock_exit:
                        with patch('builtins.print') as mock_print:
                            # Mock file content with parse error
                            mock_open.return_value.__enter__.return_value.read.return_value = 'def main() { print("hello")'  # Missing closing brace
                            
                            from lyric.cli import main
                            try:
                                main()
                            except SystemExit:
                                pass  # Expected due to sys.exit(1)
                            
                            # Verify error was printed
                            mock_print.assert_called()
                            mock_exit.assert_called_with(1)
    
    def test_run_command_runtime_error(self):
        """Test run command with runtime error."""
        with patch('sys.argv', ['lyric', 'run', 'examples/error.ly']):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', create=True) as mock_open:
                    with patch('sys.exit') as mock_exit:
                        with patch('builtins.print') as mock_print:
                            # Mock file content with runtime error
                            mock_open.return_value.__enter__.return_value.read.return_value = 'def main() { print(undefined_var) }'
                            
                            from lyric.cli import main
                            try:
                                main()
                            except SystemExit:
                                pass  # Expected due to sys.exit(1)
                            
                            # Verify error was printed
                            mock_print.assert_called()
                            mock_exit.assert_called_with(1)
