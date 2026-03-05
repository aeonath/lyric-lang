# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for importpy module blacklist (Sprint 10 Task 1)."""

import pytest
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import RuntimeErrorLyric
from lyric.pyproxy import BLACKLISTED_MODULES, BLACKLISTED_ATTRIBUTES


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(source: str):
    """Parse and evaluate a Lyric source string."""
    ast = parse(source)
    evaluate(ast)


def assert_blacklisted(module_name: str):
    """Assert that importpy raises the expected blacklist error for a module."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run(f"importpy {module_name}")
    msg = str(exc_info.value)
    assert f"'{module_name}' is blacklisted in Lyric" in msg
    assert "CPython bytecode, frames, object identity, or interpreter internals" in msg


# ---------------------------------------------------------------------------
# Blacklist membership
# ---------------------------------------------------------------------------

def test_blacklist_contains_pdb():
    assert 'pdb' in BLACKLISTED_MODULES

def test_blacklist_contains_inspect():
    assert 'inspect' in BLACKLISTED_MODULES

def test_blacklist_contains_dis():
    assert 'dis' in BLACKLISTED_MODULES

def test_blacklist_contains_gc():
    assert 'gc' in BLACKLISTED_MODULES

def test_sys_not_in_module_blacklist():
    """sys is allowed as a module; only specific attributes are blocked."""
    assert 'sys' not in BLACKLISTED_MODULES

def test_sys_settrace_in_attribute_blacklist():
    assert 'settrace' in BLACKLISTED_ATTRIBUTES.get('sys', frozenset())

def test_sys_setprofile_in_attribute_blacklist():
    assert 'setprofile' in BLACKLISTED_ATTRIBUTES.get('sys', frozenset())

def test_sys_gettrace_in_attribute_blacklist():
    assert 'gettrace' in BLACKLISTED_ATTRIBUTES.get('sys', frozenset())

def test_sys_getprofile_in_attribute_blacklist():
    assert 'getprofile' in BLACKLISTED_ATTRIBUTES.get('sys', frozenset())

def test_sys_getframe_in_attribute_blacklist():
    assert '_getframe' in BLACKLISTED_ATTRIBUTES.get('sys', frozenset())

def test_sys_current_frames_in_attribute_blacklist():
    assert '_current_frames' in BLACKLISTED_ATTRIBUTES.get('sys', frozenset())

def test_sys_getrefcount_in_attribute_blacklist():
    assert 'getrefcount' in BLACKLISTED_ATTRIBUTES.get('sys', frozenset())

def test_sys_addaudithook_in_attribute_blacklist():
    assert 'addaudithook' in BLACKLISTED_ATTRIBUTES.get('sys', frozenset())

def test_sys_exc_info_in_attribute_blacklist():
    assert 'exc_info' in BLACKLISTED_ATTRIBUTES.get('sys', frozenset())

def test_blacklist_contains_ctypes():
    assert 'ctypes' in BLACKLISTED_MODULES

def test_blacklist_contains_pickle():
    assert 'pickle' in BLACKLISTED_MODULES

def test_blacklist_contains_marshal():
    assert 'marshal' in BLACKLISTED_MODULES

def test_blacklist_contains_weakref():
    assert 'weakref' in BLACKLISTED_MODULES

def test_blacklist_contains_traceback():
    assert 'traceback' in BLACKLISTED_MODULES

def test_blacklist_contains_faulthandler():
    assert 'faulthandler' in BLACKLISTED_MODULES

def test_blacklist_contains_trace():
    assert 'trace' in BLACKLISTED_MODULES

def test_blacklist_contains_runpy():
    assert 'runpy' in BLACKLISTED_MODULES

def test_blacklist_contains_zipimport():
    assert 'zipimport' in BLACKLISTED_MODULES

def test_blacklist_contains_modulefinder():
    assert 'modulefinder' in BLACKLISTED_MODULES

def test_blacklist_contains_copyreg():
    assert 'copyreg' in BLACKLISTED_MODULES

def test_blacklist_contains_pickletools():
    assert 'pickletools' in BLACKLISTED_MODULES

def test_blacklist_contains_mmap():
    assert 'mmap' in BLACKLISTED_MODULES

def test_blacklist_contains_types():
    assert 'types' in BLACKLISTED_MODULES

def test_blacklist_contains_code():
    assert 'code' in BLACKLISTED_MODULES

def test_blacklist_contains_codeop():
    assert 'codeop' in BLACKLISTED_MODULES

def test_blacklist_contains_ctypes_private():
    assert '_ctypes' in BLACKLISTED_MODULES


# ---------------------------------------------------------------------------
# Runtime error raised for blacklisted modules
# ---------------------------------------------------------------------------

def test_importpy_pdb_raises_blacklist_error():
    assert_blacklisted('pdb')

def test_importpy_inspect_raises_blacklist_error():
    assert_blacklisted('inspect')

def test_importpy_dis_raises_blacklist_error():
    assert_blacklisted('dis')

def test_importpy_gc_raises_blacklist_error():
    assert_blacklisted('gc')

def test_importpy_sys_works():
    """sys itself must import successfully."""
    run("importpy sys")

def test_importpy_sys_settrace_raises_blacklist_error():
    """sys.settrace must raise a blacklist error."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy sys\nvar f = sys.settrace")
    msg = str(exc_info.value)
    assert "'sys.settrace' is blacklisted in Lyric" in msg
    assert "CPython bytecode, frames, object identity, or interpreter internals" in msg

