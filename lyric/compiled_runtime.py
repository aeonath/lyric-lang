# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Runtime support library for the Lyric bytecode compiler.

This module provides helper functions called by compiled Lyric code.
The compiler emits calls to these functions for Lyric-specific semantics
that don't map directly to Python operations.
"""


def lyric_add(left, right):
    """Lyric + operator: auto-coerces to string if either operand is a string."""
    if isinstance(left, str) or isinstance(right, str):
        return str(left) + str(right)
    return left + right


def lyric_mul(left, right):
    """Lyric * operator: supports string repetition."""
    return left * right


def lyric_mod(left, right):
    """Lyric % operator: string format or integer modulus."""
    if isinstance(left, str):
        return left % right
    return left % right


def lyric_div(left, right):
    """Lyric / operator with zero-division check."""
    if right == 0:
        from lyric.errors import RuntimeErrorLyric
        raise RuntimeErrorLyric("Division by zero", 0, 0)
    return left / right


def lyric_floordiv(left, right):
    """Lyric // operator with zero-division check."""
    if right == 0:
        from lyric.errors import RuntimeErrorLyric
        raise RuntimeErrorLyric("Division by zero", 0, 0)
    return left // right


def lyric_print(*args):
    """Lyric print function — mirrors Python print with space separator."""
    print(*args)


def lyric_importpy(module_name):
    """Import a Python module via Lyric's proxy system."""
    from lyric.pyproxy import PyModuleProxy
    return PyModuleProxy(module_name)


# ── Phase 2: Collections and Type System ─────────────────────────

def make_arr(elements):
    """Construct an ArrObject from a Python list."""
    from lyric.interpreter import ArrObject
    return ArrObject(elements)


def make_map(d):
    """Construct a MapObject from a Python dict."""
    from lyric.interpreter import MapObject
    return MapObject(d)


def make_tup(elements):
    """Construct a TupObject from a Python list."""
    from lyric.interpreter import TupObject
    return TupObject(elements)


def typed_assign(type_name, value, var_name):
    """Enforce type on a typed variable declaration.

    Returns the value if type-compatible, raises RuntimeErrorLyric otherwise.
    """
    from lyric.errors import RuntimeErrorLyric
    if not _is_type_compatible(type_name, value):
        raise RuntimeErrorLyric(
            f"Type mismatch: cannot assign {type(value).__name__} to variable "
            f"'{var_name}' declared as {type_name}. "
            f"Use 'var {var_name} = ...' if you need dynamic typing.",
            0, 0
        )
    return value


def _is_type_compatible(expected_type, value):
    """Check if a value is compatible with the expected Lyric type."""
    from lyric.interpreter import ArrObject, MapObject, TupObject, DskObject
    if expected_type == 'var' or expected_type == 'pyobject':
        return True
    if value is None:
        return True
    if expected_type == 'int':
        return isinstance(value, int) and not isinstance(value, bool)
    elif expected_type == 'str':
        return isinstance(value, str)
    elif expected_type == 'flt':
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    elif expected_type == 'god':
        return isinstance(value, bool)
    elif expected_type == 'bin':
        return isinstance(value, bool)
    elif expected_type == 'arr':
        return isinstance(value, (list, ArrObject))
    elif expected_type == 'map':
        return isinstance(value, (dict, MapObject))
    elif expected_type == 'tup':
        return isinstance(value, (tuple, TupObject))
    elif expected_type == 'obj':
        # obj accepts class instances only — not basic types or containers
        return (not isinstance(value, (int, float, str, bool, list, tuple, dict,
                                       ArrObject, MapObject, TupObject, DskObject))
                and hasattr(value, '__class__'))
    elif expected_type == 'dsk':
        return isinstance(value, DskObject)
    elif expected_type == 'rex':
        from lyric.interpreter import RexObject
        return isinstance(value, RexObject)
    return False


# ── Phase 3: Function Type Checking and Builtins ─────────────────

def handle_type_error(exc, func_name):
    """Translate a Python TypeError into a Lyric RuntimeErrorLyric."""
    from lyric.errors import RuntimeErrorLyric
    raise RuntimeErrorLyric(
        f"Type error in '{func_name}': {exc}",
        0, 0
    )


_FAST_TYPE_MAP = {
    'int': int,
    'str': str,
    'flt': (int, float),
    'god': bool,
    'bin': bool,
}


