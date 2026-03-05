# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Runtime module with built-in functions."""

from typing import Any, Iterator
from lyric.errors import RuntimeErrorLyric


def print_builtin(*args: Any) -> None:
    """Built-in print function that writes to stdout with single space joining."""
    if not args:
        print()
        return
    
    # Convert all arguments to strings and join with single space
    output = ' '.join(str(arg) for arg in args)
    print(output)


def input_builtin(prompt: str = "") -> str:
    """Built-in input function that reads from stdin."""
    return input(prompt)


def int_builtin(value: Any) -> int:
    """Built-in int conversion function."""
    # Import ArrObject and MapObject here to avoid circular imports
    from lyric.interpreter import ArrObject, MapObject
    
    # Handle arr type (ArrObject) - return length
    if isinstance(value, ArrObject):
        return len(value.elements)
    # Handle arr type (list) - return length
    elif isinstance(value, list):
        return len(value)
    # Handle map type (MapObject) - return number of keys
    elif isinstance(value, MapObject):
        return len(value.elements)
    # Handle map type (dict) - return number of keys
    elif isinstance(value, dict) and not ('__instance_class__' in value):
        return len(value)
    # Default behavior for other types
    return int(value)


def flt_builtin(value: Any) -> float:
    """Built-in flt conversion function."""
    # Import ArrObject and MapObject here to avoid circular imports
    from lyric.interpreter import ArrObject, MapObject
    
    # Handle arr type (ArrObject) - return length as float
    if isinstance(value, ArrObject):
        return float(len(value.elements))
    # Handle arr type (list) - return length as float
    elif isinstance(value, list):
        return float(len(value))
    # Handle map type (MapObject) - return number of keys as float
    elif isinstance(value, MapObject):
        return float(len(value.elements))
    # Handle map type (dict) - return number of keys as float
    elif isinstance(value, dict) and not ('__instance_class__' in value):
        return float(len(value))
    # Default behavior for other types
    return float(value)


def str_builtin(value: Any) -> str:
    """Built-in str conversion function."""
    # Note: str(arr) and str(map) return string representations
    # Getting the variable name would require tracking at the interpreter level
    return str(value)


def tup_builtin(value: Any) -> Any:
    """Built-in tup() — convert an arr or list to a TupObject (immutable tuple).

    Examples
    --------
    tup([1, 2, 3])          # -> TupObject (1, 2, 3)
    tup(["a", "b"])         # -> TupObject ("a", "b")
    """
    from lyric.interpreter import ArrObject, TupObject
    if isinstance(value, TupObject):
        return value
    if isinstance(value, ArrObject):
        return TupObject(list(value.elements))
    if isinstance(value, (list, tuple)):
        return TupObject(list(value))
    raise RuntimeErrorLyric(
        f"TypeError: tup() expects an arr or list, got {type(value).__name__}"
    )


def bin_builtin(value: Any) -> bool:
    """Built-in bin (boolean) conversion function.
    
    Converts various types to boolean using Python's truthiness rules:
    - 0, 0.0, empty string, empty collections -> False
    - Non-zero numbers, non-empty strings/collections -> True
    """
    return bool(value)


def god_builtin(value: Any) -> bool:
    """Built-in god (boolean) conversion function.
    
    Alias for bin(). Converts various types to boolean using Python's truthiness rules:
    - 0, 0.0, empty string, empty collections -> False
    - Non-zero numbers, non-empty strings/collections -> True
    """
    return bool(value)


def arr_builtin(value: Any) -> Any:
    """Built-in arr conversion function to create lists."""
    # Import ArrObject and MapObject here to avoid circular imports
    from lyric.interpreter import ArrObject, MapObject
    
    # Handle string - convert to list of characters
    if isinstance(value, str):
        return ArrObject(list(value))
    # Handle MapObject - convert to list of values
    elif isinstance(value, MapObject):
        return ArrObject(list(value.elements.values()))
    # Handle dict (map) - convert to list of values
    elif isinstance(value, dict) and not ('__instance_class__' in value):
        return ArrObject(list(value.values()))
    # Handle already an ArrObject
    elif isinstance(value, ArrObject):
        return value
    # Handle plain Python list - wrap it
    elif isinstance(value, list):
        return ArrObject(value)
    # Try to convert iterable types
    else:
        try:
            return ArrObject(list(value))
        except TypeError:
            raise RuntimeErrorLyric(f"Cannot convert {type(value).__name__} to arr")


