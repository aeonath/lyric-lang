# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for importpy module whitelist and --unsafe flag (Sprint 10 Task 4)."""

import pytest
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import RuntimeErrorLyric
from lyric.pyproxy import (
    WHITELISTED_MODULES,
    BLACKLISTED_MODULES,
    set_unsafe_mode,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(source: str):
    """Parse and evaluate a Lyric source string."""
    ast = parse(source)
    evaluate(ast)


# ---------------------------------------------------------------------------
# Whitelist membership
# ---------------------------------------------------------------------------

def test_whitelist_contains_math():
    assert 'math' in WHITELISTED_MODULES

def test_whitelist_contains_time():
    assert 'time' in WHITELISTED_MODULES

def test_whitelist_contains_datetime():
    assert 'datetime' in WHITELISTED_MODULES

def test_whitelist_contains_os():
    assert 'os' in WHITELISTED_MODULES

def test_whitelist_contains_sys():
    assert 'sys' in WHITELISTED_MODULES

def test_whitelist_contains_random():
    assert 'random' in WHITELISTED_MODULES

def test_whitelist_is_frozenset():
    assert isinstance(WHITELISTED_MODULES, frozenset)

def test_blacklisted_modules_not_in_whitelist():
    """No module should appear in both lists."""
    overlap = WHITELISTED_MODULES & BLACKLISTED_MODULES
    assert overlap == frozenset(), f"Overlap between whitelist and blacklist: {overlap}"


# ---------------------------------------------------------------------------
# Whitelisted modules import without --unsafe
# ---------------------------------------------------------------------------

def test_importpy_math_whitelisted():
    run("importpy math")

def test_importpy_time_whitelisted():
    run("importpy time")

def test_importpy_datetime_whitelisted():
    run("importpy datetime")

def test_importpy_os_whitelisted():
    run("importpy os")

def test_importpy_sys_whitelisted():
    run("importpy sys")

def test_importpy_random_whitelisted():
    run("importpy random")


# ---------------------------------------------------------------------------
# Non-whitelisted, non-blacklisted module blocked without --unsafe
# ---------------------------------------------------------------------------

def test_importpy_itertools_blocked_without_unsafe():
    """A non-whitelisted module must raise a whitelist error without --unsafe."""
    set_unsafe_mode(False)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy itertools")
        msg = str(exc_info.value)
        assert "ImportError" in msg
        assert "itertools" in msg
        assert "not whitelisted" in msg
    finally:
        set_unsafe_mode(False)

def test_importpy_csv_blocked_without_unsafe():
    """csv is not in the whitelist and must be blocked without --unsafe."""
    set_unsafe_mode(False)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy csv")
        msg = str(exc_info.value)
        assert "not whitelisted" in msg
    finally:
        set_unsafe_mode(False)

def test_whitelist_error_contains_module_name():
    set_unsafe_mode(False)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy itertools")
        assert "itertools" in str(exc_info.value)
    finally:
        set_unsafe_mode(False)

def test_whitelist_error_mentions_unsafe_flag():
    set_unsafe_mode(False)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy string")
        assert "--unsafe" in str(exc_info.value)
    finally:
        set_unsafe_mode(False)


# ---------------------------------------------------------------------------
# Non-whitelisted module allowed with --unsafe
# ---------------------------------------------------------------------------

def test_importpy_random_allowed_with_unsafe():
    set_unsafe_mode(True)
    try:
        run("importpy random")  # should not raise
    finally:
        set_unsafe_mode(False)

def test_importpy_json_allowed_with_unsafe():
    set_unsafe_mode(True)
    try:
        run("importpy json")  # should not raise
    finally:
        set_unsafe_mode(False)

def test_importpy_itertools_allowed_with_unsafe():
    set_unsafe_mode(True)
    try:
        run("importpy itertools")  # should not raise
    finally:
        set_unsafe_mode(False)


# ---------------------------------------------------------------------------
# Blacklisted modules always blocked — even with --unsafe
# ---------------------------------------------------------------------------

def test_blacklisted_module_blocked_even_with_unsafe_pdb():
    set_unsafe_mode(True)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy pdb")
        assert "blacklisted" in str(exc_info.value)
    finally:
        set_unsafe_mode(False)

def test_blacklisted_module_blocked_even_with_unsafe_gc():
    set_unsafe_mode(True)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy gc")
        assert "blacklisted" in str(exc_info.value)
    finally:
        set_unsafe_mode(False)

def test_blacklisted_module_blocked_even_with_unsafe_inspect():
    set_unsafe_mode(True)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy inspect")
        assert "blacklisted" in str(exc_info.value)
    finally:
        set_unsafe_mode(False)

def test_blacklisted_module_blocked_even_with_unsafe_ctypes():
    set_unsafe_mode(True)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy ctypes")
        assert "blacklisted" in str(exc_info.value)
    finally:
        set_unsafe_mode(False)

def test_blacklisted_module_blocked_even_with_unsafe_pickle():
    set_unsafe_mode(True)
    try:
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            run("importpy pickle")
        assert "blacklisted" in str(exc_info.value)
    finally:
        set_unsafe_mode(False)


# ---------------------------------------------------------------------------
# unsafe mode state resets correctly
# ---------------------------------------------------------------------------

def test_unsafe_mode_off_by_default():
    """set_unsafe_mode(False) must restore the blocked behaviour."""
    set_unsafe_mode(True)
    set_unsafe_mode(False)
    with pytest.raises(RuntimeErrorLyric):
        run("importpy csv")


# ---------------------------------------------------------------------------
# CLI --blacklist and --whitelist output (via pyproxy constants)
# ---------------------------------------------------------------------------

def test_blacklist_is_frozenset():
    assert isinstance(BLACKLISTED_MODULES, frozenset)

def test_whitelist_and_blacklist_are_disjoint():
    assert WHITELISTED_MODULES.isdisjoint(BLACKLISTED_MODULES)

def test_whitelist_has_at_least_five_modules():
    assert len(WHITELISTED_MODULES) >= 5
