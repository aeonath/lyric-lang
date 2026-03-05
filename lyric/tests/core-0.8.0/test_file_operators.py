# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for file operator functionality (Sprint 9 Task 9)."""

import pytest
import subprocess
import sys
import tempfile
import os


def test_string_append_to_file():
    """Test str ->> dsk (append string to file)."""
    code = """
def main() {
    dsk myfile = disk("test_append.txt")
    str text = "Hello"
    text ->> myfile
    str text2 = "World"
    text2 ->> myfile
    myfile.close()
    
    dsk readfile = disk("test_append.txt")
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
        assert "HelloWorld" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_string_overwrite_file():
    """Test str -> dsk (overwrite file)."""
    code = """
def main() {
    dsk myfile = disk("test_overwrite.txt")
    str text1 = "First"
    text1 -> myfile
    str text2 = "Second"
    text2 -> myfile
    myfile.close()
    
    dsk readfile = disk("test_overwrite.txt")
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
        assert "Second" in result.stdout
        assert "First" not in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_string_read_from_file():
    """Test str <- dsk (read file to string)."""
    code = """
def main() {
    dsk myfile = disk("test_read.txt")
    str data = "Test content"
    data -> myfile
    myfile.close()
    
    str content
    dsk readfile = disk("test_read.txt")
    content <- readfile
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
        assert "Test content" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_array_append_to_file():
    """Test arr ->> dsk (write array lines to file, append)."""
    code = """
def main() {
    dsk myfile = disk("test_arr_append.txt")
    arr numbers = [1, 2, 3]
    numbers ->> myfile
    myfile.close()
    
    dsk readfile = disk("test_arr_append.txt")
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
        lines = result.stdout.strip().split('\n')
        assert "1" in result.stdout
        assert "2" in result.stdout
        assert "3" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_array_read_from_file():
    """Test arr <- dsk (read file lines to array)."""
    code = """
def main() {
    dsk myfile = disk("test_arr_read.txt")
    str data = "line1\\nline2\\nline3"
    data -> myfile
    myfile.close()
    
    arr lines
    dsk readfile = disk("test_arr_read.txt")
    lines <- readfile
    print(lines.len())
    print(lines[0])
    print(lines[1])
    print(lines[2])
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
        assert "3" in result.stdout
        assert "line1" in result.stdout
        assert "line2" in result.stdout
        assert "line3" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_array_overwrite_file():
    """Test arr -> dsk (overwrite file with array lines)."""
    code = """
def main() {
    dsk myfile = disk("test_arr_overwrite.txt")
    arr first = [1, 2]
    first -> myfile
    arr second = [3, 4, 5]
    second -> myfile
    myfile.close()
    
    dsk readfile = disk("test_arr_overwrite.txt")
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
        # Should only contain second array content
        assert "3" in result.stdout
        assert "4" in result.stdout
        assert "5" in result.stdout
        # Should not contain first array
        assert result.stdout.count("1") == 0
        assert result.stdout.count("2") == 0
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_int_to_file():
    """Test int ->> dsk (append integer to file)."""
    code = """
def main() {
    dsk myfile = disk("test_int.txt")
    int num = 42
    num ->> myfile
    myfile.close()
    
    dsk readfile = disk("test_int.txt")
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
        assert "42" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_error_write_to_non_dsk():
    """Test error when trying to write to non-dsk type."""
    code = """
def main() {
    str notfile = "not a file"
    str text = "hello"
    text ->> notfile
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
        assert "require dsk type on right side" in result.stderr or "require dsk type on right side" in result.stdout
        assert result.returncode != 0
    finally:
        os.unlink(temp_file)


def test_error_read_from_non_dsk():
    """Test error when trying to read from non-dsk type."""
    code = """
def main() {
    str notfile = "not a file"
    str text
    text <- notfile
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
        assert "requires dsk type on right side" in result.stderr or "requires dsk type on right side" in result.stdout
        assert result.returncode != 0
    finally:
        os.unlink(temp_file)


def test_multiple_operations():
    """Test multiple file operations in sequence."""
    code = """
def main() {
    dsk myfile = disk("test_multi.txt")
    
    str line1 = "First line"
    line1 -> myfile
    
    str line2 = "Second line"
    line2 ->> myfile
    
    str line3 = "Third line"
    line3 ->> myfile
    
    myfile.close()
    
    str content
    dsk readfile = disk("test_multi.txt")
    content <- readfile
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
        assert "First line" in result.stdout
        assert "Second line" in result.stdout
        assert "Third line" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_map_to_file():
    """Test map ->> dsk (append map to file)."""
    code = """
def main() {
    dsk myfile = disk("test_map.txt")
    map data = {"name": "Alice", "age": 30}
    data ->> myfile
    myfile.close()
    
    dsk readfile = disk("test_map.txt")
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
        assert "name" in result.stdout
        assert "Alice" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_god_to_file():
    """Test god (boolean) ->> dsk (append boolean to file)."""
    code = """
def main() {
    dsk myfile = disk("test_god.txt")
    god flag = True
    flag ->> myfile
    myfile.close()
    
    dsk readfile = disk("test_god.txt")
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
        assert "True" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)
