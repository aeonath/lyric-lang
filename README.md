# Lyric

Lyric is an experimental interpreted programming language built in Python. It features optional type declarations enforced at runtime, a classical hand-written interpreter pipeline (lexer → parser → AST → tree-walker), and Python interoperability via `importpy`.

**Current version:** 1.0.3 (Alpha)  
**Website:** [lyric-lang.org](https://lyric-lang.org)  

## Install

From PyPI:

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

This is a classic interperter with a lexer, a parser, and AST.

```
lyric/
├── lexer.py          # Single-pass tokenizer
├── parser.py         # Recursive descent parser → AST
├── ast_nodes.py      # AST node definitions
├── interpreter.py    # Tree-walking executor with lexical scoping
├── runtime.py        # Built-in functions and type coercions
├── pyproxy.py        # importpy bridge to Python packages
├── errors.py         # Error types with source positions
└── cli.py            # CLI entry point
```

## Development

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

Tests are organized under `lyric/tests/` by version milestone.

## Contributing

Contributions are welcome. Please open an issue before submitting large changes so we can discuss the approach.

## License

Copyright (c) 2026 MiraNova Studios. Licensed under the [GNU General Public License v3.0](LICENSE).
