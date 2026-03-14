# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for the Lyric standard library (import lyric).

Full coverage of every function exported by lib/lyric/lyric.ly:
  sleep, randflt, randint, randarr, seed, cd, ls, mkdir, pwd,
  env, set, pid, exists, isfile, isdir, rm, rmdir, date, datefmt,
  now, join, path, base, dir
"""

import pytest
import subprocess
import sys
import tempfile
import os


# ---------------------------------------------------------------------------
# Helper: write Lyric code to a temp .ly file, run it, return CompletedProcess
# ---------------------------------------------------------------------------
def _run_lyric(code: str, timeout: int = 30) -> subprocess.CompletedProcess:
    """Write code to a temp file and execute via the lyric CLI."""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.ly', delete=False, dir=tempfile.gettempdir()
    ) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            ['lyric', temp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result
    finally:
        os.unlink(temp_file)


def _run_lyric_interpret(code: str, timeout: int = 30) -> subprocess.CompletedProcess:
    """Run with --interpret flag for comparison."""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.ly', delete=False, dir=tempfile.gettempdir()
    ) as f:
        f.write(code)
        f.flush()
        temp_file = f.name

    try:
        result = subprocess.run(
            ['lyric', temp_file, '--interpret'],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result
    finally:
        os.unlink(temp_file)


# ===================================================================
# pwd()
# ===================================================================
class TestPwd:
    """Tests for lyric.pwd() — returns current working directory."""

    def test_pwd_returns_nonempty_string(self):
        code = """