def check_param(type_name, value, param_name):
    """Enforce type on a function parameter.

    Returns the value if type-compatible, raises RuntimeErrorLyric otherwise.
    """
    # Fast path for common types
    if type_name == 'var':
        return value
    if value is None:
        return value
    expected = _FAST_TYPE_MAP.get(type_name)
    if expected is not None:
        if isinstance(value, expected):
            # Exclude bool from int/flt
            if type_name in ('int', 'flt') and isinstance(value, bool):
                pass  # fall through to error
            else:
                return value
    else:
        if _is_type_compatible(type_name, value):
            return value
    from lyric.errors import RuntimeErrorLyric
    raise RuntimeErrorLyric(
        f"Type error: parameter '{param_name}' expects {type_name}, "
        f"got {type(value).__name__}",
        0, 0
    )


def check_return(type_name, value):
    """Enforce type on a function return value.

    Returns the value if type-compatible, raises RuntimeErrorLyric otherwise.
    """
    from lyric.errors import RuntimeErrorLyric
    if not _is_type_compatible(type_name, value):
        raise RuntimeErrorLyric(
            f"Type error: return value does not match declared type. "
            f"Expected {type_name}, but got {type(value).__name__}",
            0, 0
        )
    return value


def make_rex(pattern):
    """Compile a regex pattern and return a RexObject."""
    import re
    from lyric.interpreter import RexObject
    from lyric.errors import RuntimeErrorLyric
    try:
        compiled = re.compile(pattern)
        return RexObject(compiled)
    except re.error as e:
        raise RuntimeErrorLyric(f"Invalid regex pattern '{pattern}': {e}")


# ── Phase 5: Module System ────────────────────────────────────────

def lyric_importpy_selective(module_name, names, env):
    """Selective importpy: importpy math; sin, cos.

    Imports specific names from a Python module into the caller's scope.
    """
    from lyric.pyproxy import PyModuleProxy, PyCallableProxy
    from lyric.errors import RuntimeErrorLyric

    proxy = PyModuleProxy(module_name)
    for name in names:
        try:
            attr = getattr(proxy, name)
        except AttributeError:
            raise RuntimeErrorLyric(
                f"ImportError: cannot import '{name}' from '{module_name}'"
            )
        if callable(attr) and not isinstance(attr, PyCallableProxy):
            attr = PyCallableProxy(attr, f"{module_name}.{name}")
        env[name] = attr


def lyric_import(module_name, source_file, env):
    """Import a Lyric module (.ly file) and bind it in the caller's scope.

    Finds the .ly file, compiles and executes it, then binds the module
    namespace (or individual symbols) into env.
    """
    import os
    from lyric.errors import RuntimeErrorLyric

    parts = module_name.split('.')
    base_name = parts[0]

    if base_name == 'ly':
        raise RuntimeErrorLyric(
            f"ImportError: '{module_name}' is a reserved module name."
        )

    # Determine search paths
    RESERVED_PREFIXES = {'lyric', 'lyrical'}
    is_reserved = base_name in RESERVED_PREFIXES
    lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')

    if is_reserved:
        search_paths = [lib_dir]
    else:
        search_paths = [os.getcwd()]
        if source_file:
            source_dir = os.path.dirname(os.path.abspath(source_file))
            if source_dir not in search_paths:
                search_paths.append(source_dir)
        lyric_path = os.environ.get('LYRIC_PATH', '')
        if lyric_path:
            search_paths.extend(lyric_path.split(os.pathsep))

    # Find the module file
    module_path = module_name.replace('.', os.sep)
    leaf_name = parts[-1]
    module_file = None
    for sp in search_paths:
        candidate = os.path.join(sp, f"{module_path}.ly")
        if os.path.isfile(candidate):
            module_file = candidate
            break
        candidate = os.path.join(sp, module_path, f"{leaf_name}.ly")
        if os.path.isfile(candidate):
            module_file = candidate
            break

    if module_file is None:
        raise RuntimeErrorLyric(
            f"ModuleNotFoundError: No module named '{module_name}'. "
            f"Searched in: {', '.join(search_paths)}"
        )

    # Compile and execute the module
    module_env = _compile_and_exec_module(module_file, module_name, is_reserved)

    # Bind as namespace using the last dotted component
    binding_name = parts[-1] if len(parts) == 1 else None
    if len(parts) == 1:
        env[module_name] = _ModuleNamespace(module_name, module_env)
    else:
        # For dotted imports, build namespace chain
        root_name = parts[0]
        if root_name not in env or not isinstance(env.get(root_name), _ModuleNamespace):
            env[root_name] = _ModuleNamespace(root_name, {})
        current = env[root_name]
        for part in parts[1:-1]:
            if not hasattr(current, part):
                sub = _ModuleNamespace('.'.join(parts[:parts.index(part)+1]), {})
                setattr(current, part, sub)
            current = getattr(current, part)
        setattr(current, parts[-1], _ModuleNamespace(module_name, module_env))


