# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Integration tests for CLI error messages."""

import pytest
import subprocess
import sys
import os
from unittest.mock import patch


def test_cli_class_test_output():
    """Test CLI run of class_test.ly produces correct greeting (A19)."""
    # Get the path to the class_test.ly file
    class_test_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'class_test.ly')
    
    # Run the CLI command
    result = subprocess.run(['lyric', 'run', class_test_path], 
                           capture_output=True, text=True)
    
    # Should succeed (exit code 0)
    assert result.returncode == 0
    
    # Check that the output contains expected greetings
    output = result.stdout
    assert "Testing class functionality in Lyric" in output
    assert "Hello, I'm Guest" in output
    assert "Hello, I'm Alice" in output
    assert "Hi, I'm Student" in output
    assert "Hi, I'm Bob" in output


def test_cli_error_demo_output():
    """Test CLI run of error_demo.ly produces expected error messages without Python tracebacks (A20)."""
    # Get the path to the error_demo.ly file
    error_demo_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'error_demo.ly')
    
    # Run the CLI command
    result = subprocess.run(['lyric', 'run', error_demo_path], 
                           capture_output=True, text=True)
    
    # Should fail (exit code 1) due to undefined variable
    assert result.returncode == 1
    
    # Check that stdout contains the proper error message
    output = result.stdout
    assert "Testing error handling in Lyric" in output
    assert "This will cause an error:" in output
    assert "Runtime error:" in output
    assert "Undefined variable" in output
    assert "'undefined_variable' has not been declared" in output
    
    # Ensure no Python traceback appears
    assert "Traceback (most recent call last):" not in output
    assert "File \"" not in output


def test_cli_nested_flow_output():
    """Test CLI run of nested_flow.ly produces correct output."""
    # Get the path to the nested_flow.ly file
    nested_flow_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'nested_flow.ly')
    
    # Run the CLI command
    result = subprocess.run(['lyric', 'run', nested_flow_path], 
                           capture_output=True, text=True)
    
    # Should succeed (exit code 0)
    assert result.returncode == 0
    
    # Check that the output contains expected nested flow results
    output = result.stdout
    assert "Testing nested control flow in Lyric" in output
    assert "x is positive" in output
    assert "x is greater than 3" in output
    assert "Outer loop:" in output
    assert "Inner loop:" in output
    assert "First iteration" in output
    assert "Second iteration" in output


def test_cli_file_not_found_error():
    """Test CLI error handling for non-existent files."""
    # Run the CLI command with a non-existent file
    result = subprocess.run(['lyric', 'run', 'nonexistent.ly'], 
                           capture_output=True, text=True)
    
    # Should fail (exit code 1)
    assert result.returncode == 1
    
    # Check that the error message is appropriate
    output = result.stdout
    assert "Error:" in output or "Runtime error:" in output


def test_cli_invalid_extension_error():
    """Test CLI error handling for files with invalid extensions."""
    # Create a temporary file with wrong extension
    temp_file = "temp.txt"
    with open(temp_file, 'w') as f:
        f.write('print("hello")')
    
    try:
        # Run the CLI command with wrong extension
        result = subprocess.run(['lyric', 'run', temp_file], 
                               capture_output=True, text=True)
        
        # Should fail (exit code 1)
        assert result.returncode == 1
        
        # Check that the error message is appropriate
        output = result.stdout
        assert "Error:" in output or "Runtime error:" in output
        
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_cli_syntax_error_handling():
    """Test CLI error handling for syntax errors."""
    # Create a temporary file with syntax error
    temp_file = "syntax_error.ly"
    with open(temp_file, 'w') as f:
        f.write('def main() {\n    if true\n        print("missing end")\n}')
    
    try:
        # Run the CLI command
        result = subprocess.run(['lyric', 'run', temp_file], 
                               capture_output=True, text=True)
        
        # Should fail (exit code 1)
        assert result.returncode == 1
        
        # Check that the error message is appropriate
        output = result.stdout
        assert "Error:" in output or "Parse error:" in output or "Error [line" in output
        
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)