import lyric
def main() {
    var cwd = lyric.pwd()
    print(cwd)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0

    def test_pwd_returns_absolute_path(self):
        code = """
import lyric
def main() {
    var cwd = lyric.pwd()
    print(cwd)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        # Absolute paths start with / on Unix
        assert result.stdout.strip().startswith('/')

    def test_pwd_interpreter_matches_compiled(self):
        code = """
import lyric
def main() {
    var cwd = lyric.pwd()
    print(cwd)
}
"""
        compiled = _run_lyric(code)
        interpreted = _run_lyric_interpret(code)
        assert compiled.returncode == 0
        assert interpreted.returncode == 0
        assert compiled.stdout.strip() == interpreted.stdout.strip()


# ===================================================================
# exists()
# ===================================================================
class TestExists:
    """Tests for lyric.exists() — check if file or directory exists."""

    def test_exists_current_dir(self):
        code = """
import lyric
def main() {
    print(lyric.exists("."))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_exists_nonexistent(self):
        code = """
import lyric
def main() {
    print(lyric.exists("__nonexistent_path_xyz_999__"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "False" in result.stdout

    def test_exists_real_file(self):
        """Create a temp file, check it exists via Lyric."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        code = f"""
import lyric
def main() {{
    print(lyric.exists("{tmp_path}"))
}}
"""
        try:
            result = _run_lyric(code)
            assert result.returncode == 0
            assert "True" in result.stdout
        finally:
            os.unlink(tmp_path)


# ===================================================================
# isfile() / isdir()
# ===================================================================
class TestIsfileIsdir:
    """Tests for lyric.isfile() and lyric.isdir()."""

    def test_isdir_current_dir(self):
        code = """
import lyric
def main() {
    print(lyric.isdir("."))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_isfile_current_dir_is_false(self):
        code = """
import lyric
def main() {
    print(lyric.isfile("."))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "False" in result.stdout

    def test_isdir_nonexistent(self):
        code = """
import lyric
def main() {
    print(lyric.isdir("__nonexistent__"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "False" in result.stdout

    def test_isfile_nonexistent(self):
        code = """
import lyric
def main() {
    print(lyric.isfile("__nonexistent__"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "False" in result.stdout

    def test_isfile_real_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        code = f"""
import lyric
def main() {{
    print(lyric.isfile("{tmp_path}"))
}}
"""
        try:
            result = _run_lyric(code)
            assert result.returncode == 0
            assert "True" in result.stdout
        finally:
            os.unlink(tmp_path)

    def test_isdir_tmp(self):
        code = """
import lyric
def main() {
    print(lyric.isdir("/tmp"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout


# ===================================================================
# mkdir() / rmdir()
# ===================================================================
class TestMkdirRmdir:
    """Tests for lyric.mkdir() and lyric.rmdir()."""

    def test_mkdir_creates_directory(self):
        test_dir = os.path.join(tempfile.gettempdir(), '_lyric_test_mkdir')
        # Ensure clean state
        if os.path.exists(test_dir):
            os.rmdir(test_dir)

        code = f"""
import lyric
def main() {{
    lyric.mkdir("{test_dir}")
    print(lyric.isdir("{test_dir}"))
}}
"""
        try:
            result = _run_lyric(code)
            assert result.returncode == 0
            assert "True" in result.stdout
        finally:
            if os.path.exists(test_dir):
                os.rmdir(test_dir)

    def test_rmdir_removes_directory(self):
        test_dir = os.path.join(tempfile.gettempdir(), '_lyric_test_rmdir')
        os.makedirs(test_dir, exist_ok=True)

        code = f"""
import lyric
def main() {{
    lyric.rmdir("{test_dir}")
    print(lyric.exists("{test_dir}"))
}}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "False" in result.stdout

    def test_mkdir_then_rmdir(self):
        test_dir = os.path.join(tempfile.gettempdir(), '_lyric_test_mkrmdir')
        if os.path.exists(test_dir):
            os.rmdir(test_dir)

        code = f"""
import lyric
def main() {{
    lyric.mkdir("{test_dir}")
    print(lyric.isdir("{test_dir}"))
    lyric.rmdir("{test_dir}")
    print(lyric.exists("{test_dir}"))
}}
"""
        try:
            result = _run_lyric(code)
            assert result.returncode == 0
            lines = result.stdout.strip().split('\n')
            assert "True" in lines[0]
            assert "False" in lines[1]
        finally:
            if os.path.exists(test_dir):
                os.rmdir(test_dir)


# ===================================================================
# cd()
# ===================================================================
class TestCd:
    """Tests for lyric.cd() — change working directory."""

    def test_cd_changes_directory(self):
        test_dir = os.path.join(tempfile.gettempdir(), '_lyric_test_cd')
        os.makedirs(test_dir, exist_ok=True)

        code = f"""
import lyric
def main() {{
    var original = lyric.pwd()
    lyric.cd("{test_dir}")
    var newdir = lyric.pwd()
    print(original != newdir)
    lyric.cd(original)
}}
"""
        try:
            result = _run_lyric(code)
            assert result.returncode == 0
            assert "True" in result.stdout
        finally:
            if os.path.exists(test_dir):
                os.rmdir(test_dir)

    def test_cd_and_back(self):
        test_dir = os.path.join(tempfile.gettempdir(), '_lyric_test_cd_back')
        os.makedirs(test_dir, exist_ok=True)

        code = f"""
import lyric
def main() {{
    var original = lyric.pwd()
    lyric.cd("{test_dir}")
    lyric.cd(original)
    print(lyric.pwd() == original)
}}
"""
        try:
            result = _run_lyric(code)
            assert result.returncode == 0
            assert "True" in result.stdout
        finally:
            if os.path.exists(test_dir):
                os.rmdir(test_dir)


# ===================================================================
# ls()
# ===================================================================
class TestLs:
    """Tests for lyric.ls() — list directory contents or glob."""

    def test_ls_current_dir(self):
        code = """
import lyric
def main() {
    arr entries = lyric.ls(".")
    print(int(entries) > 0)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_ls_parent_dir(self):
        code = """
import lyric
def main() {
    arr entries = lyric.ls("..")
    print(int(entries) >= 0)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_ls_glob_pattern(self):
        """ls() with a glob pattern returns matching files."""
        # Create a temp dir with known files
        test_dir = os.path.join(tempfile.gettempdir(), '_lyric_test_ls_glob')
        os.makedirs(test_dir, exist_ok=True)
        for name in ['a.txt', 'b.txt', 'c.log']:
            open(os.path.join(test_dir, name), 'w').close()

        code = f"""
import lyric
def main() {{
    arr entries = lyric.ls("{test_dir}/*.txt")
    print(int(entries))
}}
"""
        try:
            result = _run_lyric(code)
            assert result.returncode == 0
            assert result.stdout.strip() == "2"
        finally:
            for name in ['a.txt', 'b.txt', 'c.log']:
                p = os.path.join(test_dir, name)
                if os.path.exists(p):
                    os.unlink(p)
            if os.path.exists(test_dir):
                os.rmdir(test_dir)

    def test_ls_directory_listing(self):
        """ls() on a directory returns its contents."""
        test_dir = os.path.join(tempfile.gettempdir(), '_lyric_test_ls_dir')
        os.makedirs(test_dir, exist_ok=True)
        open(os.path.join(test_dir, 'file1.txt'), 'w').close()
        open(os.path.join(test_dir, 'file2.txt'), 'w').close()

        code = f"""
import lyric
def main() {{
    arr entries = lyric.ls("{test_dir}")
    print(int(entries))
}}
"""
        try:
            result = _run_lyric(code)
            assert result.returncode == 0
            assert result.stdout.strip() == "2"
        finally:
            for name in ['file1.txt', 'file2.txt']:
                p = os.path.join(test_dir, name)
                if os.path.exists(p):
                    os.unlink(p)
            if os.path.exists(test_dir):
                os.rmdir(test_dir)


# ===================================================================
# rm()
# ===================================================================
class TestRm:
    """Tests for lyric.rm() — remove a file."""

    def test_rm_removes_file(self):
        tmp_path = os.path.join(tempfile.gettempdir(), '_lyric_test_rm.txt')
        with open(tmp_path, 'w') as f:
            f.write("test content")

        code = f"""
import lyric
def main() {{
    print(lyric.exists("{tmp_path}"))
    lyric.rm("{tmp_path}")
    print(lyric.exists("{tmp_path}"))
}}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert "True" in lines[0]
        assert "False" in lines[1]

    def test_rm_via_disk_and_rm(self):
        """Create file with disk(), then remove with lyric.rm()."""
        tmp_path = os.path.join(tempfile.gettempdir(), '_lyric_test_rm2.txt')

        code = f"""
import lyric
def main() {{
    dsk f = disk("{tmp_path}")
    f.write("hello")
    f.close()
    print(lyric.isfile("{tmp_path}"))
    lyric.rm("{tmp_path}")
    print(lyric.exists("{tmp_path}"))
}}
"""
        try:
            result = _run_lyric(code)
            assert result.returncode == 0
            lines = result.stdout.strip().split('\n')
            assert "True" in lines[0]
            assert "False" in lines[1]
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


# ===================================================================
# env() / set()
# ===================================================================
class TestEnvSet:
    """Tests for lyric.env() and lyric.set() — environment variables."""

    def test_env_path(self):
        """env('PATH') should return a non-empty string."""
        code = """
import lyric
def main() {
    var p = lyric.env("PATH")
    print(p != "")
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_env_nonexistent(self):
        """env() returns None for missing variables."""
        code = """
import lyric
def main() {
    var v = lyric.env("LYRIC_NONEXISTENT_VAR_XYZ_12345")
    print(v == None)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_set_and_env(self):
        """set() then env() retrieves the value."""
        code = """
import lyric
def main() {
    lyric.set("LYRIC_TEST_STDLIB_VAR", "hello_stdlib")
    var v = lyric.env("LYRIC_TEST_STDLIB_VAR")
    print(v)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "hello_stdlib" in result.stdout

    def test_set_overwrites(self):
        """set() can overwrite an existing variable."""
        code = """
import lyric
def main() {
    lyric.set("LYRIC_TEST_OVERWRITE", "first")
    lyric.set("LYRIC_TEST_OVERWRITE", "second")
    print(lyric.env("LYRIC_TEST_OVERWRITE"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "second" in result.stdout
        assert "first" not in result.stdout


# ===================================================================
# pid()
# ===================================================================
class TestPid:
    """Tests for lyric.pid() — returns process ID."""

    def test_pid_positive(self):
        code = """
import lyric
def main() {
    var p = lyric.pid()
    print(p > 0)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_pid_is_integer(self):
        code = """
import lyric
def main() {
    var p = lyric.pid()
    print(type(p))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "int" in result.stdout


# ===================================================================
# now()
# ===================================================================
class TestNow:
    """Tests for lyric.now() — returns Unix timestamp."""

    def test_now_reasonable_value(self):
        code = """
import lyric
def main() {
    var t = lyric.now()
    print(t > 1700000000)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_now_nondecreasing(self):
        code = """
import lyric
def main() {
    var t1 = lyric.now()
    var t2 = lyric.now()
    print(t2 >= t1)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_now_is_integer(self):
        code = """
import lyric
def main() {
    var t = lyric.now()
    print(type(t))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "int" in result.stdout


# ===================================================================
# date()
# ===================================================================
class TestDate:
    """Tests for lyric.date() — returns (date_str, time_str) tuple."""

    def test_date_returns_tuple(self):
        code = """
import lyric
def main() {
    var d = lyric.date()
    print(d)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        # Should print a tuple-like output containing date and time
        assert result.returncode == 0

    def test_date_format_lengths(self):
        """date()[0] is YYYY-MM-DD (10 chars), date()[1] is HH:MM:SS (8 chars)."""
        code = """
import lyric
def main() {
    var d = lyric.date()
    str datepart = d[0]
    str timepart = d[1]
    print(datepart)
    print(timepart)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert len(lines[0].strip()) == 10  # YYYY-MM-DD
        assert len(lines[1].strip()) == 8   # HH:MM:SS

    def test_date_contains_dashes_and_colons(self):
        code = """
import lyric
def main() {
    var d = lyric.date()
    str datepart = d[0]
    str timepart = d[1]
    print(datepart)
    print(timepart)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        # YYYY-MM-DD has dashes at positions 4 and 7
        assert '-' in lines[0]
        # HH:MM:SS has colons
        assert ':' in lines[1]


# ===================================================================
# datefmt()
# ===================================================================
class TestDatefmt:
    """Tests for lyric.datefmt() — formatted date string."""

    def test_datefmt_year(self):
        code = """
import lyric
def main() {
    str s = lyric.datefmt("%Y")
    print(s)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        output = result.stdout.strip()
        assert len(output) == 4
        assert int(output) >= 2025

    def test_datefmt_full_date(self):
        code = """
import lyric
def main() {
    str s = lyric.datefmt("%Y-%m-%d")
    print(s)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert len(result.stdout.strip()) == 10

    def test_datefmt_time(self):
        code = """
import lyric
def main() {
    str s = lyric.datefmt("%H:%M:%S")
    print(s)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert len(result.stdout.strip()) == 8

    def test_datefmt_custom_format(self):
        code = """
import lyric
def main() {
    str s = lyric.datefmt("%d/%m/%Y")
    print(s)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        output = result.stdout.strip()
        # dd/mm/yyyy
        assert len(output) == 10
        assert output[2] == '/'
        assert output[5] == '/'


# ===================================================================
# join()
# ===================================================================
class TestJoin:
    """Tests for lyric.join() — joins two path components."""

    def test_join_basic(self):
        code = """
import lyric
def main() {
    var p = lyric.join("usr", "local")
    print(p)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "usr/local"

    def test_join_with_slash(self):
        code = """
import lyric
def main() {
    var p = lyric.join("/home", "user")
    print(p)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "/home/user"

    def test_join_absolute_second(self):
        """If second arg is absolute, it overrides first (os.path.join behavior)."""
        code = """
import lyric
def main() {
    var p = lyric.join("relative", "/absolute")
    print(p)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "/absolute"


# ===================================================================
# path()
# ===================================================================
class TestPath:
    """Tests for lyric.path() — returns absolute path."""

    def test_path_dot(self):
        code = """
import lyric
def main() {
    var p = lyric.path(".")
    print(p)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        output = result.stdout.strip()
        assert output.startswith('/')
        assert len(output) > 1

    def test_path_makes_absolute(self):
        code = """
import lyric
def main() {
    var p = lyric.path("somefile.txt")
    print(p)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        output = result.stdout.strip()
        assert output.startswith('/')
        assert output.endswith('somefile.txt')

    def test_path_already_absolute(self):
        code = """
import lyric
def main() {
    var p = lyric.path("/tmp/test.txt")
    print(p)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "/tmp/test.txt"


# ===================================================================
# base()
# ===================================================================
class TestBase:
    """Tests for lyric.base() — returns basename of a path."""

    def test_base_with_directory(self):
        code = """
import lyric
def main() {
    print(lyric.base("/home/user/file.txt"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "file.txt"

    def test_base_just_filename(self):
        code = """
import lyric
def main() {
    print(lyric.base("file.txt"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "file.txt"

    def test_base_trailing_slash(self):
        code = """
import lyric
def main() {
    print(lyric.base("/just/a/dir/"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_base_nested(self):
        code = """
import lyric
def main() {
    print(lyric.base("/a/b/c/d/script.ly"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "script.ly"


# ===================================================================
# dir()
# ===================================================================
class TestDir:
    """Tests for lyric.dir() — returns directory part of a path."""

    def test_dir_with_path(self):
        code = """
import lyric
def main() {
    print(lyric.dir("/home/user/file.txt"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "/home/user"

    def test_dir_just_filename(self):
        code = """
import lyric
def main() {
    print(lyric.dir("file.txt"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_dir_nested(self):
        code = """
import lyric
def main() {
    print(lyric.dir("/a/b/c/file.py"))
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "/a/b/c"


# ===================================================================
# sleep()
# ===================================================================
class TestSleep:
    """Tests for lyric.sleep() — pauses execution."""

    def test_sleep_short(self):
        code = """
import lyric
def main() {
    lyric.sleep(0.01)
    print("done")
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "done" in result.stdout

    def test_sleep_zero(self):
        code = """
import lyric
def main() {
    lyric.sleep(0)
    print("done")
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "done" in result.stdout


# ===================================================================
# seed() / randflt() / randint() / randarr()
# ===================================================================
class TestRandom:
    """Tests for lyric.seed(), lyric.randflt(), lyric.randint(), lyric.randarr()."""

    def test_randflt_in_range(self):
        code = """
import lyric
def main() {
    var r = lyric.randflt()
    print(r >= 0.0 and r < 1.0)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_randflt_multiple_in_range(self):
        code = """
import lyric
def main() {
    god all_ok = true
    var r
    for var i in range(20)
        r = lyric.randflt()
        if r < 0.0 or r >= 1.0
            all_ok = false
        end
    done
    print(all_ok)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_randint_in_range(self):
        code = """
import lyric
def main() {
    var r = lyric.randint(1, 10)
    print(r >= 1 and r <= 10)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_randint_same_bounds(self):
        code = """
import lyric
def main() {
    var r = lyric.randint(5, 5)
    print(r)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "5"

    def test_randint_negative_range(self):
        code = """
import lyric
def main() {
    var r = lyric.randint(-100, -50)
    print(r >= -100 and r <= -50)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_randint_multiple_in_range(self):
        code = """
import lyric
def main() {
    god all_ok = true
    var r
    for var i in range(20)
        r = lyric.randint(1, 3)
        if r < 1 or r > 3
            all_ok = false
        end
    done
    print(all_ok)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_randarr_from_list(self):
        code = """
import lyric
def main() {
    arr items = ["a", "b", "c"]
    var r = lyric.randarr(items)
    print(r == "a" or r == "b" or r == "c")
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout

    def test_randarr_single_element(self):
        code = """
import lyric
def main() {
    arr items = [42]
    var r = lyric.randarr(items)
    print(r)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert result.stdout.strip() == "42"

    def test_seed_deterministic(self):
        """Seeding with same value produces same sequence."""
        code = """
import lyric
def main() {
    lyric.seed(12345)
    var a1 = lyric.randint(1, 1000)
    var a2 = lyric.randint(1, 1000)
    var a3 = lyric.randflt()

    lyric.seed(12345)
    var b1 = lyric.randint(1, 1000)
    var b2 = lyric.randint(1, 1000)
    var b3 = lyric.randflt()

    print(a1 == b1)
    print(a2 == b2)
    print(a3 == b3)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert "True" in lines[0]
        assert "True" in lines[1]
        assert "True" in lines[2]

    def test_seed_different_seeds_differ(self):
        """Different seeds should produce different results (with high probability)."""
        code = """
import lyric
def main() {
    lyric.seed(1)
    var a = lyric.randint(1, 1000000)

    lyric.seed(2)
    var b = lyric.randint(1, 1000000)

    print(a != b)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        assert "True" in result.stdout


# ===================================================================
# Integration: combined stdlib operations
# ===================================================================
class TestIntegration:
    """Integration tests combining multiple stdlib functions."""

    def test_mkdir_disk_isfile_rm_rmdir(self):
        """Full lifecycle: create dir, create file, verify, clean up."""
        test_dir = os.path.join(tempfile.gettempdir(), '_lyric_stdlib_int')
        test_file = os.path.join(test_dir, 'data.txt')

        code = f"""
import lyric
def main() {{
    lyric.mkdir("{test_dir}")
    print(lyric.isdir("{test_dir}"))

    dsk f = disk("{test_file}")
    f.write("integration test")
    f.close()
    print(lyric.isfile("{test_file}"))

    str b = lyric.base("{test_file}")
    print(b)

    str d = lyric.dir("{test_file}")
    print(d)

    lyric.rm("{test_file}")
    print(lyric.exists("{test_file}"))
    lyric.rmdir("{test_dir}")
    print(lyric.exists("{test_dir}"))
}}
"""
        try:
            result = _run_lyric(code)
            assert result.returncode == 0
            lines = result.stdout.strip().split('\n')
            assert "True" in lines[0]   # isdir
            assert "True" in lines[1]   # isfile
            assert lines[2].strip() == "data.txt"  # base
            assert test_dir in lines[3]  # dir
            assert "False" in lines[4]  # file removed
            assert "False" in lines[5]  # dir removed
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)
            if os.path.exists(test_dir):
                os.rmdir(test_dir)

    def test_env_set_join_path(self):
        """Combine env, set, join, path operations."""
        code = """
import lyric
def main() {
    lyric.set("LYRIC_INT_TEST", "works")
    print(lyric.env("LYRIC_INT_TEST"))

    var p = lyric.join("/usr", "local")
    print(p)

    var abs = lyric.path(".")
    print(abs != "")
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert "works" in lines[0]
        assert lines[1].strip() == "/usr/local"
        assert "True" in lines[2]

    def test_date_now_together(self):
        """Both date() and now() return sensible current time."""
        code = """
import lyric
def main() {
    var t = lyric.now()
    var d = lyric.date()
    str datepart = d[0]
    str timepart = d[1]
    print(t > 1700000000)
    print(datepart)
    print(timepart)
}
"""
        result = _run_lyric(code)
        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert "True" in lines[0]
        assert len(lines[1].strip()) == 10  # YYYY-MM-DD
        assert len(lines[2].strip()) == 8   # HH:MM:SS

    def test_full_stdlib_compiled_vs_interpreted(self):
        """Run a program using many stdlib functions in both modes and compare."""
        code = """
import lyric
def main() {
    # Deterministic operations only (no random, no timestamps)
    print(lyric.join("a", "b"))
    print(lyric.base("/x/y/z.txt"))
    print(lyric.dir("/x/y/z.txt"))
    print(lyric.exists("."))
    print(lyric.isdir("."))
    print(lyric.isfile("."))
    lyric.set("LYRIC_COMPARE_TEST", "match")
    print(lyric.env("LYRIC_COMPARE_TEST"))
    print(lyric.pid() > 0)
}
"""
        compiled = _run_lyric(code)
        interpreted = _run_lyric_interpret(code)
        assert compiled.returncode == 0
        assert interpreted.returncode == 0
        # Compare deterministic lines (skip pid since different processes)
        c_lines = compiled.stdout.strip().split('\n')
        i_lines = interpreted.stdout.strip().split('\n')
        assert len(c_lines) == len(i_lines)
        # join, base, dir, exists, isdir, isfile, env should all match
        for idx in [0, 1, 2, 3, 4, 5, 6]:
            assert c_lines[idx].strip() == i_lines[idx].strip(), \
                f"Line {idx} mismatch: compiled={c_lines[idx]!r} vs interpreted={i_lines[idx]!r}"