def lyric_import_selective(module_name, symbols, source_file, env):
    """Selective Lyric module import: import lyric.math; sin, cos."""
    import os
    from lyric.errors import RuntimeErrorLyric

    parts = module_name.split('.')
    base_name = parts[0]

    RESERVED_PREFIXES = {'lyric', 'lyrical'}
    is_reserved = base_name in RESERVED_PREFIXES
    lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')

    if is_reserved:
        search_paths = [lib_dir]
    else:
        search_paths = [os.getcwd()]
        if source_file:
            source_dir = os.path.dirname(os.path.abspath(source_file))
            if source_dir not in search_paths:
                search_paths.append(source_dir)

    module_path = module_name.replace('.', os.sep)
    leaf_name = parts[-1]
    module_file = None
    for sp in search_paths:
        candidate = os.path.join(sp, f"{module_path}.ly")
        if os.path.isfile(candidate):
            module_file = candidate
            break
        candidate = os.path.join(sp, module_path, f"{leaf_name}.ly")
        if os.path.isfile(candidate):
            module_file = candidate
            break

    if module_file is None:
        raise RuntimeErrorLyric(
            f"ModuleNotFoundError: No module named '{module_name}'"
        )

    module_env = _compile_and_exec_module(module_file, module_name, is_reserved)

    for symbol_name, alias in symbols:
        target_name = alias if alias else symbol_name
        if symbol_name in module_env:
            env[target_name] = module_env[symbol_name]
        else:
            raise RuntimeErrorLyric(
                f"ImportError: cannot import name '{symbol_name}' from module '{module_name}'"
            )


def _compile_and_exec_module(module_file, module_name, is_stdlib=False):
    """Compile and execute a .ly module file. Returns the module's global namespace."""
    from lyric.lexer import tokenize
    from lyric.parser import Parser
    from lyric.compiler import LyricCompiler
    from lyric.errors import RuntimeErrorLyric

    if is_stdlib:
        from lyric.pyproxy import set_stdlib_mode
        set_stdlib_mode(True)

    try:
        with open(module_file, 'r', encoding='utf-8') as f:
            source = f.read()

        tokens = tokenize(source)
        parser = Parser(tokens)
        module_ast = parser.parse()

        compiler = LyricCompiler(source_file=module_file)
        code_obj = compiler.compile(module_ast)

        module_env = {'__name__': module_name, '__file__': module_file}
        exec(code_obj, module_env)
        return module_env

    except RuntimeErrorLyric:
        raise
    except Exception as e:
        raise RuntimeErrorLyric(f"Error loading module '{module_name}': {e}")
    finally:
        if is_stdlib:
            from lyric.pyproxy import set_stdlib_mode
            set_stdlib_mode(False)


class _ModuleNamespace:
    """Simple namespace for compiled Lyric module imports."""

    def __init__(self, name, env):
        self._name = name
        self._env = env

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        if name in self._env:
            return self._env[name]
        raise AttributeError(
            f"Module '{self._name}' has no attribute '{name}'"
        )

    def __repr__(self):
        return f"<lyric module '{self._name}'>"


# ── Phase 6: Try/Catch/Raise, File Ops, Exec Chains ──────────────

def get_exception_type(type_name):
    """Map a Lyric exception type name to a Python exception class."""
    from lyric.errors import EXCEPTION_TYPES
    cls = EXCEPTION_TYPES.get(type_name)
    if cls is not None:
        return cls
    # Fallback: try standard Python exception names
    builtin_map = {
        'RuntimeError': RuntimeError,
        'IndexError': IndexError,
        'TypeError': TypeError,
        'ValueError': ValueError,
        'KeyError': KeyError,
        'AttributeError': AttributeError,
        'ZeroDivisionError': ZeroDivisionError,
    }
    return builtin_map.get(type_name, Exception)


