# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Error classes for Lyric language."""

class LexError(Exception):
    """Raised when lexing fails."""
    def __init__(self, message: str, line: int = 0, column: int = 0, filename: str = ""):
        super().__init__(message)
        self.line = line
        self.column = column
        self.filename = filename
    
    def __str__(self):
        if self.filename:
            return f"Lexical error in {self.filename}: {super().__str__()}"
        else:
            return f"Lexical error: {super().__str__()}"


class ParseError(Exception):
    """Raised when parsing fails."""
    def __init__(self, message: str, line: int = 0, column: int = 0, filename: str = ""):
        super().__init__(message)
        self.line = line
        self.column = column
        self.filename = filename
    
    def __str__(self):
        if self.filename:
            return f"Parse error in {self.filename}: {super().__str__()}"
        else:
            return f"Parse error: {super().__str__()}"


class SyntaxErrorLyric(ParseError):
    """Raised when syntax is invalid."""
    pass


class RuntimeErrorLyric(Exception):
    """Raised when runtime execution fails."""
    def __init__(self, message: str, line: int = 0, column: int = 0, filename: str = ""):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.filename = filename

    def __str__(self):
        return self.message


class NameErrorLyric(RuntimeErrorLyric):
    """Raised when a name is not defined."""
    pass


class CompileErrorLyric(RuntimeErrorLyric):
    """Raised when compilation fails (e.g., redeclaration)."""
    pass


# Exception Type Hierarchy for catch clauses
class LyricError(RuntimeErrorLyric):
    """Base class for all Lyric exceptions."""
    def __init__(self, message: str, line: int = 0, column: int = 0, filename: str = ""):
        super().__init__(message, line, column, filename)
        self.exception_type = self.__class__.__name__
        self.message = message
    
    def __str__(self):
        # Return just the message for string concatenation
        return self.message


class TypeErrorLyric(LyricError):
    """Raised when a type error occurs."""
    pass


class ValueErrorLyric(LyricError):
    """Raised when a value error occurs."""
    pass


class IndexErrorLyric(LyricError):
    """Raised when an index error occurs."""
    pass


class KeyErrorLyric(LyricError):
    """Raised when a key error occurs."""
    pass


class AttributeErrorLyric(LyricError):
    """Raised when an attribute error occurs."""
    pass


class ZeroDivisionErrorLyric(LyricError):
    """Raised when division by zero occurs."""
    pass


# Exception type mapping for catch clauses
EXCEPTION_TYPES = {
    'Error': Exception,
    'TypeError': TypeErrorLyric,
    'ValueError': ValueErrorLyric,
    'NameError': NameErrorLyric,
    'RuntimeError': RuntimeErrorLyric,
    'IndexError': IndexErrorLyric,
    'KeyError': KeyErrorLyric,
    'AttributeError': AttributeErrorLyric,
    'ZeroDivisionError': ZeroDivisionErrorLyric,
    'CompileError': CompileErrorLyric,
}


# Control flow signals (not exceptions, subclass BaseException)
class BreakSignal(BaseException):
    """Internal signal for break statement."""
    def __init__(self, line: int = 0, column: int = 0):
        super().__init__()
        self.line = line
        self.column = column


class ContinueSignal(BaseException):
    """Internal signal for continue statement."""
    def __init__(self, line: int = 0, column: int = 0):
        super().__init__()
        self.line = line
        self.column = column
