# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for auto-generated help with -h option (Sprint 9 Task 8)."""

import pytest
import subprocess
import sys
import tempfile
import os


def test_auto_help_no_override():
    """Test that -h shows auto-generated help when not overridden."""
    code = """
def main() {
    var a = getopts("a", None)
    var verbose = getopts(None, "verbose")
    print("Running program")
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-h'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Usage:" in result.stdout
        assert "Auto-generated help" in result.stdout
        assert "-a" in result.stdout
        assert "--verbose" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_auto_help_with_override():
    """Test that -h is handled by program when getopts('h', ...) is used."""
    code = """
def main() {
    var help = getopts("h", None)
    if help
        print("Custom help message")
    else
        print("Running program")
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-h'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Custom help message" in result.stdout
        assert "Auto-generated help" not in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_auto_help_no_options():
    """Test auto-help when program has no getopts calls."""
    code = """
def main() {
    print("Hello, World!")
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-h'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Usage:" in result.stdout
        assert "No options defined" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_auto_help_with_argc_argv():
    """Test auto-help recognizes main(argc, argv) signature."""
    code = """
def main(int argc, arr argv) {
    var verbose = getopts(None, "verbose")
    print("Args:", argc)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-h'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Usage:" in result.stdout
        assert "This program accepts command-line arguments" in result.stdout
        assert "--verbose" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_no_help_when_h_not_passed():
    """Test that program runs normally without -h."""
    code = """
def main() {
    var a = getopts("a", None)
    print("Program executed")
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
        assert "Program executed" in result.stdout
        assert "Usage:" not in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_auto_help_with_multiple_options():
    """Test auto-help lists all available options."""
    code = """
def main() {
    var debug = getopts(None, "debug")
    var verbose = getopts(None, "verbose")
    var file = getopts(None, "file")
    var a = getopts("a", None)
    var b = getopts("b", None)
    print("Running")
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-h'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Usage:" in result.stdout
        assert "-a" in result.stdout
        assert "-b" in result.stdout
        assert "--debug" in result.stdout
        assert "--verbose" in result.stdout
        assert "--file" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_override_with_double_quotes():
    """Test that getopts("h", ...) with double quotes is recognized."""
    code = """
def main() {
    var host = getopts("h", None)
    if host
        print("Host:", host)
    else
        print("No host specified")
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-h'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        # Should execute program, not show auto-help
        assert "No host specified" in result.stdout or "Host:" in result.stdout
        assert "Auto-generated help" not in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_override_with_single_quotes():
    """Test that getopts('h', ...) with single quotes is recognized."""
    code = """
def main() {
    var host = getopts('h', None)
    print("Host:", host)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-h'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        # Should execute program, not show auto-help
        assert "Host:" in result.stdout
        assert "Auto-generated help" not in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_auto_help_sorted_options():
    """Test that options are sorted alphabetically in auto-help."""
    code = """
def main() {
    var z = getopts("z", None)
    var a = getopts("a", None)
    var m = getopts("m", None)
    print("Running")
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-h'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        # Find positions of options in output
        a_pos = result.stdout.find("-a")
        m_pos = result.stdout.find("-m")
        z_pos = result.stdout.find("-z")
        
        # Should be in alphabetical order
        assert a_pos < m_pos < z_pos
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_auto_help_duplicate_options():
    """Test that duplicate getopts calls only list option once."""
    code = """
def main() {
    var v1 = getopts(None, "verbose")
    var v2 = getopts(None, "verbose")
    print("Running")
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-h'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        # Count occurrences of --verbose
        count = result.stdout.count("--verbose")
        assert count == 1  # Should only appear once
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)

