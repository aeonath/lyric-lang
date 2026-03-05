# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Command-line interface for Lyric interpreter."""

import sys
import os
from lyric.errors import LexError, ParseError, RuntimeErrorLyric, SyntaxErrorLyric, NameErrorLyric
from lyric.parser import parse, Parser
from lyric.lexer import tokenize
from lyric.interpreter import evaluate, Interpreter
from lyric.runtime import set_command_line_options
from lyric import __version__


def _parse_options(args):
    """Parse command-line options and separate them from regular arguments.
    
    Returns:
        tuple: (options_dict, arguments_list)
        - options_dict: Dictionary mapping option names to their values
        - arguments_list: List of non-option arguments
    """
    options = {}
    arguments = []
    i = 0
    
    while i < len(args):
        arg = args[i]
        
        # Check if it's an option
        if arg.startswith('--'):
            # Long option (e.g., --verbose or --file=myfile)
            if '=' in arg:
                # Option with value: --file=myfile
                option_name = arg[2:].split('=', 1)[0]
                option_value = arg.split('=', 1)[1]
                options[option_name] = option_value
            else:
                # Flag without value: --verbose
                option_name = arg[2:]
                options[option_name] = None  # Flag present, no value
        elif arg.startswith('-') and len(arg) >= 2 and arg[1].isalpha():
            # Short option (e.g., -a or multi-char -hc)
            if '=' in arg:
                option_name = arg[1:].split('=', 1)[0]
                option_value = arg.split('=', 1)[1]
                options[option_name] = option_value
            else:
                option_name = arg[1:]
                options[option_name] = None
        else:
            # Not an option, it's a regular argument
            arguments.append(arg)
        
        i += 1
    
    return options, arguments


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: lyric --version | lyric --help | lyric run <file.ly> | lyric <file.ly> | lyric -i [code]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--version":
        print(f"Lyric {__version__}")
    elif command == "--blacklist":
        from lyric.pyproxy import BLACKLISTED_MODULES
        print("Importpy Blacklist — modules that cannot be imported even with --unsafe:")
        print("(These rely on CPython bytecode, frames, object identity, or interpreter internals.)")
        print()
        for mod in sorted(BLACKLISTED_MODULES):
            print(f"  {mod}")
        sys.exit(0)
    elif command == "--whitelist":
        from lyric.pyproxy import WHITELISTED_MODULES
        print("Importpy Whitelist — modules approved for importpy use in Lyric:")
        print("(Use --unsafe to allow non-whitelisted, non-blacklisted modules.)")
        print()
        for mod in sorted(WHITELISTED_MODULES):
            print(f"  {mod}")
        sys.exit(0)
    elif command == "--help":
        print("Lyric Language Interpreter")
        print("")
        print("Usage:")
        print("  lyric --version                    Show version information")
        print("  lyric --help                       Show this help message")
        print("  lyric --blacklist                  Print the importpy module blacklist")
        print("  lyric --whitelist                  Print the importpy module whitelist")
        print("  lyric run <file.ly> [options] [args]  Run a Lyric source file with options and arguments")
        print("  lyric <file.ly> [options] [args]      Run a Lyric source file (shorthand)")
        print("  lyric -i [code]                   Interactive mode (REPL) or execute immediate code")
        print("")
        print("Options:")
        print("  -a, -b, -c, etc.                  Short options (single character)")
        print("  --verbose, --debug, etc.          Long options (multiple characters)")
        print("  --file=myfile                     Long option with value")
        print("  --unsafe                          Allow importpy of non-whitelisted modules")
        print("                                    (blacklisted modules are still blocked)")
        print("")
        print("Arguments:")
        print("  Arguments are passed after options and available via main(argc, argv)")
        print("")
        print("Examples:")
        print("  lyric run hello.ly")
        print("  lyric hello.ly")
        print("  lyric hello.ly -a --verbose --file=myfile arg1 arg2")
        print('  lyric -i "print(2 + 2)"')
        print("  lyric -i                           Start REPL")
        sys.exit(0)
    elif command == "-i":
        # Interactive/Immediate mode
        if len(sys.argv) > 2:
            # Execute immediate code passed as argument
            code = ' '.join(sys.argv[2:])
            _execute_immediate(code)
        else:
            # Start REPL
            _start_repl()
    elif command == "run":
        if len(sys.argv) < 3:
            print("Usage: lyric run <file.ly> [options] [arguments]")
            sys.exit(1)
        
        # Parse options and get filename and arguments
        options, remaining = _parse_options(sys.argv[2:])
        
        if not remaining:
            print("Usage: lyric run <file.ly> [options] [arguments]")
            sys.exit(1)
        
        file_path = remaining[0]
        arguments = remaining[1:]  # Everything after the filename
        
        # Set command-line options for getopts()
        set_command_line_options(options, sys.argv[2:])

        # Activate unsafe importpy mode if --unsafe flag is present
        if 'unsafe' in options:
            from lyric.pyproxy import set_unsafe_mode
            set_unsafe_mode(True)

        _execute_file(file_path, arguments)
    elif command.endswith('.ly'):
        # Treat as shorthand for "lyric run <file.ly>"
        # Parse options from remaining args
        options, remaining = _parse_options(sys.argv[2:])

        file_path = command
        arguments = remaining  # All remaining args are arguments

        # Set command-line options for getopts()
        set_command_line_options(options, sys.argv[2:])

        # Activate unsafe importpy mode if --unsafe flag is present
        if 'unsafe' in options:
            from lyric.pyproxy import set_unsafe_mode
            set_unsafe_mode(True)

        _execute_file(file_path, arguments)
    else:
        print(f"Unknown command: {command}")
        print("Usage: lyric --version | lyric --help | lyric run <file.ly> | lyric <file.ly> | lyric -i [code]")
        sys.exit(1)