def lyric_raise(exception_name):
    """Raise a Lyric exception by name."""
    from lyric.errors import RuntimeErrorLyric
    exception_map = {
        'RuntimeErrorLyric': RuntimeErrorLyric,
        'RuntimeError': RuntimeErrorLyric,
        'IndexError': IndexError,
        'TypeError': TypeError,
        'ValueError': ValueError,
        'KeyError': KeyError,
        'AttributeError': AttributeError,
        'ZeroDivisionError': ZeroDivisionError,
    }
    exc_class = exception_map.get(exception_name)
    if exc_class:
        raise exc_class(f"{exception_name} raised")
    else:
        raise RuntimeErrorLyric(f"Unknown exception type: {exception_name}")


def lyric_file_op(operator, left, right):
    """Execute a file I/O operation: ->, ->>, <-."""
    from lyric.interpreter import DskObject
    from lyric.errors import RuntimeErrorLyric

    if operator in ('->', '->>'):
        # Write/append: left is data, right is DskObject
        if isinstance(right, DskObject):
            if isinstance(left, str):
                content = left
            else:
                content = str(left) + '\n'
            if operator == '->>':
                right.append(content)
            else:
                right.overwrite(content)
        else:
            raise RuntimeErrorLyric(
                f"File write operators ({operator}) require dsk type on right side, "
                f"got {type(right).__name__}"
            )
    elif operator == '<-':
        # Read: left is target variable (handled differently at compile level)
        if isinstance(right, DskObject):
            return right.read()
        else:
            raise RuntimeErrorLyric(
                f"File read operator (<-) requires dsk type on right side, "
                f"got {type(right).__name__}"
            )


def lyric_file_read(dsk_obj, current_value):
    """Read from a file. If current_value is an ArrObject, read as lines."""
    from lyric.interpreter import DskObject, ArrObject
    from lyric.errors import RuntimeErrorLyric

    if not isinstance(dsk_obj, DskObject):
        raise RuntimeErrorLyric(
            f"File read operator (<-) requires dsk type on right side, got {type(dsk_obj).__name__}"
        )
    content = dsk_obj.read()
    # If the target variable is an arr type, split into lines
    if isinstance(current_value, ArrObject) or isinstance(current_value, list):
        lines = content.splitlines()
        return ArrObject(lines)
    return content


def lyric_print_to_file(operator, args, dsk_obj):
    """Handle print -> file or print ->> file (write print output to file, not stdout)."""
    from lyric.interpreter import DskObject
    from lyric.errors import RuntimeErrorLyric

    if not isinstance(dsk_obj, DskObject):
        raise RuntimeErrorLyric(
            f"File write operators ({operator}) require dsk type on right side, "
            f"got {type(dsk_obj).__name__}"
        )
    content = ' '.join(str(a) for a in args) + '\n'
    if operator == '->>':
        dsk_obj.append(content)
    else:
        dsk_obj.overwrite(content)


def lyric_exec_capture(command):
    """Execute a command and return its stdout+stderr as a string."""
    import subprocess
    from lyric.runtime import get_shell_args
    from lyric.errors import RuntimeErrorLyric

    if not isinstance(command, str):
        raise RuntimeErrorLyric(f"exec() expects a string command, got {type(command).__name__}")

    try:
        sh = get_shell_args(command)
        result = subprocess.run(
            sh['args'], shell=sh['shell'],
            capture_output=True, text=True
        )
        return result.stdout + result.stderr
    except Exception as e:
        raise RuntimeErrorLyric(f"exec() error: {e}")


def lyric_exec_to_file(operator, command, dsk_obj):
    """Execute a command and write/append output to a file."""
    from lyric.interpreter import DskObject
    from lyric.errors import RuntimeErrorLyric

    output = lyric_exec_capture(command)
    if not isinstance(dsk_obj, DskObject):
        raise RuntimeErrorLyric(
            f"File write operators ({operator}) require dsk type on right side"
        )
    if operator == '->>':
        dsk_obj.append(output)
    else:
        dsk_obj.overwrite(output)


