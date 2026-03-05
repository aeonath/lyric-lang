# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Lexer module for tokenizing Lyric source code."""

from dataclasses import dataclass
from typing import List
from lyric.errors import LexError


@dataclass
class Token:
    """Represents a token with type, value, line, and column information."""
    type: str
    value: str
    line: int
    col: int


class Lexer:
    """Tokenizes Lyric source code into a list of tokens."""
    
    # Keywords
    KEYWORDS = {
        'def', 'class', 'if', 'else', 'elif', 'case', 'given', 'for', 'done', 'end', 
        'try', 'catch', 'finally', 'fade', 'and', 'or', 'not', 'in', 'as', 'return',
        'int', 'str', 'flt', 'var', 'pyobject', 'rex', 'god', 'bin', 'arr', 'map', 'obj', 'dsk', 'tup', 'True', 'False', 'true', 'false', 'None', 'raise', 'import', 'importpy',
        'break', 'continue', 'public', 'private', 'protected'
    }
    
    # Single character operators and delimiters
    SINGLE_CHARS = {
        '+', '-', '*', '/', '%', '=', '(', ')', '{', '}', ':', ',', ';', '.', '[', ']'
    }

    # Operator type mappings
    OPERATOR_TYPES = {
        '>': 'GT',
        '<': 'LT',
        '=': 'ASSIGN',
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULTIPLY',
        '/': 'DIVIDE',
        '%': 'PERCENT',
        '(': 'LPAREN',
        ')': 'RPAREN',
        '{': 'LBRACE',
        '}': 'RBRACE',
        ':': 'COLON',
        ',': 'COMMA',
        ';': 'SEMICOLON',
        '.': 'DOT',
        '[': 'LBRACKET',
        ']': 'RBRACKET'
    }
    
    # Multi-character operators
    MULTI_CHARS = {
        '==', '!=', '<', '<=', '>', '>=', '+++', '->>', '->', '<-', '&&', '||',
        '+=', '-=', '*=', '/=', '%='
    }
    
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.current = 0
        self.line = 1
        self.col = 1
        self.start_col = 1
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code and return a list of tokens."""
        self.tokens = []
        self.current = 0
        self.line = 1
        self.col = 1
        
        while not self._is_at_end():
            self.start_col = self.col
            self._scan_token()
        
        # Add EOF token
        self.tokens.append(Token('EOF', '', self.line, self.col))
        return self.tokens
    
    def _is_at_end(self) -> bool:
        """Check if we've reached the end of the source."""
        return self.current >= len(self.source)
    
    def _advance(self) -> str:
        """Advance to the next character and return the previous one."""
        if not self._is_at_end():
            char = self.source[self.current]
            self.current += 1
            if char == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            return char
        return ''
    
    def _peek(self) -> str:
        """Look at the current character without advancing."""
        if self._is_at_end():
            return ''
        return self.source[self.current]
    
    def _peek_next(self) -> str:
        """Look at the next character without advancing."""
        if self.current + 1 >= len(self.source):
            return ''
        return self.source[self.current + 1]
    
    def _scan_token(self):
        """Scan the next token."""
        char = self._advance()
        
        # Skip whitespace
        if char in ' \t\r':
            return
        
        # Handle newlines
        if char == '\n':
            self.tokens.append(Token('NEWLINE', '\n', self.line - 1, self.start_col))
            return
        
        # Handle comments
        if char == '#':
            self._scan_comment()
            return
        
        # Handle strings (both single and double quotes)
        if char == '"' or char == "'":
            self._scan_string(char)
            return
        
        # Handle division operator (and /= compound assignment)
        if char == '/':
            if self._peek() == '=':
                self._advance()  # consume '='
                self.tokens.append(Token('DIVIDE_ASSIGN', '/=', self.line, self.start_col))
            else:
                self.tokens.append(Token('DIVIDE', char, self.line, self.start_col))
            return
        
        # Handle numbers
        if char.isdigit():
            self._scan_number(char)
            return
        
        # Handle identifiers and keywords
        if char.isalpha() or char == '_':
            self._scan_identifier(char)
            return
        
        # Handle multi-character operators
        if char in '<>=!+-&|':
            self._scan_multi_char_operator(char)
            return
        
        # Handle *= and %= compound assignment operators
        if char == '*' and self._peek() == '=':
            self._advance()  # consume '='
            self.tokens.append(Token('MULTIPLY_ASSIGN', '*=', self.line, self.start_col))
            return
        if char == '%' and self._peek() == '=':
            self._advance()  # consume '='
            self.tokens.append(Token('PERCENT_ASSIGN', '%=', self.line, self.start_col))
            return

        # Handle single character operators and delimiters
        if char in self.SINGLE_CHARS:
            token_type = self.OPERATOR_TYPES.get(char, char)
            self.tokens.append(Token(token_type, char, self.line, self.start_col))
            return
        
        # Unknown character
        raise LexError(f"Unexpected character '{char}' at line {self.line}, column {self.start_col}")
    
    def _scan_comment(self):
        """Scan a comment until end of line."""
        while self._peek() != '\n' and not self._is_at_end():
            self._advance()
    
    def _scan_string(self, quote_char):
        """Scan a string literal with escape sequence handling.
        
        Args:
            quote_char: The quote character that started the string ('"' or "'")
        """
        start_line = self.line
        start_col = self.start_col
        value = ''
        
        while self._peek() != quote_char and not self._is_at_end():
            if self._peek() == '\n':
                raise LexError(f"Unterminated string at line {start_line}, column {start_col}")
            
            # Handle escape sequences
            if self._peek() == '\\':
                self._advance()  # consume the backslash
                if self._is_at_end():
                    raise LexError(f"Unterminated string at line {start_line}, column {start_col}")
                
                escaped = self._advance()
                if escaped == 'n':
                    value += '\n'
                elif escaped == 't':
                    value += '\t'
                elif escaped == 'r':
                    value += '\r'
                elif escaped == '\\':
                    value += '\\'
                elif escaped == '"':
                    value += '"'
                elif escaped == "'":
                    value += "'"
                elif escaped == '/':
                    # Preserve escaped forward slash (for regex patterns)
                    value += '/'
                else:
                    # Unknown escape sequence - include both characters
                    value += '\\' + escaped
            else:
                value += self._advance()
        
        if self._is_at_end():
            raise LexError(f"Unterminated string at line {start_line}, column {start_col}")
        
        # Consume the closing quote
        self._advance()
        
        self.tokens.append(Token('STRING', value, start_line, start_col))
    
    def _scan_number(self, first_char: str):
        """Scan a number (integer or float)."""
        start_line = self.line
        start_col = self.start_col
        value = first_char
        
        # Scan integer part
        while self._peek().isdigit():
            value += self._advance()
        
        # Check for decimal point
        if self._peek() == '.' and self._peek_next().isdigit():
            value += self._advance()  # consume the '.'
            while self._peek().isdigit():
                value += self._advance()
            self.tokens.append(Token('FLOAT', float(value), start_line, start_col))
        else:
            self.tokens.append(Token('INT', int(value), start_line, start_col))
    
    def _scan_identifier(self, first_char: str):
        """Scan an identifier or keyword."""
        start_line = self.line
        start_col = self.start_col
        value = first_char
        
        while self._peek().isalnum() or self._peek() == '_':
            value += self._advance()
        
        # Check if it's a keyword
        if value in self.KEYWORDS:
            if value in ('True', 'False', 'true', 'false'):
                # Convert boolean keywords to actual boolean values
                bool_value = value in ('True', 'true')
                self.tokens.append(Token('BOOLEAN', bool_value, start_line, start_col))
            elif value == 'None':
                # Convert None keyword to actual None value
                self.tokens.append(Token('NONE', None, start_line, start_col))
            elif value in ('int', 'str', 'flt', 'var', 'pyobject', 'rex', 'god', 'bin', 'arr', 'map', 'obj', 'dsk', 'tup'):
                # Type keywords can also be used as identifiers in expressions
                # We'll let the parser decide based on context
                self.tokens.append(Token('TYPE_OR_IDENT', value, start_line, start_col))
            elif value == 'for':
                # Map 'for' to 'GIVEN' token for syntactic sugar
                self.tokens.append(Token('GIVEN', 'for', start_line, start_col))
            elif value == 'case':
                # Map 'case' to 'ELIF' token for syntactic sugar
                self.tokens.append(Token('ELIF', 'case', start_line, start_col))
            else:
                self.tokens.append(Token(value.upper(), value, start_line, start_col))
        else:
            self.tokens.append(Token('IDENT', value, start_line, start_col))
    
    def _scan_multi_char_operator(self, first_char: str):
        """Scan multi-character operators."""
        start_line = self.line
        start_col = self.start_col
        
        if first_char == '+' and self._peek() == '+' and self._peek_next() == '+':
            # Handle +++ (CLASS_END)
            self._advance()  # consume second +
            self._advance()  # consume third +
            self.tokens.append(Token('CLASS_END', '+++', start_line, start_col))
        elif first_char == '-' and self._peek() == '>' and self._peek_next() == '>':
            # Handle ->> (file append operator) - must check before ->
            self._advance()  # consume >
            self._advance()  # consume second >
            self.tokens.append(Token('FILE_APPEND', '->>', start_line, start_col))
        elif first_char == '-' and self._peek() == '>':
            # Handle -> (file write operator)
            self._advance()  # consume >
            self.tokens.append(Token('FILE_WRITE', '->', start_line, start_col))
        elif first_char == '<' and self._peek() == '-':
            # Handle <- (file read operator)
            self._advance()  # consume -
            self.tokens.append(Token('FILE_READ', '<-', start_line, start_col))
        elif first_char == '&' and self._peek() == '&':
            # Handle && (logical AND / exec chain operator)
            self._advance()  # consume second &
            self.tokens.append(Token('AND', '&&', start_line, start_col))
        elif first_char == '|' and self._peek() == '|':
            # Handle || (logical OR / exec chain operator)
            self._advance()  # consume second |
            self.tokens.append(Token('OR', '||', start_line, start_col))
        elif first_char == '|':
            # Handle | (pipe operator)
            self.tokens.append(Token('PIPE', '|', start_line, start_col))
        elif first_char == '+' and self._peek() == '=':
            # Handle += (compound addition assignment)
            self._advance()  # consume '='
            self.tokens.append(Token('PLUS_ASSIGN', '+=', start_line, start_col))
        elif first_char == '-' and self._peek() == '=':
            # Handle -= (compound subtraction assignment)
            self._advance()  # consume '='
            self.tokens.append(Token('MINUS_ASSIGN', '-=', start_line, start_col))
        elif first_char in '<>=!' and self._peek() == '=':
            # Handle <=, >=, ==, !=
            operator = first_char + self._advance()
            self.tokens.append(Token(operator, operator, start_line, start_col))
        else:
            # Single character operator - use proper type
            token_type = self.OPERATOR_TYPES.get(first_char, first_char)
            self.tokens.append(Token(token_type, first_char, start_line, start_col))


def tokenize(source: str) -> List[Token]:
    """Tokenize source code and return a list of tokens."""
    lexer = Lexer(source)
    return lexer.tokenize()