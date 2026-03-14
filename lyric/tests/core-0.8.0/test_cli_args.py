# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for command-line arguments (Sprint 9 Task 6)."""

import pytest
import subprocess
import sys
import tempfile
import os


def test_main_with_no_arguments():
    """Test main() with no parameters when no arguments provided."""
    code = """
def main() {
    print("Hello from main")
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['lyric', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Hello from main" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_main_with_argc_argv():
    """Test main(argc, argv) receives command-line arguments."""
    code = """
def main(int argc, arr argv) {
    print("argc:", argc)
    print("argv:", argv)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['lyric', temp_file, 'arg1', 'arg2', 'arg3'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "argc: 3" in result.stdout
        assert "['arg1', 'arg2', 'arg3']" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_main_with_options_and_arguments():
    """Test that options and arguments are properly separated."""
    code = """
def main(int argc, arr argv) {
    god a = getopts("a", None)
    god verbose = getopts(None, "verbose")

    print("Option -a:", a)
    print("Option --verbose:", verbose)
    print("argc:", argc)
    print("argv:", argv)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['lyric', temp_file, '-a', '--verbose', 'arg1', 'arg2'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Option -a: True" in result.stdout
        assert "Option --verbose: True" in result.stdout
        assert "argc: 2" in result.stdout
        assert "['arg1', 'arg2']" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_main_accessing_argv_elements():
    """Test accessing individual argv elements."""
    code = """
def main(int argc, arr argv) {
    if argc == 2
        str var1 = argv[0]
        str var2 = argv[1]
        print("First arg:", var1)
        print("Second arg:", var2)
    else
        print("Expected 2 arguments, got:", argc)
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['lyric', temp_file, 'hello', 'world'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "First arg: hello" in result.stdout
        assert "Second arg: world" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_main_with_zero_arguments():
    """Test main(argc, argv) when no arguments are provided."""
    code = """
def main(int argc, arr argv) {
    print("argc:", argc)
    if argc == 0
        print("No arguments provided")
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['lyric', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "argc: 0" in result.stdout
        assert "No arguments provided" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_spec_example():
    """Test the exact example from Sprint 9 Task 6 specification."""
    code = """
def main(int argc, arr argv) {
    god a = getopts("a", None)
    if argc == 2
        str var1 = argv[0]
        str var2 = argv[1]
        print("a:", a)
        print("var1:", var1)
        print("var2:", var2)
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        # Command: lyric myprogram -a arg1 arg2
        result = subprocess.run(
            ['lyric', temp_file, '-a', 'arg1', 'arg2'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "a: True" in result.stdout
        assert "var1: arg1" in result.stdout
        assert "var2: arg2" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_arguments_with_run_command():
    """Test that arguments work with 'lyric run' command."""
    code = """
def main(int argc, arr argv) {
    print("Arguments:", argc)
    var arg
    for arg in argv
        print("  -", arg)
    done
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['lyric', 'run', temp_file, 'test1', 'test2'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Arguments: 2" in result.stdout
        assert "- test1" in result.stdout
        assert "- test2" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_mixed_options_values_and_arguments():
    """Test complex mix of options with values and arguments."""
    code = """
def main(int argc, arr argv) {
    god a = getopts("a", None)
    var file = getopts(None, "file")
    god verbose = getopts(None, "verbose")
    
    print("Options:")
    print("  a =", a)
    print("  file =", file)
    print("  verbose =", verbose)
    print("Arguments:", argc)
    var arg
    for arg in argv
        print("  arg:", arg)
    done
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['lyric', temp_file, '-a', '--file=data.txt', 
             'input1.txt', '--verbose', 'input2.txt'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "a = True" in result.stdout
        assert "file = data.txt" in result.stdout
        assert "verbose = True" in result.stdout
        assert "Arguments: 2" in result.stdout
        assert "arg: input1.txt" in result.stdout
        assert "arg: input2.txt" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_argv_len_method():
    """Test using argv.len() method."""
    code = """
def main(int argc, arr argv) {
    int length = argv.len()
    print("argc:", argc)
    print("argv.len():", length)
    if argc == length
        print("argc matches argv.len()")
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['lyric', temp_file, 'a', 'b', 'c'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "argc: 3" in result.stdout
        assert "argv.len(): 3" in result.stdout
        assert "argc matches argv.len()" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_numeric_string_arguments():
    """Test that arguments remain as strings even if they look numeric."""
    code = """
def main(int argc, arr argv) {
    if argc > 0
        str first = argv[0]
        print("Type:", type(first))
        print("Value:", first)
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['lyric', temp_file, '123'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Type: str" in result.stdout
        assert "Value: 123" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)

