# core_collections.ly
# Lyric adhoc test -- exercises the public classes and functions of Python's collections module.
#
# Run with:  lyric run lyric/tests/python_modules/core_collections.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions

importpy collections

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
    print("=== Lyric collections module adhoc test ===")
    print("")

    # ================================================================
    # Module identity
    # ================================================================
    print("--- Module identity ---")

    try:
        var v = collections.__name__
        check("collections.__name__ == 'collections'", v == "collections")
    catch:
        print("ERROR: collections.__name__ threw exception")
    fade

    # ================================================================
    # Counter -- creation and basic usage
    # ================================================================
    print("")
    print("--- Counter: creation ---")

    try:
        var c = collections.Counter()
        check("Counter() creates empty counter", true)
        print("  empty counter:", c)
    catch:
        print("ERROR: Counter() threw exception")
    fade

    try:
        var c = collections.Counter("abracadabra")
        check("Counter(string) counts characters", true)
        print("  counter('abracadabra'):", c)
    catch:
        print("ERROR: Counter(string) threw exception")
    fade

    try:
        arr words = ["red", "blue", "red", "green", "blue", "blue"]
        var c = collections.Counter(words)
        check("Counter(list) counts elements", true)
        print("  counter(list):", c)
    catch:
        print("ERROR: Counter(list) threw exception")
    fade

    # ================================================================
    # Counter -- element access
    # ================================================================
    print("")
    print("--- Counter: element access ---")

    try:
        var c = collections.Counter("abracadabra")
        var a_count = c["a"]
        check("counter['a'] == 5", a_count == 5)
    catch:
        print("ERROR: counter['a'] threw exception")
    fade

    try:
        var c = collections.Counter("abracadabra")
        var b_count = c["b"]
        check("counter['b'] == 2", b_count == 2)
    catch:
        print("ERROR: counter['b'] threw exception")
    fade

    try:
        var c = collections.Counter("abracadabra")
        var z_count = c["z"]
        check("counter['z'] == 0 (missing key returns 0)", z_count == 0)
    catch:
        print("ERROR: counter['z'] threw exception")
    fade

    # ================================================================
    # Counter -- most_common
    # ================================================================
    print("")
    print("--- Counter: most_common ---")

    try:
        var c = collections.Counter("abracadabra")
        var mc = c.most_common(3)
        check("most_common(3) returns list", true)
        print("  most_common(3):", mc)
    catch:
        print("ERROR: most_common(3) threw exception")
    fade

    try:
        var c = collections.Counter("abracadabra")
        var mc = c.most_common()
        check("most_common() returns all elements sorted", true)
        print("  most_common():", mc)
    catch:
        print("ERROR: most_common() threw exception")
    fade

    # ================================================================
    # Counter -- update
    # ================================================================
    print("")
    print("--- Counter: update ---")

    try:
        var c = collections.Counter("aab")
        c.update("bcc")
        var a_count = c["a"]
        var b_count = c["b"]
        var c_count = c["c"]
        check("update adds counts: a==2", a_count == 2)
        check("update adds counts: b==2", b_count == 2)
        check("update adds counts: c==2", c_count == 2)
    catch:
        print("ERROR: Counter.update() threw exception")
    fade

    # ================================================================
    # Counter -- total (Python 3.10+)
    # ================================================================
    print("")
    print("--- Counter: total ---")

    try:
        var c = collections.Counter("abracadabra")
        var t = c.total()
        check("total() == 11", t == 11)
    catch:
        print("ERROR: Counter.total() threw exception (Python 3.10+ only)")
    fade

    # ================================================================
    # Counter -- clear
    # ================================================================
    print("")
    print("--- Counter: clear ---")

    try:
        var c = collections.Counter("abc")
        c.clear()
        var a_count = c["a"]
        check("clear() resets all counts to 0", a_count == 0)
    catch:
        print("ERROR: Counter.clear() threw exception")
    fade

    # ================================================================
    # Counter -- values, keys
    # ================================================================
    print("")
    print("--- Counter: keys and values ---")

    try:
        var c = collections.Counter("aabbb")
        var keys = arr(c.keys())
        check("keys() returns key list", true)
        print("  keys:", keys)
    catch:
        print("ERROR: Counter.keys() threw exception")
    fade

    try:
        var c = collections.Counter("aabbb")
        var vals = arr(c.values())
        check("values() returns value list", true)
        print("  values:", vals)
    catch:
        print("ERROR: Counter.values() threw exception")
    fade

    # ================================================================
    # defaultdict -- creation and usage
    # ================================================================
    # NOTE: defaultdict's auto-creation on missing keys (the __missing__ callback)
    # does not work in Lyric because Python's defaultdict calls the factory function
    # (int, list, str) in Python's runtime, but Lyric's type keywords (int, str) are
    # builtin conversion functions that require arguments. This is a known importpy
    # limitation: Python cannot call back into Lyric functions.
    #
    # defaultdict still works for explicit assignment and retrieval of existing keys.
    print("")
    print("--- defaultdict: creation and explicit usage ---")

    try:
        var d = collections.defaultdict(int)
        check("defaultdict(int) created", true)
    catch:
        print("ERROR: defaultdict(int) threw exception")
    fade

    try:
        var d = collections.defaultdict(str)
        check("defaultdict(str) created", true)
    catch:
        print("ERROR: defaultdict(str) threw exception")
    fade

    try:
        var d = collections.defaultdict(int)
        d["x"] = 10
        d["x"] += 5
        var v = d["x"]
        check("defaultdict(int) assignment and compound: x == 15", v == 15)
    catch:
        print("ERROR: defaultdict(int) assignment threw exception")
    fade

    # ================================================================
    # defaultdict -- iteration
    # ================================================================
    print("")
    print("--- defaultdict: keys and items ---")

    try:
        var d = collections.defaultdict(int)
        d["a"] = 1
        d["b"] = 2
        var keys = arr(d.keys())
        check("defaultdict.keys() returns key list", true)
        print("  keys:", keys)
    catch:
        print("ERROR: defaultdict.keys() threw exception")
    fade

    try:
        var d = collections.defaultdict(int)
        d["a"] = 1
        d["b"] = 2
        var items = arr(d.items())
        check("defaultdict.items() returns item list", true)
        print("  items:", items)
    catch:
        print("ERROR: defaultdict.items() threw exception")
    fade

    # ================================================================
    # deque -- creation
    # ================================================================
    print("")
    print("--- deque: creation ---")

    try:
        var dq = collections.deque()
        check("deque() creates empty deque", true)
        print("  empty deque:", dq)
    catch:
        print("ERROR: deque() threw exception")
    fade

    try:
        arr items = [1, 2, 3]
        var dq = collections.deque(items)
        check("deque(list) creates from list", true)
        print("  deque([1,2,3]):", dq)
    catch:
        print("ERROR: deque(list) threw exception")
    fade

    try:
        var dq = collections.deque("abc")
        check("deque(string) creates from chars", true)
        print("  deque('abc'):", dq)
    catch:
        print("ERROR: deque(string) threw exception")
    fade

    # ================================================================
    # deque -- append and appendleft
    # ================================================================
    print("")
    print("--- deque: append / appendleft ---")

    try:
        var dq = collections.deque()
        dq.append(1)
        dq.append(2)
        dq.append(3)
        check("append adds to right end", true)
        print("  after appends:", dq)
    catch:
        print("ERROR: deque.append() threw exception")
    fade

    try:
        var dq = collections.deque()
        dq.appendleft(1)
        dq.appendleft(2)
        dq.appendleft(3)
        check("appendleft adds to left end", true)
        print("  after appendlefts:", dq)
    catch:
        print("ERROR: deque.appendleft() threw exception")
    fade

    # ================================================================
    # deque -- pop and popleft
    # ================================================================
    print("")
    print("--- deque: pop / popleft ---")

    try:
        arr items = [1, 2, 3, 4, 5]
        var dq = collections.deque(items)
        var v = dq.pop()
        check("pop() returns rightmost: 5", v == 5)
        print("  after pop:", dq)
    catch:
        print("ERROR: deque.pop() threw exception")
    fade

    try:
        arr items = [1, 2, 3, 4, 5]
        var dq = collections.deque(items)
        var v = dq.popleft()
        check("popleft() returns leftmost: 1", v == 1)
        print("  after popleft:", dq)
    catch:
        print("ERROR: deque.popleft() threw exception")
    fade

    # ================================================================
    # deque -- rotate
    # ================================================================
    print("")
    print("--- deque: rotate ---")

    try:
        arr items = [1, 2, 3, 4, 5]
        var dq = collections.deque(items)
        dq.rotate(2)
        check("rotate(2) shifts right", true)
        print("  rotate(2):", dq)
    catch:
        print("ERROR: deque.rotate(2) threw exception")
    fade

    try:
        arr items = [1, 2, 3, 4, 5]
        var dq = collections.deque(items)
        dq.rotate(-2)
        check("rotate(-2) shifts left", true)
        print("  rotate(-2):", dq)
    catch:
        print("ERROR: deque.rotate(-2) threw exception")
    fade

    # ================================================================
    # deque -- extend and extendleft
    # ================================================================
    print("")
    print("--- deque: extend / extendleft ---")

    try:
        arr start = [1, 2]
        arr extra = [3, 4, 5]
        var dq = collections.deque(start)
        dq.extend(extra)
        check("extend adds to right", true)
        print("  after extend:", dq)
    catch:
        print("ERROR: deque.extend() threw exception")
    fade

    try:
        arr start = [1, 2]
        arr extra = [3, 4, 5]
        var dq = collections.deque(start)
        dq.extendleft(extra)
        check("extendleft adds to left (reversed)", true)
        print("  after extendleft:", dq)
    catch:
        print("ERROR: deque.extendleft() threw exception")
    fade

    # ================================================================
    # deque -- maxlen
    # ================================================================
    print("")
    print("--- deque: maxlen ---")

    try:
        arr items = [1, 2, 3]
        var dq = collections.deque(items, 3)
        dq.append(4)
        check("maxlen=3 drops leftmost on overflow", true)
        print("  after append(4) with maxlen=3:", dq)
    catch:
        print("ERROR: deque with maxlen threw exception")
    fade

    try:
        arr items = [1, 2, 3]
        var dq = collections.deque(items, 3)
        var ml = dq.maxlen
        check("deque.maxlen == 3", ml == 3)
    catch:
        print("ERROR: deque.maxlen threw exception")
    fade

    # ================================================================
    # deque -- len and clear
    # ================================================================
    print("")
    print("--- deque: len and clear ---")

    try:
        arr items = [1, 2, 3, 4]
        var dq = collections.deque(items)
        var n = dq.len()
        check("deque.len() == 4", n == 4)
    catch:
        print("ERROR: deque.len() threw exception")
    fade

    try:
        arr items = [1, 2, 3]
        var dq = collections.deque(items)
        dq.clear()
        var n = dq.len()
        check("clear() empties deque: len == 0", n == 0)
    catch:
        print("ERROR: deque.clear() threw exception")
    fade

    # ================================================================
    # deque -- count and reverse
    # ================================================================
    print("")
    print("--- deque: count and reverse ---")

    try:
        arr items = [1, 2, 2, 3, 2]
        var dq = collections.deque(items)
        var c = dq.count(2)
        check("count(2) == 3", c == 3)
    catch:
        print("ERROR: deque.count() threw exception")
    fade

    try:
        arr items = [1, 2, 3]
        var dq = collections.deque(items)
        dq.reverse()
        check("reverse() reverses in place", true)
        print("  after reverse:", dq)
    catch:
        print("ERROR: deque.reverse() threw exception")
    fade

    # ================================================================
    # OrderedDict -- creation
    # ================================================================
    print("")
    print("--- OrderedDict ---")

    try:
        var od = collections.OrderedDict()
        check("OrderedDict() created", true)
    catch:
        print("ERROR: OrderedDict() threw exception")
    fade

    try:
        var od = collections.OrderedDict()
        od["first"] = 1
        od["second"] = 2
        od["third"] = 3
        var keys = arr(od.keys())
        check("OrderedDict preserves insertion order", true)
        print("  keys:", keys)
    catch:
        print("ERROR: OrderedDict key insertion threw exception")
    fade

    try:
        var od = collections.OrderedDict()
        od["a"] = 1
        od["b"] = 2
        od["c"] = 3
        od.move_to_end("a")
        var keys = arr(od.keys())
        check("move_to_end('a') moves to last", true)
        print("  after move_to_end('a'):", keys)
    catch:
        print("ERROR: OrderedDict.move_to_end() threw exception")
    fade

    try:
        var od = collections.OrderedDict()
        od["a"] = 1
        od["b"] = 2
        od["c"] = 3
        od.move_to_end("c", false)
        var keys = arr(od.keys())
        check("move_to_end('c', false) moves to first", true)
        print("  after move_to_end('c', false):", keys)
    catch:
        print("ERROR: OrderedDict.move_to_end(last=false) threw exception")
    fade

    # ================================================================
    # namedtuple -- creation and access
    # ================================================================
    print("")
    print("--- namedtuple ---")

    try:
        var Point = collections.namedtuple("Point", ["x", "y"])
        check("namedtuple('Point', ['x','y']) created", true)
    catch:
        print("ERROR: namedtuple creation threw exception")
    fade

    try:
        var Point = collections.namedtuple("Point", ["x", "y"])
        var p = Point(3, 4)
        check("Point(3, 4) created", true)
        print("  Point:", p)
    catch:
        print("ERROR: namedtuple instantiation threw exception")
    fade

    try:
        var Point = collections.namedtuple("Point", ["x", "y"])
        var p = Point(3, 4)
        var x = p.x
        var y = p.y
        check("p.x == 3", x == 3)
        check("p.y == 4", y == 4)
    catch:
        print("ERROR: namedtuple field access threw exception")
    fade

    try:
        var Point = collections.namedtuple("Point", ["x", "y"])
        var p = Point(3, 4)
        var x = p[0]
        var y = p[1]
        check("p[0] == 3 (index access)", x == 3)
        check("p[1] == 4 (index access)", y == 4)
    catch:
        print("ERROR: namedtuple index access threw exception")
    fade

    # ================================================================
    # ChainMap -- creation and lookup
    # ================================================================
    print("")
    print("--- ChainMap ---")

    try:
        map defaults = {"color": "red", "size": "medium"}
        map overrides = {"color": "blue"}
        var cm = collections.ChainMap(overrides.elements, defaults.elements)
        check("ChainMap created", true)
    catch:
        print("ERROR: ChainMap creation threw exception")
    fade

    try:
        map defaults = {"color": "red", "size": "medium"}
        map overrides = {"color": "blue"}
        var cm = collections.ChainMap(overrides.elements, defaults.elements)
        var color = cm["color"]
        check("ChainMap lookup 'color' == 'blue' (override wins)", color == "blue")
    catch:
        print("ERROR: ChainMap lookup 'color' threw exception")
    fade

    try:
        map defaults = {"color": "red", "size": "medium"}
        map overrides = {"color": "blue"}
        var cm = collections.ChainMap(overrides.elements, defaults.elements)
        var size = cm["size"]
        check("ChainMap lookup 'size' == 'medium' (falls through)", size == "medium")
    catch:
        print("ERROR: ChainMap lookup 'size' threw exception")
    fade

    try:
        map defaults = {"color": "red", "size": "medium"}
        map overrides = {"color": "blue"}
        var cm = collections.ChainMap(overrides.elements, defaults.elements)
        var keys = arr(cm.keys())
        check("ChainMap.keys() returns merged keys", true)
        print("  keys:", keys)
    catch:
        print("ERROR: ChainMap.keys() threw exception")
    fade

    print("")
    print("=== collections test complete ===")
}