def map_builtin(value: Any) -> Any:
    """Built-in map conversion function to create dictionaries."""
    # Import ArrObject and MapObject here to avoid circular imports
    from lyric.interpreter import ArrObject, MapObject
    
    # Handle ArrObject - convert to dict with string keys "1", "2", "3", etc.
    if isinstance(value, ArrObject):
        result = {str(i + 1): val for i, val in enumerate(value.elements)}
        return MapObject(result)
    # Handle list (arr) - convert to dict with string keys "1", "2", "3", etc.
    elif isinstance(value, list):
        result = {str(i + 1): val for i, val in enumerate(value)}
        return MapObject(result)
    # Handle MapObject - return as is
    elif isinstance(value, MapObject):
        return value
    # Handle string - not directly supported, raise error
    elif isinstance(value, str):
        raise RuntimeErrorLyric("Cannot directly convert str to map. Consider using dict comprehension or manual construction.")
    # Handle already a dict - wrap in MapObject
    elif isinstance(value, dict):
        return MapObject(value)
    # Try to convert other dict-like types
    else:
        try:
            result = dict(value)
            return MapObject(result)
        except (TypeError, ValueError) as e:
            raise RuntimeErrorLyric(f"Cannot convert {type(value).__name__} to map: {e}")


def range_builtin(n: int) -> Iterator[int]:
    """Built-in range function that yields 0..N-1."""
    return range(n)


def len_builtin(obj: Any) -> int:
    """Built-in len function."""
    return len(obj)


def open_builtin(path: str) -> Iterator[str]:
    """Built-in open function that returns an iterable over lines."""
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.rstrip('\n\r')


def regex_builtin(pattern: str, flags: str = "") -> Any:
    """Built-in regex constructor function that creates a rex object."""
    try:
        import re
        
        # Strip leading and trailing slashes from pattern if present
        if pattern.startswith('/') and pattern.endswith('/'):
            pattern = pattern[1:-1]
        
        # Parse flags if provided
        flag_value = 0
        if flags:
            for flag_char in flags:
                if flag_char == 'i':
                    flag_value |= re.IGNORECASE
                elif flag_char == 'm':
                    flag_value |= re.MULTILINE
                elif flag_char == 's':
                    flag_value |= re.DOTALL
                elif flag_char == 'x':
                    flag_value |= re.VERBOSE
                else:
                    raise RuntimeErrorLyric(f"Unknown regex flag: '{flag_char}'. Supported flags: i, m, s, x")
        
        # Compile the regex pattern
        compiled_pattern = re.compile(pattern, flag_value)
        
        # Import RexObject from interpreter to avoid circular imports
        from lyric.interpreter import RexObject
        return RexObject(compiled_pattern)
        
    except re.error as e:
        raise RuntimeErrorLyric(f"Invalid regex pattern '{pattern}': {e}")
    except Exception as e:
        raise RuntimeErrorLyric(f"Error creating regex: {e}")


def isinstance_builtin(obj: Any, class_or_type: Any) -> bool:
    """Built-in isinstance function for checking type names."""
    # Handle Lyric class instances
    if isinstance(obj, dict) and '__instance_class__' in obj:
        instance_class = obj['__instance_class__']
        
        # Check against class definition (dict)
        if isinstance(class_or_type, dict) and '__class_name__' in class_or_type:
            return instance_class == class_or_type['__class_name__']
        
        # Check against class name string
        if isinstance(class_or_type, str):
            return instance_class == class_or_type
    
    # Handle Python built-in types
    if isinstance(class_or_type, type):
        return isinstance(obj, class_or_type)
    
    # Handle string type names
    if isinstance(class_or_type, str):
        if class_or_type == "int":
            return isinstance(obj, int)
        elif class_or_type == "float" or class_or_type == "flt":
            return isinstance(obj, float)
        elif class_or_type == "str":
            return isinstance(obj, str)
        elif class_or_type == "list":
            return isinstance(obj, list)
        elif class_or_type == "dict":
            return isinstance(obj, dict)
        elif class_or_type == "bool":
            return isinstance(obj, bool)
        elif class_or_type == "god":
            return isinstance(obj, bool)  # god type represents boolean values
        elif class_or_type == "bin":
            return isinstance(obj, bool)  # bin is an alias for god
        elif class_or_type == "None":
            return obj is None
        elif class_or_type == "pyobject":
            # pyobject represents any Python object that's not a basic Lyric type
            return not (isinstance(obj, dict) and '__instance_class__' in obj)
    
    # Handle when class_or_type is a built-in function (int_builtin, str_builtin, etc.)
    # Map built-in functions to their corresponding Python types
    if callable(class_or_type):
        if class_or_type.__name__ == "int_builtin":
            return isinstance(obj, int)
        elif class_or_type.__name__ == "flt_builtin":
            return isinstance(obj, float)
        elif class_or_type.__name__ == "str_builtin":
            return isinstance(obj, str)
        elif class_or_type.__name__ == "bin_builtin" or class_or_type.__name__ == "god_builtin":
            return isinstance(obj, bool)
        elif class_or_type.__name__ == "arr_builtin":
            from lyric.interpreter import ArrObject
            return isinstance(obj, (list, ArrObject))
        elif class_or_type.__name__ == "map_builtin":
            from lyric.interpreter import MapObject
            return isinstance(obj, (dict, MapObject)) and not (isinstance(obj, dict) and '__instance_class__' in obj)
    
    return False