def lyric_exec_with_input(command, input_data):
    """Execute a command with input piped as stdin."""
    import subprocess
    from lyric.runtime import get_shell_args

    sh = get_shell_args(command)
    result = subprocess.run(
        sh['args'], shell=sh['shell'],
        input=str(input_data),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    # Print output to stdout (like the interpreter does)
    if result.stdout:
        print(result.stdout, end='')
    return result.returncode


def lyric_exec_chain(elements, operators, input_source, output_target):
    """Execute an exec chain with pipe operators (|, &&, ||).

    Elements are command strings (extracted from exec() calls by the compiler).
    stderr is merged with stdout for each command in the chain.
    """
    import subprocess
    from lyric.runtime import get_shell_args
    from lyric.errors import RuntimeErrorLyric

    current_output = ""
    if input_source is not None:
        current_output = str(input_source)

    exit_code = 0
    for i, element in enumerate(elements):
        # Check short-circuit from previous operator
        if i > 0:
            prev_op = operators[i - 1]
            if prev_op == '&&' and exit_code != 0:
                break
            elif prev_op == '||' and exit_code == 0:
                break

        has_input = i > 0 or input_source is not None

        # Handle print in chain — print the piped input
        if element == '__print__':
            if has_input and current_output:
                print(current_output, end='')
            continue

        command = str(element)

        try:
            sh = get_shell_args(command)
            result = subprocess.run(
                sh['args'],
                shell=sh['shell'],
                input=current_output if has_input else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            exit_code = result.returncode
            current_output = result.stdout
        except Exception as e:
            raise RuntimeErrorLyric(f"exec() error in chain: {e}")

    # Handle output target
    if output_target is not None and output_target is not False:
        return current_output

    return exit_code


def lyric_exec_chain_to_file(operator, chain_output, dsk_obj):
    """Write exec chain output to a file."""
    from lyric.interpreter import DskObject
    from lyric.errors import RuntimeErrorLyric

    # chain_output is the string result from lyric_exec_chain
    if not isinstance(dsk_obj, DskObject):
        raise RuntimeErrorLyric(
            f"File write operators ({operator}) require dsk type on right side"
        )
    content = str(chain_output)
    if operator == '->>':
        dsk_obj.append(content)
    else:
        dsk_obj.overwrite(content)


def call_main(main_func):
    """Call main() with argc/argv from sys.argv, matching interpreter behavior.

    Uses the same option parsing as the CLI to separate options from arguments.
    Options (starting with - or --) are filtered out; only positional args remain.
    """
    import sys
    import inspect
    from lyric.interpreter import ArrObject

    params = inspect.signature(main_func).parameters
    param_count = len(params)

    # Collect CLI args (everything after the .ly file)
    cli_args = []
    argv = sys.argv
    found_ly = False
    for i, arg in enumerate(argv):
        if arg.endswith('.ly'):
            found_ly = True
            # Parse remaining args — filter out options
            for a in argv[i+1:]:
                if a.startswith('-'):
                    continue  # Skip options
                cli_args.append(a)
            break

    if param_count >= 2:
        main_func(len(cli_args), ArrObject(cli_args))
    elif param_count == 1:
        main_func(len(cli_args))
    else:
        main_func()


def resolve_index_key(key_str, local_vars, global_vars):
    """Resolve an index key from an AssignNode name.

    The parser strips quotes from keys, so 'person[name]' could mean
    person["name"] (string key) or person[name] (variable key).
    Check if key_str is a variable name in scope; if so, use its value.
    Otherwise, treat it as a string literal.
    """
    if key_str in local_vars:
        return local_vars[key_str]
    if key_str in global_vars:
        return global_vars[key_str]
    # Not a variable — treat as string key
    return key_str


def register_builtins(env):
    """Register all Lyric builtin functions into the compiled code's namespace."""
    from lyric.runtime import (
        int_builtin, flt_builtin, str_builtin, bin_builtin, god_builtin,
        arr_builtin, map_builtin, tup_builtin, regex_builtin,
        isinstance_builtin, type_builtin, input_builtin,
        disk_builtin, exit_builtin, exec_builtin, getopts_builtin,
    )
    env['int'] = int_builtin
    env['flt'] = flt_builtin
    env['str'] = str_builtin
    env['bin'] = bin_builtin
    env['god'] = god_builtin
    env['arr'] = arr_builtin
    env['map'] = map_builtin
    env['tup'] = tup_builtin
    env['regex'] = regex_builtin
    env['isinstance'] = isinstance_builtin
    env['type'] = type_builtin
    env['input'] = input_builtin
    env['disk'] = disk_builtin
    env['exit'] = exit_builtin
    env['exec'] = exec_builtin
    env['getopts'] = getopts_builtin