def _remove_shebang(source: str) -> str:
    """Remove shebang line from source code if present."""
    lines = source.splitlines()
    
    # Check if first line is a shebang
    if lines and lines[0].startswith('#!'):
        # Remove the shebang line
        return '\n'.join(lines[1:])
    
    return source


def _check_for_auto_help(source: str, file_path: str):
    """Check if -h was passed and program doesn't override it.
    
    Returns True if auto-help was shown, False otherwise.
    """
    from lyric.runtime import get_command_line_options
    
    options = get_command_line_options()
    
    # Check if -h or --help was passed
    if 'h' not in options and 'help' not in options:
        return False

    # Check if the program handles -h/--help itself via getopts.
    # Matches getopts("h", ...) as the short arg, or getopts(..., "help") as the long arg.
    import re
    if re.search(r'''getopts\(\s*["']h["']''', source):
        return False
    if re.search(r''',\s*["']help["']''', source):
        return False

    # Auto-generate help
    print(f"Usage: lyric {os.path.basename(file_path)} [options] [arguments]")
    print()
    print("Auto-generated help (use getopts(\"h\", \"help\") in your program to override)")
    print()

    # Scan for getopts calls to list available options.
    # getopts() always takes two args: getopts(short, long)
    # Either arg can be None.
    getopts_calls = re.findall(r'getopts\(([^)]+)\)', source)

    options_found = []
    for call_args in getopts_calls:
        # Extract quoted strings and None tokens
        parts = [p.strip() for p in call_args.split(',')]
        short = None
        long = None
        if len(parts) >= 1:
            m = re.search(r'''["']([^"']+)["']''', parts[0])
            if m:
                short = m.group(1)
        if len(parts) >= 2:
            m = re.search(r'''["']([^"']+)["']''', parts[1])
            if m:
                long = m.group(1)

        if short and long:
            options_found.append(f"  -{short}, --{long}")
        elif short:
            options_found.append(f"  -{short}")
        elif long:
            options_found.append(f"  --{long}")

    if options_found:
        print("Available options:")
        for opt in sorted(set(options_found)):
            print(opt)
    else:
        print("No options defined in this program.")

    print()
    print("Arguments:")
    if 'def main(int argc, arr argv)' in source or 'def main(argc, argv)' in source:
        print("  This program accepts command-line arguments via main(argc, argv)")
    else:
        print("  This program does not accept arguments")

    return True


