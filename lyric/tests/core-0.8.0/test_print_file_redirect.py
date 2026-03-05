# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for print statement with file redirection (print "text" ->> file)."""

import pytest
import subprocess
import sys
import tempfile
import os


def test_print_append_to_file():
    """Test print "text" ->> dsk appends with newline."""
    code = """
def main() {
    dsk myfile = disk("test_print_append.txt")
    print "Hello" ->> myfile
    print "World" ->> myfile
    myfile.close()

    dsk readfile = disk("test_print_append.txt")
    str content = readfile.read()
    print(content)
    readfile.close()
    readfile.delete()
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True
        )
        # print adds newline, so file should contain "Hello\nWorld\n"
        assert "Hello\nWorld\n" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_print_overwrite_file():
    """Test print "text" -> dsk overwrites with newline."""
    code = """
def main() {
    dsk myfile = disk("test_print_overwrite.txt")
    print "First" -> myfile
    print "Second" -> myfile
    myfile.close()

    dsk readfile = disk("test_print_overwrite.txt")
    str content = readfile.read()
    print(content)
    readfile.close()
    readfile.delete()
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True
        )
        assert "Second\n" in result.stdout
        assert "First" not in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_print_multiple_args_to_file():
    """Test print with multiple args appended to file."""
    code = """
def main() {
    dsk myfile = disk("test_print_multi.txt")
    str name = "World"
    print "Hello", name ->> myfile
    myfile.close()

    dsk readfile = disk("test_print_multi.txt")
    str content = readfile.read()
    print(content)
    readfile.close()
    readfile.delete()
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True
        )
        assert "Hello World\n" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_print_expression_to_file():
    """Test print with string concatenation to file."""
    code = """
def main() {
    dsk myfile = disk("test_print_expr.txt")
    str title = "My Post"
    print "title: " + title ->> myfile
    myfile.close()

    dsk readfile = disk("test_print_expr.txt")
    str content = readfile.read()
    print(content)
    readfile.close()
    readfile.delete()
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True
        )
        assert "title: My Post\n" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_print_append_builds_multiline_file():
    """Test building a multi-line file with print ->> (like pulse.ly)."""
    code = """
def main() {
    dsk myfile = disk("test_print_multiline.txt")
    print "---" ->> myfile
    print "title: Hello" ->> myfile
    print "date: 2026-03-01" ->> myfile
    print "---" ->> myfile
    print "" ->> myfile
    print "Content here." ->> myfile
    myfile.close()

    dsk readfile = disk("test_print_multiline.txt")
    str content = readfile.read()
    print(content)
    readfile.close()
    readfile.delete()
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True
        )
        assert "---\ntitle: Hello\ndate: 2026-03-01\n---\n\nContent here.\n" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_print_does_not_echo_to_stdout():
    """Test that print ->> file does NOT also print to stdout."""
    code = """
def main() {
    dsk myfile = disk("test_print_no_echo.txt")
    print "secret" ->> myfile
    print("visible")
    myfile.close()

    dsk readfile = disk("test_print_no_echo.txt")
    readfile.close()
    readfile.delete()
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True
        )
        # "secret" should only be in the file, not stdout
        assert "visible" in result.stdout
        assert "secret" not in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_print_funcall_syntax_still_works():
    """Test that print() with parens still works normally."""
    code = """
def main() {
    print("Hello from parens")
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True
        )
        assert "Hello from parens" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_print_statement_without_redirect_still_works():
    """Test that print "text" without redirect still prints to stdout."""
    code = """
def main() {
    print "Hello stdout"
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True
        )
        assert "Hello stdout" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)
