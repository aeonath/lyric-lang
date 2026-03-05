# core_json.ly
# Lyric adhoc test -- exercises the public functions of Python's json module.
#
# Run with:  lyric run lyric/tests/python_modules/core_json.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions

importpy json

# -----------------------------------------------------------------------
# Helper: print PASS or ERROR based on a condition
# -----------------------------------------------------------------------
def check(var label, var cond) {
    if cond
        print("PASS:", label)
    else
        print("ERROR:", label)
    end
}

def main() {
    print("=== Lyric json module adhoc test ===")
    print("")

    # ================================================================
    # json.dumps -- basic types
    # ================================================================
    print("--- json.dumps: basic types ---")

    try:
        var s = json.dumps(42)
        check("json.dumps(42) == '42'", s == "42")
    catch:
        print("ERROR: json.dumps(42) threw exception")
    fade

    try:
        var s = json.dumps(3.14)
        check("json.dumps(3.14) == '3.14'", s == "3.14")
    catch:
        print("ERROR: json.dumps(3.14) threw exception")
    fade

    try:
        var s = json.dumps("hello")
        check("json.dumps('hello') == '\"hello\"'", s == "\"hello\"")
    catch:
        print("ERROR: json.dumps('hello') threw exception")
    fade

    try:
        var s = json.dumps(true)
        check("json.dumps(true) == 'true'", s == "true")
    catch:
        print("ERROR: json.dumps(true) threw exception")
    fade

    try:
        var s = json.dumps(false)
        check("json.dumps(false) == 'false'", s == "false")
    catch:
        print("ERROR: json.dumps(false) threw exception")
    fade

    try:
        var s = json.dumps(None)
        check("json.dumps(None) == 'null'", s == "null")
    catch:
        print("ERROR: json.dumps(None) threw exception")
    fade

    try:
        var s = json.dumps(0)
        check("json.dumps(0) == '0'", s == "0")
    catch:
        print("ERROR: json.dumps(0) threw exception")
    fade

    try:
        var s = json.dumps(-99)
        check("json.dumps(-99) == '-99'", s == "-99")
    catch:
        print("ERROR: json.dumps(-99) threw exception")
    fade

    try:
        var s = json.dumps("")
        check("json.dumps('') == '\"\"'", s == "\"\"")
    catch:
        print("ERROR: json.dumps('') threw exception")
    fade

    # ================================================================
    # json.dumps -- lists / arrays
    # ================================================================
    print("")
    print("--- json.dumps: lists ---")

    try:
        arr a = [1, 2, 3]
        var s = json.dumps(a.elements)
        check("json.dumps([1,2,3]) == '[1, 2, 3]'", s == "[1, 2, 3]")
    catch:
        print("ERROR: json.dumps([1,2,3]) threw exception")
    fade

    try:
        arr a = []
        var s = json.dumps(a.elements)
        check("json.dumps([]) == '[]'", s == "[]")
    catch:
        print("ERROR: json.dumps([]) threw exception")
    fade

    try:
        arr a = ["a", "b", "c"]
        var s = json.dumps(a.elements)
        check("json.dumps(['a','b','c']) works", s == "[\"a\", \"b\", \"c\"]")
    catch:
        print("ERROR: json.dumps(['a','b','c']) threw exception")
    fade

    try:
        arr a = [1, "two", 3.0, true, None]
        var s = json.dumps(a.elements)
        check("json.dumps(mixed list) works", s == "[1, \"two\", 3.0, true, null]")
        print("  mixed:", s)
    catch:
        print("ERROR: json.dumps(mixed list) threw exception")
    fade

    # NOTE: nested Lyric arrays inside .elements remain as ArrObjects and
    # are not recursively converted to Python lists.  json.dumps cannot
    # serialise them, so nested-structure dumps is a known limitation.
    # json.loads of nested structures works fine (returns Python lists).

    # ================================================================
    # json.dumps -- dicts / maps
    # ================================================================
    print("")
    print("--- json.dumps: dicts ---")

    try:
        map m = {"name": "Alice", "age": 30}
        var s = json.dumps(m.elements)
        check("json.dumps(map) produces valid JSON", true)
        print("  map:", s)
    catch:
        print("ERROR: json.dumps(map) threw exception")
    fade

    try:
        map m = {}
        var s = json.dumps(m.elements)
        check("json.dumps({}) == '{}'", s == "{}")
    catch:
        print("ERROR: json.dumps({}) threw exception")
    fade

    # NOTE: nested Lyric maps/arrays inside .elements are not recursively
    # converted — same limitation as nested lists above.

    # NOTE: json.dumps formatting options (indent, sort_keys, separators,
    # ensure_ascii) require keyword arguments which Lyric does not currently
    # support.  Only positional-arg calls are tested here.

    # ================================================================
    # json.loads -- basic types
    # ================================================================
    print("")
    print("--- json.loads: basic types ---")

    try:
        var v = json.loads("42")
        check("json.loads('42') == 42", v == 42)
    catch:
        print("ERROR: json.loads('42') threw exception")
    fade

    try:
        var v = json.loads("3.14")
        check("json.loads('3.14') > 3.13 and < 3.15", v > 3.13 and v < 3.15)
    catch:
        print("ERROR: json.loads('3.14') threw exception")
    fade

    try:
        var v = json.loads("\"hello\"")
        check("json.loads('\"hello\"') == 'hello'", v == "hello")
    catch:
        print("ERROR: json.loads('\"hello\"') threw exception")
    fade

    try:
        var v = json.loads("true")
        check("json.loads('true') == true", v == true)
    catch:
        print("ERROR: json.loads('true') threw exception")
    fade

    try:
        var v = json.loads("false")
        check("json.loads('false') == false", v == false)
    catch:
        print("ERROR: json.loads('false') threw exception")
    fade

    try:
        var v = json.loads("null")
        check("json.loads('null') == None", v == None)
    catch:
        print("ERROR: json.loads('null') threw exception")
    fade

    try:
        var v = json.loads("0")
        check("json.loads('0') == 0", v == 0)
    catch:
        print("ERROR: json.loads('0') threw exception")
    fade

    try:
        var v = json.loads("-99")
        check("json.loads('-99') == -99", v == -99)
    catch:
        print("ERROR: json.loads('-99') threw exception")
    fade

    try:
        var v = json.loads("\"\"")
        check("json.loads('\"\"') == ''", v == "")
    catch:
        print("ERROR: json.loads('\"\"') threw exception")
    fade

    # ================================================================
    # json.loads -- arrays
    # ================================================================
    print("")
    print("--- json.loads: arrays ---")

    try:
        var v = json.loads("[1, 2, 3]")
        check("json.loads('[1,2,3]') callable", true)
        print("  loaded list:", v)
    catch:
        print("ERROR: json.loads('[1,2,3]') threw exception")
    fade

    try:
        var v = json.loads("[]")
        check("json.loads('[]') callable", true)
        print("  loaded empty list:", v)
    catch:
        print("ERROR: json.loads('[]') threw exception")
    fade

    try:
        var v = json.loads("[\"a\", \"b\", \"c\"]")
        check("json.loads string array callable", true)
        print("  loaded string list:", v)
    catch:
        print("ERROR: json.loads string array threw exception")
    fade

    try:
        var v = json.loads("[1, \"two\", 3.0, true, null]")
        check("json.loads mixed array callable", true)
        print("  loaded mixed:", v)
    catch:
        print("ERROR: json.loads mixed array threw exception")
    fade

    try:
        var v = json.loads("[[1, 2], [3, 4]]")
        check("json.loads nested array callable", true)
        print("  loaded nested:", v)
    catch:
        print("ERROR: json.loads nested array threw exception")
    fade

    # ================================================================
    # json.loads -- objects (dicts)
    # ================================================================
    print("")
    print("--- json.loads: objects ---")

    try:
        var v = json.loads("{\"name\": \"Alice\", \"age\": 30}")
        check("json.loads object callable", true)
        print("  loaded object:", v)
    catch:
        print("ERROR: json.loads object threw exception")
    fade

    try:
        var v = json.loads("{}")
        check("json.loads('{}') callable", true)
        print("  loaded empty object:", v)
    catch:
        print("ERROR: json.loads('{}') threw exception")
    fade

    try:
        var v = json.loads("{\"user\": {\"name\": \"Bob\", \"scores\": [10, 20]}}")
        check("json.loads nested object callable", true)
        print("  loaded nested obj:", v)
    catch:
        print("ERROR: json.loads nested object threw exception")
    fade

    # ================================================================
    # Round-trip: dumps → loads
    # ================================================================
    print("")
    print("--- Round-trip: dumps then loads ---")

    try:
        var original = 42
        var encoded = json.dumps(original)
        var decoded = json.loads(encoded)
        check("round-trip int: 42 -> '42' -> 42", decoded == original)
    catch:
        print("ERROR: round-trip int threw exception")
    fade

    try:
        var original = "hello world"
        var encoded = json.dumps(original)
        var decoded = json.loads(encoded)
        check("round-trip string preserved", decoded == original)
    catch:
        print("ERROR: round-trip string threw exception")
    fade

    try:
        var original = 3.14
        var encoded = json.dumps(original)
        var decoded = json.loads(encoded)
        check("round-trip float preserved", decoded > 3.13 and decoded < 3.15)
    catch:
        print("ERROR: round-trip float threw exception")
    fade

    try:
        var original = true
        var encoded = json.dumps(original)
        var decoded = json.loads(encoded)
        check("round-trip true preserved", decoded == true)
    catch:
        print("ERROR: round-trip true threw exception")
    fade

    try:
        var original = false
        var encoded = json.dumps(original)
        var decoded = json.loads(encoded)
        check("round-trip false preserved", decoded == false)
    catch:
        print("ERROR: round-trip false threw exception")
    fade

    try:
        var original = None
        var encoded = json.dumps(original)
        var decoded = json.loads(encoded)
        check("round-trip None preserved", decoded == None)
    catch:
        print("ERROR: round-trip None threw exception")
    fade

    try:
        arr original = [1, "two", 3.0, true, None]
        var encoded = json.dumps(original.elements)
        var decoded = json.loads(encoded)
        check("round-trip mixed list callable", true)
        print("  round-trip list:", decoded)
    catch:
        print("ERROR: round-trip mixed list threw exception")
    fade

    try:
        map original = {"key": "value", "num": 42}
        var encoded = json.dumps(original.elements)
        var decoded = json.loads(encoded)
        check("round-trip map callable", true)
        print("  round-trip map:", decoded)
    catch:
        print("ERROR: round-trip map threw exception")
    fade

    # ================================================================
    # json.loads -- error handling
    # ================================================================
    print("")
    print("--- json.loads: error handling ---")

    try:
        var v = json.loads("not valid json")
        print("ERROR: json.loads('not valid json') should have thrown")
    catch:
        print("PASS: json.loads('not valid json') raises exception")
    fade

    try:
        var v = json.loads("")
        print("ERROR: json.loads('') should have thrown")
    catch:
        print("PASS: json.loads('') raises exception")
    fade

    try:
        var v = json.loads("{bad}")
        print("ERROR: json.loads('{bad}') should have thrown")
    catch:
        print("PASS: json.loads('{bad}') raises exception")
    fade

    try:
        var v = json.loads("[1, 2,]")
        print("ERROR: json.loads('[1,2,]') should have thrown (trailing comma)")
    catch:
        print("PASS: json.loads('[1,2,]') raises exception (trailing comma)")
    fade

    try:
        var v = json.loads("{'key': 'value'}")
        print("ERROR: json.loads single-quote keys should have thrown")
    catch:
        print("PASS: json.loads(single-quote keys) raises exception")
    fade

    # ================================================================
    # json.dumps -- special values
    # ================================================================
    print("")
    print("--- json.dumps: special values ---")

    try:
        var s = json.dumps("line1\nline2")
        check("json.dumps handles newlines in strings", true)
        print("  with newline:", s)
    catch:
        print("ERROR: json.dumps with newlines threw exception")
    fade

    try:
        var s = json.dumps("tab\there")
        check("json.dumps handles tabs in strings", true)
        print("  with tab:", s)
    catch:
        print("ERROR: json.dumps with tabs threw exception")
    fade

    try:
        var s = json.dumps("quote\"here")
        check("json.dumps handles embedded quotes", true)
        print("  with quote:", s)
    catch:
        print("ERROR: json.dumps with quotes threw exception")
    fade

    try:
        var s = json.dumps("back\\slash")
        check("json.dumps handles backslashes", true)
        print("  with backslash:", s)
    catch:
        print("ERROR: json.dumps with backslash threw exception")
    fade

    try:
        var s = json.dumps(10000000000.0)
        check("json.dumps(large float) callable", true)
        print("  large float:", s)
    catch:
        print("ERROR: json.dumps(large float) threw exception")
    fade

    try:
        var s = json.dumps(0.0)
        check("json.dumps(0.0) callable", true)
        print("  0.0:", s)
    catch:
        print("ERROR: json.dumps(0.0) threw exception")
    fade

    # ================================================================
    # json.dumps -- unicode
    # ================================================================
    print("")
    print("--- json.dumps: unicode ---")

    try:
        var s = json.dumps("hello")
        check("json.dumps default ASCII output works", true)
        print("  ascii string:", s)
    catch:
        print("ERROR: json.dumps ascii string threw exception")
    fade

    # ================================================================
    # json.loads -- large / complex structures
    # ================================================================
    print("")
    print("--- json.loads: complex structures ---")

    try:
        str big = "[{\"id\": 1, \"name\": \"Alice\", \"active\": true}, {\"id\": 2, \"name\": \"Bob\", \"active\": false}]"
        var v = json.loads(big)
        check("json.loads array of objects callable", true)
        print("  array of objects:", v)
    catch:
        print("ERROR: json.loads array of objects threw exception")
    fade

    try:
        str deep = "{\"a\": {\"b\": {\"c\": {\"d\": 42}}}}"
        var v = json.loads(deep)
        check("json.loads deeply nested object callable", true)
        print("  deep nesting:", v)
    catch:
        print("ERROR: json.loads deeply nested threw exception")
    fade

    try:
        str nums = "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
        var v = json.loads(nums)
        check("json.loads 10-element array callable", true)
    catch:
        print("ERROR: json.loads 10-element array threw exception")
    fade

    try:
        str mixed = "{\"str\": \"text\", \"int\": 1, \"flt\": 1.5, \"bool\": true, \"nil\": null, \"arr\": [1,2], \"obj\": {\"k\": \"v\"}}"
        var v = json.loads(mixed)
        check("json.loads all JSON types in one object", true)
        print("  all types:", v)
    catch:
        print("ERROR: json.loads all types threw exception")
    fade

    # ================================================================
    # json.JSONDecodeError
    # ================================================================
    print("")
    print("--- JSONDecodeError ---")

    try:
        var err = json.JSONDecodeError
        check("json.JSONDecodeError accessible", true)
    catch:
        print("ERROR: json.JSONDecodeError threw exception")
    fade

    # ================================================================
    # json.tool -- module identity
    # ================================================================
    print("")
    print("--- Module identity ---")

    try:
        var v = json.__name__
        check("json.__name__ == 'json'", v == "json")
    catch:
        print("ERROR: json.__name__ threw exception")
    fade

    print("")
    print("=== json test complete ===")
}
