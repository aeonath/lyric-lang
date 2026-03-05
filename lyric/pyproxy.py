# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Python module proxy for importpy functionality."""

import importlib
from typing import Any
from lyric.errors import RuntimeErrorLyric

# Modules that rely on CPython bytecode, frames, object identity, or interpreter
# internals are blacklisted and cannot be imported via importpy in Lyric.
BLACKLISTED_MODULES = frozenset([
    'pdb',
    'trace',
    'traceback',
    'faulthandler',
    'inspect',
    'dis',
    'marshal',
    'pickle',
    'pickletools',
    'copyreg',
    'code',
    'codeop',
    'compile',
    'eval',
    'exec',
    'types',
    'importlib._bootstrap',
    'importlib._bootstrap_external',
    'zipimport',
    'runpy',
    'modulefinder',
    'gc',
    'weakref',
    'ctypes',
    'cffi',
    '_ctypes',
    'mmap',
])

# Specific attributes that are blacklisted on otherwise-allowed modules.
BLACKLISTED_ATTRIBUTES = {
    'sys': frozenset([
        'settrace',       # installs a CPython bytecode trace hook
        'setprofile',     # installs a CPython call/return profile hook
        'gettrace',       # reads back the installed trace hook
        'getprofile',     # reads back the installed profile hook
        '_getframe',      # returns a live CPython frame object
        '_current_frames', # returns all live frames across all threads
        'getrefcount',    # exposes CPython reference-counting internals
        'addaudithook',   # installs a permanent process-wide audit hook
        'exc_info',       # returns (type, value, traceback) with frame refs
    ]),
}

_BLACKLIST_REASON = (
    "This module relies on CPython bytecode, frames, object identity, or "
    "interpreter internals and does not work with Lyric."
)

# Modules explicitly approved for importpy use in Lyric.
WHITELISTED_MODULES = frozenset([
    'math',
    'time',
    'datetime',
    'json',
    'os',
    'sys',
    'random',
    'collections',
    'http.server',
    'requests',
])

_WHITELIST_REASON = (
    "Module is not in the Lyric importpy whitelist. "
    "Use 'lyric run --unsafe <file.ly>' to allow non-whitelisted, non-blacklisted modules."
)

# Global unsafe-mode flag — set to True when --unsafe CLI flag is present.
_unsafe_mode = False

# Stdlib-mode flag — set to True while loading stdlib .ly files.
# Bypasses the whitelist (but NOT the blacklist) so the standard library
# can import any non-blacklisted Python module without --unsafe.
_stdlib_mode = False


def set_unsafe_mode(enabled: bool) -> None:
    """Enable or disable unsafe importpy mode."""
    global _unsafe_mode
    _unsafe_mode = enabled


def is_unsafe_mode() -> bool:
    """Return True if unsafe importpy mode is currently enabled."""
    return _unsafe_mode


def set_stdlib_mode(enabled: bool) -> None:
    """Enable or disable stdlib importpy mode."""
    global _stdlib_mode
    _stdlib_mode = enabled


def is_stdlib_mode() -> bool:
    """Return True if stdlib importpy mode is currently enabled."""
    return _stdlib_mode


def _lyric_to_python(val: Any) -> Any:
    """Convert Lyric runtime collection types to Python-native equivalents.

    Called before passing arguments to Python callables so that Python code
    receives standard Python lists/dicts rather than ArrObject/MapObject
    wrappers that it knows nothing about.

    Uses class-name duck-typing to avoid a circular import with interpreter.py.
    Recurses into nested collections.
    """
    cls = type(val).__name__
    if cls == 'ArrObject':
        return [_lyric_to_python(e) for e in val.elements]
    if cls == 'MapObject':
        return {k: _lyric_to_python(v) for k, v in val.elements.items()}
    if cls == 'TupObject':
        return tuple(_lyric_to_python(e) for e in val.elements)
    return val


class PyModuleProxy:
    """Proxy object that forwards attribute access to Python modules."""

    def __init__(self, module_name: str):
        """Initialize the proxy with a Python module name."""
        self._module_name = module_name
        if module_name in BLACKLISTED_MODULES:
            raise RuntimeErrorLyric(
                f"ImportError: Python module '{module_name}' is blacklisted in Lyric. "
                f"{_BLACKLIST_REASON}"
            )
        if module_name not in WHITELISTED_MODULES and not _unsafe_mode and not _stdlib_mode:
            raise RuntimeErrorLyric(
                f"ImportError: Python module '{module_name}' is not whitelisted in Lyric. "
                f"{_WHITELIST_REASON}"
            )
        try:
            # importlib.import_module handles dotted names correctly:
            # __import__('http.server') returns `http` (top-level package),
            # but importlib.import_module('http.server') returns the
            # http.server submodule itself, which is what we want.
            self._module = importlib.import_module(module_name)
        except ImportError:
            raise RuntimeErrorLyric(f"ImportError: cannot import Python module '{module_name}'")
    
    def __getattr__(self, name: str) -> Any:
        """Forward attribute access to the underlying Python module."""
        blocked = BLACKLISTED_ATTRIBUTES.get(self._module_name)
        if blocked and name in blocked:
            raise RuntimeErrorLyric(
                f"AttributeError: '{self._module_name}.{name}' is blacklisted in Lyric. "
                f"{_BLACKLIST_REASON}"
            )
        try:
            attr = getattr(self._module, name)
            # Only wrap functions, not classes
            if callable(attr) and not isinstance(attr, type):
                return PyCallableProxy(attr, f"{self._module_name}.{name}")
            return attr
        except AttributeError as e:
            raise RuntimeErrorLyric(f"AttributeError: '{self._module_name}' has no attribute '{name}'")
    
    def __repr__(self) -> str:
        """Return a string representation of the proxy."""
        return f"<PyModuleProxy {self._module_name}>"


class PyCallableProxy:
    """Proxy for callable Python objects."""
    
    def __init__(self, callable_obj: Any, name: str):
        """Initialize the proxy with a callable object."""
        self._callable = callable_obj
        self._name = name
    
    def __call__(self, *args, **kwargs) -> Any:
        """Call the underlying callable object."""
        converted = [_lyric_to_python(a) for a in args]
        try:
            return self._callable(*converted, **kwargs)
        except Exception as e:
            raise RuntimeErrorLyric(f"Error calling '{self._name}': {str(e)}")
    
    def __getattr__(self, name: str) -> Any:
        """Forward attribute access to the underlying callable (e.g. class methods)."""
        attr = getattr(self._callable, name)
        if callable(attr) and not isinstance(attr, type):
            return PyCallableProxy(attr, f"{self._name}.{name}")
        return attr

    def __repr__(self) -> str:
        """Return a string representation of the proxy."""
        return f"<PyCallableProxy {self._name}>"