def type_builtin(obj: Any) -> str:
    """Built-in type function returning the object's class name or Python type."""
    # Import here to avoid circular imports
    from lyric.interpreter import ArrObject, MapObject

    # Handle Lyric class instances
    if isinstance(obj, dict) and '__instance_class__' in obj:
        return obj['__instance_class__']

    # Handle Lyric container types
    if isinstance(obj, ArrObject):
        return "arr"
    elif isinstance(obj, MapObject):
        return "map"

    # Handle Python built-in types (check bool first since it's a subclass of int)
    elif isinstance(obj, bool):
        return "god"  # Return "god" for boolean types (honoring Kurt Gödel)
    elif isinstance(obj, int):
        return "int"
    elif isinstance(obj, float):
        return "float"
    elif isinstance(obj, str):
        return "str"
    elif isinstance(obj, list):
        return "list"
    elif obj is None:
        return "None"
    else:
        # For any other Python object, return "pyobject"
        return "pyobject"


def append_builtin(obj: Any, item: Any) -> None:
    """Built-in append function that adds an item to a list."""
    if isinstance(obj, list):
        obj.append(item)
    else:
        raise RuntimeErrorLyric(f"append() only works on lists, got {type(obj).__name__}")


def keys_builtin(obj: Any) -> list:
    """Built-in keys function that returns dictionary keys."""
    if isinstance(obj, dict):
        return list(obj.keys())
    else:
        raise RuntimeErrorLyric(f"keys() only works on dictionaries, got {type(obj).__name__}")


def values_builtin(obj: Any) -> list:
    """Built-in values function that returns dictionary values."""
    if isinstance(obj, dict):
        return list(obj.values())
    else:
        raise RuntimeErrorLyric(f"values() only works on dictionaries, got {type(obj).__name__}")


# Global storage for command-line options
_command_line_options = {}
_command_line_raw_args = []


def set_command_line_options(options: dict, raw_args: list = None) -> None:
    """Set the command-line options to be accessed by getopts()."""
    global _command_line_options, _command_line_raw_args
    _command_line_options = options
    _command_line_raw_args = raw_args if raw_args is not None else []


def get_command_line_options() -> dict:
    """Get the current command-line options."""
    global _command_line_options
    return _command_line_options


def getopts_builtin(short_option, long_option) -> Any:
    """Built-in getopts function that retrieves command-line options.

    Always takes exactly two arguments:
        getopts("v", "verbose")   — matches -v or --verbose
        getopts(None, "verbose")  — long option only (--verbose)
        getopts("v", None)        — short option only (-v)
        getopts("f:", "file:")    — option expects a value (-f val or --file val)

    A trailing colon ':' indicates the option expects a value argument,
    supporting space-separated syntax: -f config.txt or --file config.txt

    Args:
        short_option: Short option name (without dash), or None to skip.
                      Append ':' to indicate the option expects a value.
        long_option:  Long option name (without dashes), or None to skip.
                      Append ':' to indicate the option expects a value.

    Returns:
        - The option value if it was provided with a value
        - True  if the option was provided as a flag
        - False if the option was not provided at all
    """
    global _command_line_options, _command_line_raw_args

    # Check for ':' suffix indicating value-expected options
    expects_value = False
    if short_option is not None and short_option.endswith(':'):
        short_option = short_option[:-1]
        expects_value = True
    if long_option is not None and long_option.endswith(':'):
        long_option = long_option[:-1]
        expects_value = True

    # First check parsed options (handles = syntax: -f=value, --file=value)
    for name in (short_option, long_option):
        if name is not None and name in _command_line_options:
            value = _command_line_options[name]
            if value is not None:
                return value
            # Option was a flag (no = value) — if it expects a value,
            # scan raw args for the next argument after the flag
            if expects_value:
                for i, arg in enumerate(_command_line_raw_args):
                    if arg == f'-{short_option}' or arg == f'--{long_option}':
                        if i + 1 < len(_command_line_raw_args):
                            return _command_line_raw_args[i + 1]
                return False
            return True

    return False