def _execute_file(file_path: str, arguments: list = None):
    """Execute a Lyric source file.
    
    Args:
        file_path: Path to the .ly file to execute
        arguments: List of command-line arguments to pass to main()
    """
    if arguments is None:
        arguments = []
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    
    # Check file extension
    if not file_path.endswith('.ly'):
        print(f"Error: File '{file_path}' is not a .ly file")
        sys.exit(1)
    
    try:
        # Read and execute the file
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Remove shebang line if present
        source = _remove_shebang(source)
        
        # Check for auto-help before parsing/executing
        if _check_for_auto_help(source, file_path):
            sys.exit(0)
        
        # Parse the source code
        ast = parse(source)
        
        # Execute the program, passing the source file path for relative imports
        # and the command-line arguments
        evaluate(ast, source_file=file_path, cli_args=arguments)
        
    except (LexError, ParseError, SyntaxErrorLyric) as e:
        # Syntax/lexical errors
        if hasattr(e, 'line') and e.line > 0:
            print(f"Error [line {e.line}]: {e.args[0] if e.args else str(e)}")
        else:
            print(f"Error: {e}")
        sys.exit(1)
    except (RuntimeErrorLyric, NameErrorLyric) as e:
        # Runtime errors
        if hasattr(e, 'line') and e.line > 0:
            print(f"Runtime error [line {e.line}]: {e.args[0] if e.args else str(e)}")
        else:
            print(f"Runtime error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def _execute_immediate(code: str):
    """Execute immediate code in interactive mode (no main() required)."""
    try:
        # Create parser with interactive mode enabled
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True  # Mark as interactive mode
        parser.is_top_level = False  # Disable top-level restrictions
        ast = parser.parse()

        # Execute the code
        interpreter = Interpreter()
        interpreter.evaluate(ast)

    except (LexError, ParseError, SyntaxErrorLyric) as e:
        if hasattr(e, 'line') and e.line > 0:
            print(f"Error [line {e.line}]: {e.args[0] if e.args else str(e)}")
        else:
            print(f"Error: {e}")
        sys.exit(1)
    except (RuntimeErrorLyric, NameErrorLyric) as e:
        if hasattr(e, 'line') and e.line > 0:
            print(f"Runtime error [line {e.line}]: {e.args[0] if e.args else str(e)}")
        else:
            print(f"Runtime error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def _repl_input(prompt):
    """Read a line of input with immediate Ctrl+D (EOF) support.

    On Windows, input() uses the C runtime fgets() which only recognises
    Ctrl+Z as EOF.  Ctrl+D is passed through as a literal \\x04 character
    and requires Enter before the line is returned.  To match Unix behaviour
    (and Python 3.14's own REPL which uses ReadConsoleInput), we read raw
    keystrokes via msvcrt so Ctrl+D triggers EOFError immediately.
    """
    if sys.platform == 'win32':
        try:
            import msvcrt
            sys.stdout.write(prompt)
            sys.stdout.flush()
            chars = []
            while True:
                ch = msvcrt.getwch()
                if ch == '\x04':          # Ctrl+D
                    sys.stdout.write('\n')
                    raise EOFError()
                if ch == '\x03':          # Ctrl+C
                    sys.stdout.write('\n')
                    raise KeyboardInterrupt()
                if ch in ('\r', '\n'):    # Enter
                    sys.stdout.write('\n')
                    return ''.join(chars)
                if ch == '\x08':          # Backspace
                    if chars:
                        chars.pop()
                        sys.stdout.write('\x08 \x08')
                        sys.stdout.flush()
                    continue
                if ch in ('\x00', '\xe0'):  # Special key prefix (arrows, etc.)
                    msvcrt.getwch()         # consume the scancode
                    continue
                chars.append(ch)
                sys.stdout.write(ch)
                sys.stdout.flush()
        except ImportError:
            pass
    # Unix / fallback
    return input(prompt)


def _start_repl():
    """Start interactive REPL (Read-Eval-Print Loop)."""
    print("Lyric {} Interactive Mode".format(__version__))
    print('Type "exit()" or press Ctrl+D to quit')
    print()

    interpreter = Interpreter()
    buffer = []
    in_block = False
    block_depth = 0

    while True:
        try:
            # Show prompt
            if in_block:
                line = _repl_input("...   ")
            else:
                line = _repl_input("lyric> ")

            # Check for exit command
            if line.strip() in ('exit()', 'quit()', 'exit', 'quit'):
                print("Goodbye!")
                break
            
            # Add line to buffer
            buffer.append(line)
            
            # Check if we're in a block (function, class, control structure)
            stripped = line.strip()
            if stripped:
                # Check for block start
                if any(keyword in stripped for keyword in ['def ', 'class ', 'if ', 'given ', 'for ', 'try:', 'catch:', 'finally:']):
                    in_block = True
                    # Only count keyword toward depth for end-style blocks;
                    # brace-style blocks track depth via { } below
                    if '{' not in line:
                        block_depth += 1
                
                # Track braces and block ends
                if '{' in line:
                    block_depth += line.count('{')
                if '}' in line:
                    block_depth -= line.count('}')
                if stripped in ('end', 'done', 'fade', '+++'):
                    block_depth -= 1
                
                # Check if block is complete
                if in_block and block_depth <= 0:
                    in_block = False
                    block_depth = 0
            
            # If not in block, execute the buffer
            if not in_block and buffer:
                code = '\n'.join(buffer)
                buffer = []
                
                try:
                    # Parse and execute (with top-level restrictions disabled)
                    tokens = tokenize(code)
                    parser = Parser(tokens)
                    parser._interactive_mode = True  # Mark as interactive mode
                    parser.is_top_level = False  # Disable top-level restrictions in REPL
                    ast = parser.parse()
                    
                    # Execute using the persistent interpreter
                    interpreter.evaluate(ast)
                    
                except (LexError, ParseError, SyntaxErrorLyric) as e:
                    if hasattr(e, 'line') and e.line > 0:
                        print(f"Error [line {e.line}]: {e.args[0] if e.args else str(e)}")
                    else:
                        print(f"Error: {e}")
                except (RuntimeErrorLyric, NameErrorLyric) as e:
                    if hasattr(e, 'line') and e.line > 0:
                        print(f"Runtime error [line {e.line}]: {e.args[0] if e.args else str(e)}")
                    else:
                        print(f"Runtime error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    import traceback
                    traceback.print_exc()
        
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            buffer = []
            in_block = False
            block_depth = 0
            continue
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
