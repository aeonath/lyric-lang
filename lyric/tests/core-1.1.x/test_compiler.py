# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Comprehensive unit tests for the Lyric bytecode compiler (transpiler).

Tests cover all 6 phases of the compiler, verifying that compiled output
matches the interpreter's output for every supported language construct.
"""

import pytest
import tempfile
import os
from lyric.parser import parse
from lyric.compiler import LyricCompiler, compile_lyric
from lyric.interpreter import evaluate, Interpreter


def _run_compiled(source, interactive=True):
    """Compile and execute Lyric source, capturing stdout."""
    import io, sys
    ast = parse(source, interactive=interactive)
    code_obj = compile_lyric(ast, source_file='<test>')
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(code_obj, {'__name__': '__main__', '__file__': '<test>'})
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def _run_interpreted(source, interactive=True):
    """Interpret Lyric source, capturing stdout."""
    import io, sys
    ast = parse(source, interactive=interactive)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        evaluate(ast)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def _assert_same_output(source, interactive=True):
    """Assert that compiled and interpreted output match."""
    compiled = _run_compiled(source, interactive)
    interpreted = _run_interpreted(source, interactive)
    assert compiled == interpreted, (
        f"Output mismatch!\nCompiled:    {compiled!r}\nInterpreted: {interpreted!r}"
    )
    return compiled


# ═══════════════════════════════════════════════════════════════════
# Phase 1: Core Expressions and Statements
# ═══════════════════════════════════════════════════════════════════

class TestPhase1Literals:
    def test_integer_literal(self):
        out = _assert_same_output('def main() { print(42) }')
        assert '42' in out

    def test_float_literal(self):
        out = _assert_same_output('def main() { print(3.14) }')
        assert '3.14' in out

    def test_string_literal(self):
        out = _assert_same_output('def main() { print("hello") }')
        assert 'hello' in out

    def test_boolean_true(self):
        out = _assert_same_output('def main() { print(true) }')
        assert 'True' in out

    def test_boolean_false(self):
        out = _assert_same_output('def main() { print(false) }')
        assert 'False' in out

    def test_none_literal(self):
        out = _assert_same_output('def main() { print(None) }')
        assert 'None' in out


class TestPhase1Arithmetic:
    def test_addition(self):
        out = _assert_same_output('def main() { print(2 + 3) }')
        assert '5' in out

    def test_subtraction(self):
        out = _assert_same_output('def main() { print(10 - 4) }')
        assert '6' in out

    def test_multiplication(self):
        out = _assert_same_output('def main() { print(6 * 7) }')
        assert '42' in out

    def test_division(self):
        out = _assert_same_output('def main() { print(10 / 4) }')
        assert '2.5' in out

    def test_floor_division(self):
        out = _assert_same_output('''
importpy math
def main() { print(math.floor(10 / 3)) }''')
        assert '3' in out

    def test_modulo(self):
        out = _assert_same_output('def main() { print(10 % 3) }')
        assert '1' in out

    def test_power(self):
        out = _assert_same_output('''
importpy math
def main() { print(math.pow(2, 10)) }''')
        assert '1024' in out

    def test_string_concat(self):
        out = _assert_same_output('def main() { print("hello" + " " + "world") }')
        assert 'hello world' in out

    def test_string_int_concat(self):
        out = _assert_same_output('def main() { print("count: " + 42) }')
        assert 'count: 42' in out

    def test_string_repeat(self):
        out = _assert_same_output('def main() { print("ab" * 3) }')
        assert 'ababab' in out

    def test_unary_minus(self):
        out = _assert_same_output('def main() { print(-5) }')
        assert '-5' in out

    def test_unary_not(self):
        out = _assert_same_output('def main() { print(not true) }')
        assert 'False' in out


class TestPhase1Comparison:
    def test_less_than(self):
        out = _assert_same_output('def main() { print(3 < 5) }')
        assert 'True' in out

    def test_greater_equal(self):
        out = _assert_same_output('def main() { print(5 >= 5) }')
        assert 'True' in out

    def test_equality(self):
        out = _assert_same_output('def main() { print(42 == 42) }')
        assert 'True' in out

    def test_inequality(self):
        out = _assert_same_output('def main() { print(1 != 2) }')
        assert 'True' in out

    def test_and_operator(self):
        out = _assert_same_output('def main() { print(true and false) }')
        assert 'False' in out

    def test_or_operator(self):
        out = _assert_same_output('def main() { print(false or true) }')
        assert 'True' in out


class TestPhase1Variables:
    def test_var_declaration(self):
        out = _assert_same_output('def main() { var x = 10\nprint(x) }')
        assert '10' in out

    def test_var_reassignment(self):
        out = _assert_same_output('def main() { var x = 1\nx = 2\nprint(x) }')
        assert '2' in out

    def test_multiple_vars(self):
        out = _assert_same_output('''
def main() {
    var a = 1
    var b = 2
    var c = a + b
    print(c)
}''')
        assert '3' in out


class TestPhase1ControlFlow:
    def test_if_true(self):
        out = _assert_same_output('''
def main() {
    if 1 > 0:
        print("yes")
    end
}''')
        assert 'yes' in out

    def test_if_false(self):
        out = _assert_same_output('''
def main() {
    if 1 > 2:
        print("yes")
    else:
        print("no")
    end
}''')
        assert 'no' in out

    def test_elif(self):
        out = _assert_same_output('''
def main() {
    var x = 2
    if x == 1:
        print("one")
    elif x == 2:
        print("two")
    else:
        print("other")
    end
}''')
        assert 'two' in out

    def test_while_loop(self):
        out = _assert_same_output('''
def main() {
    var i = 0
    given i < 3:
        print(i)
        i = i + 1
    done
}''')
        assert '0\n1\n2\n' in out

    def test_for_loop(self):
        out = _assert_same_output('''
def main() {
    given var i in range(4):
        print(i)
    done
}''')
        assert '0\n1\n2\n3\n' in out

    def test_break(self):
        out = _assert_same_output('''
def main() {
    var i = 0
    given i < 10:
        if i == 3:
            break
        end
        print(i)
        i = i + 1
    done
}''')
        assert '0\n1\n2\n' in out

    def test_continue(self):
        out = _assert_same_output('''
def main() {
    given var i in range(5):
        if i == 2:
            continue
        end
        print(i)
    done
}''')
        output = out.strip().split('\n')
        assert '2' not in output


class TestPhase1Functions:
    def test_basic_function(self):
        out = _assert_same_output('''
def greet() {
    return "hello"
}
def main() {
    print(greet())
}''')
        assert 'hello' in out

    def test_function_with_params(self):
        out = _assert_same_output('''
def add(var a, var b) {
    return a + b
}
def main() {
    print(add(3, 4))
}''')
        assert '7' in out

    def test_nested_function_call(self):
        out = _assert_same_output('''
def double(var n) {
    return n * 2
}
def quadruple(var n) {
    return double(double(n))
}
def main() {
    print(quadruple(5))
}''')
        assert '20' in out

    def test_function_no_return(self):
        out = _assert_same_output('''
def say_hi() {
    print("hi")
}
def main() {
    say_hi()
}''')
        assert 'hi' in out

    def test_print_multiple_args(self):
        out = _assert_same_output('def main() { print("a", "b", "c") }')
        assert 'a b c' in out


class TestPhase1ImportPy:
    def test_importpy_time(self):
        out = _run_compiled('''
importpy time
def main() {
    var t = time.time()
    print(type(t))
}''')
        # time.time() returns float
        assert 'float' in out or 'flt' in out


# ═══════════════════════════════════════════════════════════════════
# Phase 2: Collections, Strings, and Type System
# ═══════════════════════════════════════════════════════════════════

class TestPhase2Collections:
    def test_list_literal(self):
        out = _assert_same_output('def main() { arr x = [1, 2, 3]\nprint(x) }')
        assert '[1, 2, 3]' in out

    def test_dict_literal(self):
        out = _assert_same_output('def main() { map m = {"a": 1}\nprint(m["a"]) }')
        assert '1' in out

    def test_tuple_literal(self):
        out = _assert_same_output('def main() { tup t = (10, 20)\nprint(t) }')
        assert '(10, 20)' in out

    def test_list_index(self):
        out = _assert_same_output('def main() { arr x = [10, 20, 30]\nprint(x[1]) }')
        assert '20' in out

    def test_dict_access(self):
        out = _assert_same_output('''
def main() {
    map m = {"name": "Lyric", "ver": "1.0"}
    print(m["name"])
}''')
        assert 'Lyric' in out

    def test_slice(self):
        out = _assert_same_output('def main() { arr x = [1, 2, 3, 4, 5]\nprint(x[1:3]) }')
        assert '[2, 3]' in out

    def test_in_operator_list(self):
        out = _assert_same_output('def main() { arr x = [1, 2, 3]\nprint(2 in x) }')
        assert 'True' in out

    def test_in_operator_map(self):
        out = _assert_same_output('def main() { map m = {"a": 1}\nprint("a" in m) }')
        assert 'True' in out

    def test_in_operator_false(self):
        out = _assert_same_output('def main() { arr x = [1, 2, 3]\nprint(9 in x) }')
        assert 'False' in out


class TestPhase2TypeSystem:
    def test_typed_int(self):
        out = _assert_same_output('def main() { int x = 42\nprint(x) }')
        assert '42' in out

    def test_typed_str(self):
        out = _assert_same_output('def main() { str s = "hello"\nprint(s) }')
        assert 'hello' in out

    def test_typed_flt(self):
        out = _assert_same_output('def main() { flt f = 3.14\nprint(f) }')
        assert '3.14' in out

    def test_type_mismatch_raises(self):
        with pytest.raises(Exception):
            _run_compiled('def main() { int x = "not an int" }')

    def test_var_accepts_any(self):
        out = _assert_same_output('''
def main() {
    var x = 42
    x = "now a string"
    print(x)
}''')
        assert 'now a string' in out


# ═══════════════════════════════════════════════════════════════════
# Phase 3: Functions with Type Checking and Builtins
# ═══════════════════════════════════════════════════════════════════

class TestPhase3TypeChecking:
    def test_typed_params_valid(self):
        out = _assert_same_output('''
def add(int a, int b) {
    return a + b
}
def main() {
    print(add(3, 4))
}''')
        assert '7' in out

    def test_typed_params_type_error(self):
        """Type error caught by try/except wrapper in compiled function."""
        out = _run_compiled('''
def divide(int a, int b) {
    return a / b
}
def main() {
    try:
        divide("x", "y")
    catch:
        print("type error caught")
    fade
}''')
        assert 'type error caught' in out


class TestPhase3Builtins:
    def test_int_conversion(self):
        out = _assert_same_output('def main() { print(int("42")) }')
        assert '42' in out

    def test_flt_conversion(self):
        out = _assert_same_output('def main() { print(flt(10)) }')
        assert '10.0' in out

    def test_str_conversion(self):
        out = _assert_same_output('def main() { print(str(123)) }')
        assert '123' in out

    def test_bin_conversion(self):
        out = _assert_same_output('def main() { print(bin(1)) }')
        assert 'True' in out

    def test_god_conversion(self):
        out = _assert_same_output('def main() { print(god(0)) }')
        assert 'False' in out

    def test_type_builtin(self):
        out = _assert_same_output('def main() { print(type(42)) }')
        assert 'int' in out

    def test_isinstance_builtin(self):
        out = _assert_same_output('def main() { print(isinstance(42, "int")) }')
        assert 'True' in out

    def test_regex_builtin(self):
        out = _assert_same_output('def main() { var r = regex("hello")\nprint(r) }')
        assert 'RexObject' in out

    def test_range_in_loop(self):
        out = _assert_same_output('''
def main() {
    var s = 0
    given var i in range(5):
        s = s + i
    done
    print(s)
}''')
        assert '10' in out


# ═══════════════════════════════════════════════════════════════════
# Phase 4: Classes and Inheritance
# ═══════════════════════════════════════════════════════════════════

class TestPhase4Classes:
    def test_basic_class(self):
        out = _run_compiled('''
class Greeter
    var msg
    def Greeter(str msg) {
        self.msg = msg
    }
    def greet() {
        return self.msg
    }
+++
def main() {
    var g = Greeter("hi")
    print(g.greet())
}''')
        assert 'hi' in out

    def test_class_member_access(self):
        out = _run_compiled('''
class Point
    var x
    var y
    def Point(var x, var y) {
        self.x = x
        self.y = y
    }
+++
def main() {
    var p = Point(3, 4)
    print(p.x, p.y)
}''')
        assert '3 4' in out

    def test_class_methods(self):
        out = _run_compiled('''
class Counter
    var count
    def Counter() {
        self.count = 0
    }
    def increment() {
        self.count = self.count + 1
    }
    def get() {
        return self.count
    }
+++
def main() {
    var c = Counter()
    c.increment()
    c.increment()
    c.increment()
    print(c.get())
}''')
        assert '3' in out

    def test_inheritance(self):
        out = _run_compiled('''
class Animal
    var name
    def Animal(var name) {
        self.name = name
    }
    def info() {
        return self.name
    }
+++
class Dog based on Animal
    var breed
    def Dog(var name, var breed) {
        self.name = name
        self.breed = breed
    }
    def bark() {
        return self.name + " barks"
    }
+++
def main() {
    var d = Dog("Rex", "Shepherd")
    print(d.bark())
    print(d.info())
}''')
        assert 'Rex barks' in out
        assert 'Rex' in out

    def test_isinstance_with_inheritance(self):
        out = _run_compiled('''
class Base
    def Base() {
        self.x = 1
    }
+++
class Child based on Base
    def Child() {
        self.x = 2
    }
+++
def main() {
    var c = Child()
    print(isinstance(c, Child))
    print(isinstance(c, Base))
}''')
        assert 'True\nTrue\n' in out


# ═══════════════════════════════════════════════════════════════════
# Phase 5: Module System and Imports
# ═══════════════════════════════════════════════════════════════════

class TestPhase5Imports:
    def test_importpy_whole_module(self):
        out = _run_compiled('''
importpy math
def main() {
    print(math.floor(3.7))
}''')
        assert '3' in out

    def test_importpy_selective(self):
        out = _run_compiled('''
importpy json; dumps, loads
def main() {
    var s = dumps({"a": 1})
    var d = loads(s)
    print(d["a"])
}''')
        assert '1' in out

    def test_lyric_stdlib_import(self):
        out = _run_compiled('''
import lyric
def main() {
    var e = lyric.exists("/tmp")
    print(e)
}''')
        assert 'True' in out

    def test_user_module_import(self):
        """Test importing a user-defined .ly module."""
        # Create module in cwd so import resolution finds it
        mod_name = '_lyric_test_mod_tmp'
        mod_file = os.path.join(os.getcwd(), f'{mod_name}.ly')
        with open(mod_file, 'w') as f:
            f.write('def double(var n) { return n * 2 }\n')

        try:
            out = _run_compiled(f'''
import {mod_name}
def main() {{
    print({mod_name}.double(21))
}}''')
            assert '42' in out
        finally:
            os.unlink(mod_file)


# ═══════════════════════════════════════════════════════════════════
# Phase 6: I/O, Exec, and Edge Cases
# ═══════════════════════════════════════════════════════════════════

class TestPhase6TryCatch:
    def test_try_catch_basic(self):
        out = _assert_same_output('''
def main() {
    try:
        var x = 10 / 0
    catch:
        print("caught")
    fade
}''')
        assert 'caught' in out

    def test_try_finally(self):
        out = _assert_same_output('''
def main() {
    try:
        print("try")
    catch:
        print("catch")
    finally:
        print("finally")
    fade
}''')
        assert 'try' in out
        assert 'finally' in out
        assert 'catch' not in out

    def test_try_catch_finally(self):
        out = _assert_same_output('''
def main() {
    try:
        var x = int("bad")
    catch:
        print("caught")
    finally:
        print("done")
    fade
}''')
        assert 'caught' in out
        assert 'done' in out

    def test_raise(self):
        out = _assert_same_output('''
def main() {
    try:
        raise RuntimeError
    catch:
        print("raised and caught")
    fade
}''')
        assert 'raised and caught' in out


class TestPhase6FileOps:
    def test_write_and_read(self):
        out = _run_compiled('''
def main() {
    var f = disk("/tmp/lyric_compiler_test.txt")
    "hello" -> f
    f.close()
    var r = disk("/tmp/lyric_compiler_test.txt")
    print(r.read())
    r.close()
}''')
        assert 'hello' in out
        os.unlink('/tmp/lyric_compiler_test.txt')

    def test_append(self):
        out = _run_compiled('''
def main() {
    var f = disk("/tmp/lyric_compiler_test2.txt")
    "line1" -> f
    "line2" ->> f
    f.close()
    var r = disk("/tmp/lyric_compiler_test2.txt")
    print(r.read())
    r.close()
}''')
        assert 'line1' in out
        assert 'line2' in out
        os.unlink('/tmp/lyric_compiler_test2.txt')


# ═══════════════════════════════════════════════════════════════════
# Regression: Benchmark Correctness
# ═══════════════════════════════════════════════════════════════════

class TestBenchmarkCorrectness:
    def test_small_benchmark_output_matches(self):
        """The small benchmark must produce identical output in both modes."""
        benchmark_path = os.path.join(
            os.path.dirname(__file__), '..', 'perftest', 'lyric_benchmark_small.ly'
        )
        if not os.path.exists(benchmark_path):
            pytest.skip("Benchmark file not found")

        with open(benchmark_path, 'r') as f:
            source = f.read()

        # Remove shebang
        if source.startswith('#!'):
            source = '\n'.join(source.split('\n')[1:])

        compiled = _run_compiled(source, interactive=False)
        interpreted = _run_interpreted(source, interactive=False)

        # Compare line by line, skipping the timing line
        compiled_lines = [l for l in compiled.strip().split('\n') if 'Execution time' not in l]
        interp_lines = [l for l in interpreted.strip().split('\n') if 'Execution time' not in l]
        assert compiled_lines == interp_lines
