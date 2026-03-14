# Lyric

Lyric is an experimental programming language built in Python, designed for clarity and expressive syntax. As of version 1.1.1, Lyric is a **transpiler** — source code is compiled to Python AST and executed as CPython bytecode, delivering near-native Python performance. Type declarations are optional and enforced at runtime — variables declared with a type (`int`, `str`, `flt`, etc.) are strongly checked on assignment, while `var` opts into dynamic typing. It is developed and maintained by **MiraNova Studios**.

**Current version:** 1.1.1 (Alpha)
**Website:** [lyric-lang.org](https://lyric-lang.org)

## Install

From PyPI:

### Debian/Ubuntu

```bash
./build-deb.sh
sudo dpkg -i dist/lyric-lang_1.1.1_all.deb
```

### pip

```bash
pip install lyric-lang
```

From source:

```bash
git clone https://github.com/miranova-studios/lyric-lang.git
cd lyric-lang
pip install -e .
```

Requires **Python 3.10+**.

## Usage

```bash
lyric program.ly          # run a file
lyric run program.ly      # same thing

lyric -i                  # interactive REPL
lyric> print "hello world"
```

Lyric programs use the `.ly` extension. Execution starts in `main()`:

```
def main() {
    str name = "world"
    print "hello, " + name
}
```

Shebang lines (`#!/usr/bin/env lyric`) are supported.

## Quick Tour

```lyric
# Functions with typed parameters
def greet(str name) {
    print "hello, " + name
}

def main() {
    greet("world")

    # Typed and untyped variables
    int count = 10
    str label = "items"
    var anything = [1, "two", 3.0]

    # Control flow
    if count > 5
        print "many " + label
    end

    for int i in range(count)
        print i
    done

    # Exception handling
    try:
        int result = int("not a number")
    catch ValueError as e :
        print "caught: " + str(e)
    fade
}
```

See the [tutorial](https://lyric-lang.org/tutorial.html) for getting started.

See the [language specification](https://lyric-lang.org/specification.html) for the full syntax reference.

## Architecture

Lyric uses a transpiler pipeline: source text flows through the lexer and parser to produce a Lyric AST, which is then compiled to a Python AST and executed as CPython bytecode. A tree-walking interpreter is preserved as a fallback via `--interpret`. All stages are implemented from scratch in pure Python with no parser-generator dependencies.

```
Source (.ly) → Lexer → Parser → Lyric AST → Compiler → Python AST → CPython bytecode → Execution
```

```
lyric/
├── lexer.py              # Tokenizer — converts source text into a token stream
├── parser.py             # Recursive descent parser — produces a Lyric AST
├── ast_nodes.py          # AST node definitions
├── compiler.py           # Transpiler — compiles Lyric AST to Python AST
├── compiled_runtime.py   # Runtime support library for compiled code
├── interpreter.py        # Tree-walking interpreter (fallback via --interpret)
├── runtime.py            # Built-in functions and type coercions
├── pyproxy.py            # Python interoperability layer (importpy bridge)
├── errors.py             # Lexer, parser, and runtime error types
└── cli.py                # Command-line interface
```

### Compiler (Transpiler)

The compiler walks the Lyric AST and emits Python `ast` module nodes. Python's built-in `compile()` converts these to bytecode, and `exec()` runs them on CPython's C-level VM. This gives Lyric near-native Python performance — the full benchmark runs in ~5 seconds compiled vs ~74 seconds interpreted (14x speedup).

The compiler handles all Lyric constructs: expressions, control flow, functions, classes with inheritance, module imports, file I/O, exec chains, try/catch/finally, and the full type system. Type errors in compiled functions are caught by a zero-overhead try/except wrapper that translates Python TypeErrors into Lyric error messages.

### Lexer

The lexer performs single-pass tokenization with support for string literals (single and double quotes), regex literals (`/pattern/flags`), shebang lines, and inline comments (`#`). Tokens carry line and column positions used for error reporting.

### Parser

The parser is a hand-written recursive descent parser that produces a typed AST. It handles operator precedence, optional colon syntax across all control structures, and both `given`/`done` and `for`/`end` loop forms. The parser enforces top-level restrictions (e.g. bare expressions outside functions are rejected).

### Interpreter (Fallback)

The tree-walking interpreter is preserved as a fallback via `--interpret`. It walks the AST directly with scope managed via a linked chain of environment frames. This is primarily useful for the REPL (`lyric -i`) and debugging.

### Type System

Lyric uses optional type declarations enforced at runtime. Variables declared with a specific type are strongly checked on every assignment and function call; `var` disables enforcement for that binding. The core types are:

| Type  | Description |
|-------|-------------|
| `int` | Integer |
| `flt` | Float |
| `str` | String |
| `var` | Dynamic (no enforcement) |
| `god` | Boolean (honoring Kurt Godel) |
| `bin` | Boolean (alternative form) |
| `rex` | Regular expression literal (`/pattern/`) |
| `arr` | Array (ordered collection) |
| `map` | Dictionary / key-value map |
| `tup` | Tuple (immutable) |
| `obj` | Generic object reference |
| `dsk` | Disk / file handle type |

Type coercion is available via casting functions (`int()`, `str()`, `flt()`, etc.). The `var` type opts out of enforcement for dynamic use cases.

### Classes and Inheritance

Classes are defined with `class Name` syntax (terminated by `+++`). Constructors are methods named after the class. Single inheritance uses `based on`. Method resolution follows the inheritance chain.

```
class Animal
    var name
    def Animal(str name) {
        self.name = name
    }
    def speak() {
        return self.name + " speaks"
    }
+++

class Dog based on Animal
    var breed
    def Dog(str name, str breed) {
        self.name = name
        self.breed = breed
    }
    def speak() {
        return self.name + " barks"
    }
+++
```

### Python Interoperability

The `importpy` keyword loads any installed Python package through `pyproxy.py`, which wraps Python objects for use inside the Lyric runtime. Return values are translated back to Lyric types where possible. This layer is intentionally kept separate from native `import`, which resolves Lyric modules.

### Error Reporting

All errors (lexer, parser, runtime) carry source position information. Error messages include file name, line number, and a description of the issue.

---

## Execution Modes

| Mode | Command | Description |
|------|---------|-------------|
| **Compiled** (default) | `lyric program.ly` | Transpiles to Python AST, executes as CPython bytecode |
| **Interpreted** | `lyric program.ly --interpret` | Tree-walking interpreter (slower, full compatibility) |
| **REPL** | `lyric -i` | Interactive mode (uses interpreter) |
| **AST Dump** | `lyric program.ly --dump-ast` | Print generated Python AST and exit (debugging) |

---

## Language Features

- Typed variable declarations: `int x = 5`, `str name = "lyric"`, `var x = anything`
- Functions with typed parameters: `def greet(str name, int age) { ... }`
- Classes with constructors, inheritance (`based on`), and method dispatch
- Control flow: `if`/`elif`/`else`, `given`/`done` loops, `break`/`continue`
- Exception handling: `try`/`catch`/`finally`/`fade` with typed exception binding
- Regular expressions as first-class values with `rex` type and `/pattern/` literals
- `importpy` for Python library access; native `import` for Lyric modules
- `exec()` with I/O redirection and pipe chains (`|`, `&&`, `||`)
- File I/O via `dsk` type with `->` (write), `->>` (append), `<-` (read) operators
- `getopts` for CLI argument parsing within scripts
- Standard library (`import lyric`) with filesystem, datetime, and random utilities

See the [language specification](https://lyric-lang.org) for full syntax reference.

---

## Module System

Lyric supports two import mechanisms. Native Lyric modules (`import name`) are resolved by searching the current directory, source file directory, and `LYRIC_PATH`. The standard library (`import lyric`, `import lyric.math`) resolves from the built-in `lib/` directory. Python packages (`importpy name`) are loaded through the `pyproxy` bridge. Resolution order is: native Lyric module → built-in standard library → Python bridge → `ModuleNotFoundError`.

---

## Performance

Lyric 1.1.1 compiles to CPython bytecode, achieving near-native Python performance:

| Mode | Benchmark Time | vs Interpreted |
|------|---------------|----------------|
| Compiled (default) | ~5s | 14x faster |
| Interpreted | ~74s | baseline |
| Python (native) | ~1.2s | reference |
| Ruby (native) | ~1.1s | reference |
| Perl (native) | ~3.0s | reference |

Benchmark: 10M function calls + 1M counting loop + 10M arithmetic operations.

---

## Development

Requires Python 3.10 or newer.

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run the full test suite
python -m pytest lyric/tests/ --tb=short -q

# Run tests for a specific version milestone
pytest lyric/tests/core-0.8.0/ -q

# Lint
flake8 lyric/
```

Tests are organized under `lyric/tests/` by version milestone (e.g. `core-0.8.0/`, `core-1.1.x/`). Run the full suite with `pytest` from the project root.

### Building the Debian Package

```bash
./build-deb.sh
sudo dpkg -i dist/lyric-lang_1.1.1_all.deb
```

## Contributing

Contributions are welcome. Please open an issue before submitting large changes so we can discuss the approach.

## License

Licensed under the MiraNova Software License. See the `LICENSE` file for full terms. All rights reserved — 2025-2026 MiraNova Studios.