def test_importpy_sys_setprofile_raises_blacklist_error():
    """sys.setprofile must raise a blacklist error."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy sys\nvar f = sys.setprofile")
    msg = str(exc_info.value)
    assert "'sys.setprofile' is blacklisted in Lyric" in msg
    assert "CPython bytecode, frames, object identity, or interpreter internals" in msg

def test_importpy_sys_gettrace_raises_blacklist_error():
    """sys.gettrace must raise a blacklist error."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy sys\nvar f = sys.gettrace")
    msg = str(exc_info.value)
    assert "'sys.gettrace' is blacklisted in Lyric" in msg

def test_importpy_sys_getprofile_raises_blacklist_error():
    """sys.getprofile must raise a blacklist error."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy sys\nvar f = sys.getprofile")
    msg = str(exc_info.value)
    assert "'sys.getprofile' is blacklisted in Lyric" in msg

def test_importpy_sys_getframe_raises_blacklist_error():
    """sys._getframe must raise a blacklist error."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy sys\nvar f = sys._getframe")
    msg = str(exc_info.value)
    assert "'sys._getframe' is blacklisted in Lyric" in msg

def test_importpy_sys_current_frames_raises_blacklist_error():
    """sys._current_frames must raise a blacklist error."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy sys\nvar f = sys._current_frames")
    msg = str(exc_info.value)
    assert "'sys._current_frames' is blacklisted in Lyric" in msg

def test_importpy_sys_getrefcount_raises_blacklist_error():
    """sys.getrefcount must raise a blacklist error."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy sys\nvar f = sys.getrefcount")
    msg = str(exc_info.value)
    assert "'sys.getrefcount' is blacklisted in Lyric" in msg

def test_importpy_sys_addaudithook_raises_blacklist_error():
    """sys.addaudithook must raise a blacklist error."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy sys\nvar f = sys.addaudithook")
    msg = str(exc_info.value)
    assert "'sys.addaudithook' is blacklisted in Lyric" in msg

def test_importpy_sys_exc_info_raises_blacklist_error():
    """sys.exc_info must raise a blacklist error."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy sys\nvar f = sys.exc_info")
    msg = str(exc_info.value)
    assert "'sys.exc_info' is blacklisted in Lyric" in msg

def test_importpy_ctypes_raises_blacklist_error():
    assert_blacklisted('ctypes')

def test_importpy_pickle_raises_blacklist_error():
    assert_blacklisted('pickle')

def test_importpy_marshal_raises_blacklist_error():
    assert_blacklisted('marshal')

def test_importpy_weakref_raises_blacklist_error():
    assert_blacklisted('weakref')

def test_importpy_traceback_raises_blacklist_error():
    assert_blacklisted('traceback')

def test_importpy_mmap_raises_blacklist_error():
    assert_blacklisted('mmap')

def test_importpy_runpy_raises_blacklist_error():
    assert_blacklisted('runpy')

def test_importpy_types_raises_blacklist_error():
    assert_blacklisted('types')


# ---------------------------------------------------------------------------
# Error message content
# ---------------------------------------------------------------------------

def test_blacklist_error_contains_module_name():
    """Error message must name the offending module."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy pickle")
    assert "pickle" in str(exc_info.value)

def test_blacklist_error_contains_reason():
    """Error message must explain why the module is blocked."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy gc")
    assert "CPython bytecode, frames, object identity, or interpreter internals" in str(exc_info.value)

def test_blacklist_error_says_blacklisted():
    """Error message must use the word 'blacklisted'."""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy dis")
    assert "blacklisted" in str(exc_info.value)


# ---------------------------------------------------------------------------
# sys attribute blacklist — allowed attributes still work
# ---------------------------------------------------------------------------

def test_importpy_sys_version_accessible():
    """sys.version must remain accessible (not blacklisted)."""
    run("importpy sys\nvar v = sys.version")

def test_importpy_sys_platform_accessible():
    """sys.platform must remain accessible (not blacklisted)."""
    run("importpy sys\nvar p = sys.platform")


# ---------------------------------------------------------------------------
# Non-blacklisted modules still work (regression)
# ---------------------------------------------------------------------------

def test_importpy_math_not_blacklisted():
    """math module must remain accessible via importpy."""
    assert 'math' not in BLACKLISTED_MODULES

def test_importpy_math_works():
    """importpy math must not raise any error."""
    run("importpy math")

def test_importpy_os_not_blacklisted():
    """os module must remain accessible via importpy."""
    assert 'os' not in BLACKLISTED_MODULES

def test_importpy_os_works():
    """importpy os must not raise any error."""
    run("importpy os")

def test_importpy_datetime_not_blacklisted():
    """datetime module must remain accessible via importpy."""
    assert 'datetime' not in BLACKLISTED_MODULES

def test_importpy_datetime_works():
    """importpy datetime must not raise any error."""
    run("importpy datetime")