def disk_builtin(filepath: str) -> Any:
    """Built-in disk function that creates a DskObject for file operations.
    
    Args:
        filepath: Path to the file
        
    Returns:
        DskObject instance
    """
    # Import DskObject here to avoid circular imports
    from lyric.interpreter import DskObject
    
    if not isinstance(filepath, str):
        from lyric.errors import RuntimeErrorLyric
        raise RuntimeErrorLyric(f"disk() expects a string filepath, got {type(filepath).__name__}")
    
    return DskObject(filepath)


def exit_builtin(code: int = 0) -> None:
    """Built-in exit function that terminates the program.
    
    Args:
        code: Exit code (default 0 for success)
    """
    import sys
    
    if not isinstance(code, int):
        from lyric.errors import RuntimeErrorLyric
        raise RuntimeErrorLyric(f"exit() expects an integer exit code, got {type(code).__name__}")
    
    sys.exit(code)


def get_shell_args(command):
    """Build the correct subprocess args for the caller's shell.

    On Windows, subprocess.run(shell=True) always uses cmd.exe.  When Lyric
    is launched from Git Bash (or another Unix-like shell), the SHELL env var
    points to that shell.  We detect this and return args that invoke bash
    directly with ``-c``, so flags like ``mkdir -p`` work as the user expects.

    Returns:
        dict of keyword arguments to pass to subprocess.run().
    """
    import os, sys
    if sys.platform == 'win32':
        shell = os.environ.get('SHELL')
        if shell and os.path.isfile(shell):
            return {'args': [shell, '-c', command], 'shell': False}
    return {'args': command, 'shell': True}


def exec_builtin(command: str) -> int:
    """Built-in exec function that executes a shell command.

    stderr is merged with stdout (stderr=subprocess.STDOUT) so the entirety of
    the command's output is captured together.

    Args:
        command: Shell command to execute

    Returns:
        Exit code of the command (0 for success)
    """
    import subprocess

    if not isinstance(command, str):
        from lyric.errors import RuntimeErrorLyric
        raise RuntimeErrorLyric(f"exec() expects a string command, got {type(command).__name__}")

    try:
        # Execute command and capture output
        # stderr is redirected to stdout as per requirements
        sh = get_shell_args(command)
        result = subprocess.run(
            sh['args'],
            shell=sh['shell'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge stderr into stdout
            text=True
        )
        
        # Store output for potential redirection
        # This will be handled by the interpreter when > operator is used
        global _last_exec_output
        _last_exec_output = result.stdout
        
        return result.returncode
        
    except Exception as e:
        from lyric.errors import RuntimeErrorLyric
        raise RuntimeErrorLyric(f"exec() error: {e}")


# Global storage for last exec output (for > operator)
_last_exec_output = ""


def get_last_exec_output() -> str:
    """Get the output from the last exec() call."""
    global _last_exec_output
    return _last_exec_output


def register_builtins(env: dict) -> None:
    """Register all built-in functions in the given environment."""
    env['print'] = print_builtin
    env['input'] = input_builtin
    env['int'] = int_builtin
    env['flt'] = flt_builtin
    env['str'] = str_builtin
    env['tup'] = tup_builtin
    env['bin'] = bin_builtin
    env['god'] = god_builtin
    env['arr'] = arr_builtin
    env['map'] = map_builtin
    env['disk'] = disk_builtin
    env['range'] = range_builtin
    env['open'] = open_builtin
    env['isinstance'] = isinstance_builtin
    env['type'] = type_builtin
    env['regex'] = regex_builtin
    env['getopts'] = getopts_builtin
    env['exit'] = exit_builtin
    env['exec'] = exec_builtin
    # Note: len(), append(), keys(), values() have been removed as built-ins
    # These are now methods on arr and map objects:
    #   len(myarray) -> myarray.len()
    #   append(myarray, item) -> myarray.append(item)
    #   keys(mydict) -> mydict.keys()
    #   values(mydict) -> mydict.values()

