# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for getopts() built-in function (Sprint 9 Task 5)."""

import pytest
import subprocess
import sys
import tempfile
import os


def test_getopts_short_flag():
    """Test getopts() with a short flag (-a)."""
    code = """
def main() {
    god a = getopts("a", None)
    if a
        print("Option -a was provided")
    else
        print("Option -a was not provided")
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-a'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Option -a was provided" in result.stdout

        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Option -a was not provided" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_long_flag():
    """Test getopts() with a long flag (--verbose)."""
    code = """
def main() {
    god verbose = getopts(None, "verbose")
    if verbose
        print("Verbose mode enabled")
    else
        print("Verbose mode disabled")
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '--verbose'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Verbose mode enabled" in result.stdout

        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Verbose mode disabled" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_option_with_value():
    """Test getopts() with an option that has a value (--file=myfile)."""
    code = """
def main() {
    var filename = getopts(None, "file")
    if filename != False
        print("File:", filename)
    else
        print("No file specified")
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '--file=myfile.txt'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "File: myfile.txt" in result.stdout

        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "No file specified" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_multiple_options():
    """Test getopts() with multiple options."""
    code = """
def main() {
    god a = getopts("a", None)
    god verbose = getopts(None, "verbose")
    var filename = getopts(None, "file")

    print("a:", a)
    print("verbose:", verbose)
    print("file:", filename)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-a', '--verbose', '--file=test.txt'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "a: True" in result.stdout
        assert "verbose: True" in result.stdout
        assert "file: test.txt" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_missing_option_returns_false():
    """Test that getopts() returns False for options that weren't provided."""
    code = """
def main() {
    god x = getopts("x", None)
    god y = getopts("y", None)
    god z = getopts("z", None)

    print("x:", x)
    print("y:", y)
    print("z:", z)
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
        assert "x: False" in result.stdout
        assert "y: False" in result.stdout
        assert "z: False" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_example_from_spec():
    """Test the example from the Sprint 9 Plan specification."""
    code = """
def main() {
    god a = getopts("a", None)
    god v = getopts(None, "verbose")
    var filename = getopts(None, "file")
    god x = getopts("x", None)

    print("a:", a)
    print("verbose:", v)
    print("file:", filename)
    print("x:", x)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-a', '--verbose', '--file=myfile'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "a: True" in result.stdout
        assert "verbose: True" in result.stdout
        assert "file: myfile" in result.stdout
        assert "x: False" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_with_run_command():
    """Test getopts() works with 'lyric run' command."""
    code = """
def main() {
    god debug = getopts(None, "debug")
    print("Debug mode:", debug)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', 'run', temp_file, '--debug'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Debug mode: True" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_long_option_requires_two_dashes():
    """Test that short and long options are distinct."""
    code = """
def main() {
    god v = getopts("v", None)
    god verbose = getopts(None, "verbose")

    print("v:", v)
    print("verbose:", verbose)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-v'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "v: True" in result.stdout
        assert "verbose: False" in result.stdout

        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '--verbose'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "v: False" in result.stdout
        assert "verbose: True" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_mixed_options_and_values():
    """Test getopts() with a mix of flags and options with values."""
    code = """
def main() {
    god a = getopts("a", None)
    god b = getopts("b", None)
    var input = getopts(None, "input")
    var output = getopts(None, "output")
    god verbose = getopts(None, "verbose")

    print("Flags: a=", a, "b=", b, "verbose=", verbose)
    print("Files: input=", input, "output=", output)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-a', '--input=in.txt', '-b', '--output=out.txt', '--verbose'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Flags: a= True b= True verbose= True" in result.stdout
        assert "Files: input= in.txt output= out.txt" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_empty_value():
    """Test getopts() with an option that has an empty value."""
    code = """
def main() {
    var value = getopts(None, "value")
    print("value:", value)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '--value='],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "value:" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_short_long_alias_short_flag():
    """Test getopts("h", "help") matches -h."""
    code = """
def main() {
    god help = getopts("h", "help")
    if help
        print("help requested")
    else
        print("no help")
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
        assert "help requested" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_short_long_alias_long_flag():
    """Test getopts("h", "help") matches --help."""
    code = """
def main() {
    god help = getopts("h", "help")
    if help
        print("help requested")
    else
        print("no help")
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '--help'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "help requested" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_short_long_alias_neither():
    """Test getopts("h", "help") returns false when neither passed."""
    code = """
def main() {
    god help = getopts("h", "help")
    if help
        print("help requested")
    else
        print("no help")
    end
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
        assert "no help" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_multichar_short_option():
    """Test getopts("hc", "high-capacity") matches -hc."""
    code = """
def main() {
    god hc = getopts("hc", "high-capacity")
    if hc
        print("high capacity mode")
    else
        print("normal mode")
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-hc'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "high capacity mode" in result.stdout

        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '--high-capacity'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "high capacity mode" in result.stdout

        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "normal mode" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_short_long_alias_with_value():
    """Test getopts("o", "output") returns value from either form."""
    code = """
def main() {
    var out = getopts("o", "output")
    print("output:", out)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-o=result.txt'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "output: result.txt" in result.stdout

        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '--output=result.txt'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "output: result.txt" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_none_short_option():
    """Test getopts(None, "verbose") — long-only option."""
    code = """
def main() {
    god v = getopts(None, "verbose")
    print("verbose:", v)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '--verbose'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "verbose: True" in result.stdout
    finally:
        os.unlink(temp_file)


def test_getopts_none_long_option():
    """Test getopts("v", None) — short-only option."""
    code = """
def main() {
    god v = getopts("v", None)
    print("v:", v)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file, '-v'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "v: True" in result.stdout
    finally:
        os.unlink(temp_file)
