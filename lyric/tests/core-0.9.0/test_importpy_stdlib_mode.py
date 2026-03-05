# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for stdlib_mode: stdlib .ly files bypass the importpy whitelist
but are still blocked by the blacklist."""

import pytest
from lyric.pyproxy import (
    set_stdlib_mode,
    is_stdlib_mode,
    set_unsafe_mode,
    BLACKLISTED_MODULES,
    WHITELISTED_MODULES,
)
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import RuntimeErrorLyric


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(source: str):
    """Parse and evaluate a Lyric source string."""
    ast = parse(source)
    evaluate(ast)


# ---------------------------------------------------------------------------
# stdlib_mode flag basics
# ---------------------------------------------------------------------------

def test_stdlib_mode_off_by_default():
    assert is_stdlib_mode() is False

def test_stdlib_mode_toggle_on():
    set_stdlib_mode(True)
    try:
        assert is_stdlib_mode() is True
    finally:
        set_stdlib_mode(False)

def test_stdlib_mode_toggle_off():
    set_stdlib_mode(True)
    set_stdlib_mode(False)
    assert is_stdlib_mode() is False


# ---------------------------------------------------------------------------
# stdlib_mode bypasses the whitelist
# ---------------------------------------------------------------------------

def test_stdlib_mode_allows_non_whitelisted_module():
    """A non-whitelisted module should import fine under stdlib_mode."""
    set_stdlib_mode(True)
    try:
        run("importpy glob")  # glob is not whitelisted
    finally:
        set_stdlib_mode(False)

def test_stdlib_mode_allows_itertools():
    """itertools is not whitelisted but should work under stdlib_mode."""
    set_stdlib_mode(True)
    try:
        run("importpy itertools")
    finally:
        set_stdlib_mode(False)

def test_non_whitelisted_still_blocked_without_stdlib_mode():
    """Confirm that without stdlib_mode, non-whitelisted modules are blocked."""
    set_unsafe_mode(False)
    set_stdlib_mode(False)
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        run("importpy glob")
    assert "not whitelisted" in str(exc_info.value)


# ---------------------------------------------------------------------------
# stdlib_mode does NOT bypass the blacklist
# ---------------------------------------------------------------------------

def test_stdlib_mode_still_blocks_blacklisted_pdb():
    set_stdlib_mode(True)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy pdb")
        assert "blacklisted" in str(exc_info.value)
    finally:
        set_stdlib_mode(False)

def test_stdlib_mode_still_blocks_blacklisted_gc():
    set_stdlib_mode(True)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy gc")
        assert "blacklisted" in str(exc_info.value)
    finally:
        set_stdlib_mode(False)

def test_stdlib_mode_still_blocks_blacklisted_ctypes():
    set_stdlib_mode(True)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy ctypes")
        assert "blacklisted" in str(exc_info.value)
    finally:
        set_stdlib_mode(False)

def test_stdlib_mode_still_blocks_blacklisted_inspect():
    set_stdlib_mode(True)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy inspect")
        assert "blacklisted" in str(exc_info.value)
    finally:
        set_stdlib_mode(False)


# ---------------------------------------------------------------------------
# stdlib_mode resets correctly
# ---------------------------------------------------------------------------

def test_stdlib_mode_reset_restores_whitelist_check():
    """After stdlib_mode is turned off, whitelist enforcement resumes."""
    set_stdlib_mode(True)
    run("importpy glob")  # should succeed
    set_stdlib_mode(False)
    with pytest.raises(RuntimeErrorLyric):
        run("importpy glob")  # should fail again


# ---------------------------------------------------------------------------
# Lyric stdlib loads without --unsafe
# ---------------------------------------------------------------------------

def test_import_lyric_stdlib_loads_without_unsafe():
    """import lyric should succeed even though lyric.ly uses non-whitelisted
    Python modules (e.g. glob), because stdlib loading enables stdlib_mode."""
    set_unsafe_mode(False)
    set_stdlib_mode(False)
    run("import lyric")
