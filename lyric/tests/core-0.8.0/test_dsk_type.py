# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for dsk type and file I/O (Sprint 9 Task 7)."""

import pytest
import subprocess
import sys
import tempfile
import os


def test_dsk_variable_declaration():
    """Test declaring a dsk variable."""
    code = """
def main() {
    dsk myfile = disk("test.txt")
    print("File:", myfile)
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
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "File: test.txt" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_dsk_file_exists():
    """Test dsk.exists() method."""
    code = """
def main() {
    dsk myfile = disk("test_exists.txt")
    god exists = myfile.exists()
    print("File exists:", exists)
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
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "File exists: False" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_dsk_write_and_read():
    """Test writing and reading a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "testfile.txt")
        
        code = f"""
def main() {{
    dsk myfile = disk("{test_file.replace(chr(92), chr(92)*2)}")
    myfile.write("Hello, World!")
    myfile.close()
    
    dsk readfile = disk("{test_file.replace(chr(92), chr(92)*2)}")
    str content = readfile.read()
    readfile.close()
    
    print("Content:", content)
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "Content: Hello, World!" in result.stdout
            assert result.returncode == 0
            
            # Verify file was actually created
            assert os.path.exists(test_file)
        finally:
            os.unlink(temp_ly_file)


def test_dsk_readlines():
    """Test reading lines from a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "lines.txt")
        
        # Create test file with content
        with open(test_file, 'w') as f:
            f.write("Line 1\nLine 2\nLine 3\n")
        
        code = f"""
def main() {{
    dsk myfile = disk("{test_file.replace(chr(92), chr(92)*2)}")
    arr lines = myfile.readlines()
    myfile.close()
    
    print("Lines:", lines.len())
    var line
    for line in lines
        print("  ", line)
    done
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "Lines: 3" in result.stdout
            assert "Line 1" in result.stdout
            assert "Line 2" in result.stdout
            assert "Line 3" in result.stdout
            assert result.returncode == 0
        finally:
            os.unlink(temp_ly_file)


def test_dsk_append():
    """Test appending to a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "append.txt")
        
        code = f"""
def main() {{
    dsk myfile = disk("{test_file.replace(chr(92), chr(92)*2)}")
    myfile.write("First line\\n")
    myfile.close()
    
    myfile.append("Second line\\n")
    myfile.append("Third line\\n")
    
    arr lines = myfile.readlines()
    myfile.close()
    
    var line
    for line in lines
        print(line)
    done
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "First line" in result.stdout
            assert "Second line" in result.stdout
            assert "Third line" in result.stdout
            assert result.returncode == 0
        finally:
            os.unlink(temp_ly_file)


def test_dsk_delete():
    """Test deleting a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "delete_me.txt")
        
        # Create test file
        with open(test_file, 'w') as f:
            f.write("Temporary content")
        
        code = f"""
def main() {{
    dsk myfile = disk("{test_file.replace(chr(92), chr(92)*2)}")
    
    god before = myfile.exists()
    print("Exists before:", before)
    
    myfile.delete()
    
    god after = myfile.exists()
    print("Exists after:", after)
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "Exists before: True" in result.stdout
            assert "Exists after: False" in result.stdout
            assert result.returncode == 0
            
            # Verify file was deleted
            assert not os.path.exists(test_file)
        finally:
            os.unlink(temp_ly_file)


def test_dsk_copy():
    """Test copying a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        source_file = os.path.join(tmpdir, "source.txt")
        dest_file = os.path.join(tmpdir, "dest.txt")
        
        # Create source file
        with open(source_file, 'w') as f:
            f.write("Copy me!")
        
        code = f"""
def main() {{
    dsk source = disk("{source_file.replace(chr(92), chr(92)*2)}")
    source.copy("{dest_file.replace(chr(92), chr(92)*2)}")
    
    dsk dest = disk("{dest_file.replace(chr(92), chr(92)*2)}")
    str content = dest.read()
    dest.close()
    
    print("Copied content:", content)
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "Copied content: Copy me!" in result.stdout
            assert result.returncode == 0
            
            # Verify file was copied
            assert os.path.exists(dest_file)
        finally:
            os.unlink(temp_ly_file)


def test_dsk_move():
    """Test moving a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        source_file = os.path.join(tmpdir, "moveme.txt")
        dest_file = os.path.join(tmpdir, "moved.txt")
        
        # Create source file
        with open(source_file, 'w') as f:
            f.write("Move me!")
        
        code = f"""
def main() {{
    dsk myfile = disk("{source_file.replace(chr(92), chr(92)*2)}")
    
    god before = myfile.exists()
    print("Exists at source before:", before)
    
    myfile.move("{dest_file.replace(chr(92), chr(92)*2)}")
    
    dsk source = disk("{source_file.replace(chr(92), chr(92)*2)}")
    god after_source = source.exists()
    print("Exists at source after:", after_source)
    
    dsk dest = disk("{dest_file.replace(chr(92), chr(92)*2)}")
    god at_dest = dest.exists()
    print("Exists at dest:", at_dest)
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "Exists at source before: True" in result.stdout
            assert "Exists at source after: False" in result.stdout
            assert "Exists at dest: True" in result.stdout
            assert result.returncode == 0
            
            # Verify file was moved
            assert not os.path.exists(source_file)
            assert os.path.exists(dest_file)
        finally:
            os.unlink(temp_ly_file)


def test_dsk_size():
    """Test getting file size."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "sizeme.txt")
        
        # Create file with known content
        content = "12345"
        with open(test_file, 'w') as f:
            f.write(content)
        
        code = f"""
def main() {{
    dsk myfile = disk("{test_file.replace(chr(92), chr(92)*2)}")
    int filesize = myfile.size()
    print("File size:", filesize)
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "File size: 5" in result.stdout
            assert result.returncode == 0
        finally:
            os.unlink(temp_ly_file)


def test_dsk_open_modes():
    """Test opening file in different modes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "modes.txt")
        
        code = f"""
def main() {{
    # Write mode
    dsk wfile = disk("{test_file.replace(chr(92), chr(92)*2)}")
    wfile.open("w")
    wfile.write("Initial content")
    wfile.close()
    
    # Append mode
    dsk afile = disk("{test_file.replace(chr(92), chr(92)*2)}")
    afile.open("a")
    afile.write("\\nAppended content")
    afile.close()
    
    # Read mode
    dsk rfile = disk("{test_file.replace(chr(92), chr(92)*2)}")
    str content = rfile.read()
    rfile.close()
    
    print(content)
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "Initial content" in result.stdout
            assert "Appended content" in result.stdout
            assert result.returncode == 0
        finally:
            os.unlink(temp_ly_file)


def test_dsk_auto_open_for_read():
    """Test that dsk automatically opens file in read mode if not explicitly opened."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "auto.txt")
        
        # Create test file
        with open(test_file, 'w') as f:
            f.write("Auto-open test")
        
        code = f"""
def main() {{
    dsk myfile = disk("{test_file.replace(chr(92), chr(92)*2)}")
    str content = myfile.read()
    print("Content:", content)
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "Content: Auto-open test" in result.stdout
            assert result.returncode == 0
        finally:
            os.unlink(temp_ly_file)

