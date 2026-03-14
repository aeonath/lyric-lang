# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for stderr-to-stdout merging in exec() operators and pipelines (Sprint 10 Task 2)."""

import pytest
import subprocess
import sys
import os
import tempfile

# Three dirs up from this file: core-0.9.0 -> tests -> lyric (project root for CLI)
_CWD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_lyric(source: str) -> subprocess.CompletedProcess:
    """Write Lyric source to a temp file and run it via the CLI."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(source)
        ly_file = f.name
    try:
        return subprocess.run(
            ['lyric', ly_file],
            capture_output=True, text=True, cwd=_CWD
        )
    finally:
        os.unlink(ly_file)


@pytest.fixture
def py_script():
    """Yields a factory for temporary Python scripts that write to stdout/stderr.

    Usage:
        path = py_script(stdout='hello\\n', stderr='error\\n')
    Returns a forward-slash path usable in Lyric exec() calls.
    """
    created = []

    def factory(stdout='', stderr='', exitcode=0):
        lines = ['import sys\n']
        if stdout:
            lines.append(f'sys.stdout.write({repr(stdout)})\n')
        if stderr:
            lines.append(f'sys.stderr.write({repr(stderr)})\n')
        if exitcode:
            lines.append(f'sys.exit({exitcode})\n')
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.writelines(lines)
            path = f.name
        created.append(path)
        return path.replace('\\', '/')

    yield factory

    for path in created:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass


# ---------------------------------------------------------------------------
# exec("cmd") -> var  captures stderr
# ---------------------------------------------------------------------------

def test_exec_redirect_captures_stderr_only(py_script):
    """exec() -> var must capture stderr when the command writes only to stderr."""
    py = py_script(stderr='only_stderr\n')
    result = _run_lyric(f"""
def main() {{
    str out
    exec("python3 {py}") -> out
    print(out)
}}
""")
    assert result.returncode == 0
    assert 'only_stderr' in result.stdout


def test_exec_redirect_captures_stdout_and_stderr(py_script):
    """exec() -> var must capture both stdout and stderr together."""
    py = py_script(stdout='got_stdout\n', stderr='got_stderr\n')
    result = _run_lyric(f"""
def main() {{
    str out
    exec("python3 {py}") -> out
    print(out)
}}
""")
    assert result.returncode == 0
    assert 'got_stdout' in result.stdout
    assert 'got_stderr' in result.stdout


def test_exec_redirect_captures_stderr_from_failing_command(py_script):
    """exec() -> var must capture stderr even when the command exits non-zero."""
    py = py_script(stderr='failure_msg\n', exitcode=1)
    result = _run_lyric(f"""
def main() {{
    str out
    exec("python3 {py}") -> out
    print(out)
}}
""")
    assert result.returncode == 0      # Lyric program itself succeeds
    assert 'failure_msg' in result.stdout


def test_exec_redirect_stderr_multiline(py_script):
    """exec() -> var captures multi-line stderr output."""
    py = py_script(stderr='err_line1\nerr_line2\nerr_line3\n')
    result = _run_lyric(f"""
def main() {{
    str out
    exec("python3 {py}") -> out
    print(out)
}}
""")
    assert result.returncode == 0
    assert 'err_line1' in result.stdout
    assert 'err_line2' in result.stdout
    assert 'err_line3' in result.stdout


# ---------------------------------------------------------------------------
# exec() | exec()  pipeline includes stderr
# ---------------------------------------------------------------------------

def test_pipeline_stderr_from_first_command_is_piped(py_script):
    """In exec() | exec(), stderr from the first command must be piped onward."""
    py = py_script(stderr='piped_err\n')
    result = _run_lyric(f"""
def main() {{
    str out
    exec("python3 {py}") | exec("cat") -> out
    print(out)
}}
""")
    assert result.returncode == 0
    assert 'piped_err' in result.stdout


def test_pipeline_stdout_and_stderr_from_first_command_are_piped(py_script):
    """In exec() | exec(), both stdout and stderr from the first command are piped."""
    py = py_script(stdout='pipe_stdout\n', stderr='pipe_stderr\n')
    result = _run_lyric(f"""
def main() {{
    str out
    exec("python3 {py}") | exec("cat") -> out
    print(out)
}}
""")
    assert result.returncode == 0
    assert 'pipe_stdout' in result.stdout
    assert 'pipe_stderr' in result.stdout


def test_pipeline_stderr_from_last_command_captured(py_script):
    """In exec() | exec() -> var, stderr from the last command is also captured."""
    py_first = py_script(stdout='data\n')
    py_last = py_script(stderr='last_err\n')
    result = _run_lyric(f"""
def main() {{
    str out
    exec("python3 {py_first}") | exec("python3 {py_last}") -> out
    print(out)
}}
""")
    assert result.returncode == 0
    assert 'last_err' in result.stdout


def test_pipeline_stderr_propagates_through_cat_stages(py_script):
    """Stderr from the first stage propagates through multiple cat stages."""
    py1 = py_script(stderr='stage1_err\n')
    result = _run_lyric(f"""
def main() {{
    str out
    exec("python3 {py1}") | exec("cat") | exec("cat") -> out
    print(out)
}}
""")
    assert result.returncode == 0
    assert 'stage1_err' in result.stdout


# ---------------------------------------------------------------------------
# exec() ->> file  captures stderr
# ---------------------------------------------------------------------------

def test_append_to_file_captures_stderr(py_script, tmp_path):
    """exec() ->> file must include stderr in the appended file content."""
    py = py_script(stderr='file_stderr\n')
    out_file = str(tmp_path / 'out.txt').replace('\\', '/')
    result = _run_lyric(f"""
def main() {{
    dsk f = disk("{out_file}")
    exec("python3 {py}") ->> f
    f.close()
    dsk r = disk("{out_file}")
    str content = r.read()
    print(content)
    r.close()
}}
""")
    assert result.returncode == 0
    assert 'file_stderr' in result.stdout


def test_append_to_file_captures_stdout_and_stderr(py_script, tmp_path):
    """exec() ->> file must include both stdout and stderr in the appended content."""
    py = py_script(stdout='file_out\n', stderr='file_err\n')
    out_file = str(tmp_path / 'out.txt').replace('\\', '/')
    result = _run_lyric(f"""
def main() {{
    dsk f = disk("{out_file}")
    exec("python3 {py}") ->> f
    f.close()
    dsk r = disk("{out_file}")
    str content = r.read()
    print(content)
    r.close()
}}
""")
    assert result.returncode == 0
    assert 'file_out' in result.stdout
    assert 'file_err' in result.stdout
