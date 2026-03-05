# Type Tests for Sprint 3
# Tests type declarations, type enforcement, and type compatibility

# Test 1: Basic type declarations
int x = 42
str name = "Alice"
flt pi = 3.14159
var dynamic = "anything"

# Test 2: Type enforcement - should work
int count = 100
str greeting = "Hello"
flt rate = 0.15

# Test 3: Type enforcement - should fail (commented out for pytest)
# int invalid = "hello"  # This should cause a type error
# str invalid2 = 42      # This should cause a type error
# flt invalid3 = "pi"   # This should cause a type error

# Test 4: var type accepts anything
var anything1 = 42
var anything2 = "hello"
var anything3 = 3.14
var anything4 = True

# Test 5: Type compatibility with built-in functions
var result1 = int("42")
var result2 = str(42)
var result3 = flt("3.14")

# Test 6: Type checking with isinstance
var is_int = isinstance(42, int)
var is_str = isinstance("hello", str)
var is_flt = isinstance(3.14, flt)

# Test 7: Type checking with type() function
var type_name1 = type(42)
var type_name2 = type("hello")
var type_name3 = type(3.14)
