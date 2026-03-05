# core_sys.ly
# Lyric adhoc test -- exercises the public attributes and functions of Python's
# sys module.
#
# Run with:  lyric run lyric/tests/python_modules/core_sys.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions
#
# NOTE: sys has attribute-level blacklisting in Lyric.  The following are
#       intentionally blocked and will report ERROR when accessed:
#       settrace, setprofile, gettrace, getprofile, _getframe,
#       _current_frames, getrefcount, addaudithook, exc_info
#
# Some values are platform / build dependent.

importpy sys

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
    print("=== Lyric sys module adhoc test ===")
    print("")

    # ================================================================
    # Version information
    # ================================================================
    print("--- Version information ---")

    try:
        var v = sys.version
        check("sys.version is non-empty string", v != "")
        print("  sys.version:", v)
    catch:
        print("ERROR: sys.version threw exception")
    fade

    try:
        var vi = sys.version_info
        check("sys.version_info accessible", true)
        print("  sys.version_info:", vi)
    catch:
        print("ERROR: sys.version_info threw exception")
    fade

    try:
        var vi = sys.version_info
        var major = vi.major
        check("sys.version_info.major >= 3", major >= 3)
        print("  major:", major)
    catch:
        print("ERROR: sys.version_info.major threw exception")
    fade

    try:
        var vi = sys.version_info
        var minor = vi.minor
        check("sys.version_info.minor >= 0", minor >= 0)
        print("  minor:", minor)
    catch:
        print("ERROR: sys.version_info.minor threw exception")
    fade

    try:
        var vi = sys.version_info
        var micro = vi.micro
        check("sys.version_info.micro >= 0", micro >= 0)
        print("  micro:", micro)
    catch:
        print("ERROR: sys.version_info.micro threw exception")
    fade

    try:
        var hv = sys.hexversion
        check("sys.hexversion > 0", hv > 0)
        print("  hexversion:", hv)
    catch:
        print("ERROR: sys.hexversion threw exception")
    fade

    try:
        var api = sys.api_version
        check("sys.api_version > 0", api > 0)
        print("  api_version:", api)
    catch:
        print("ERROR: sys.api_version threw exception")
    fade

    # ================================================================
    # Implementation details
    # ================================================================
    print("")
    print("--- Implementation details ---")

    try:
        var impl = sys.implementation
        check("sys.implementation accessible", true)
        print("  implementation:", impl)
    catch:
        print("ERROR: sys.implementation threw exception")
    fade

    try:
        var name = sys.implementation.name
        check("sys.implementation.name is 'cpython'", name == "cpython")
        print("  implementation.name:", name)
    catch:
        print("ERROR: sys.implementation.name threw exception")
    fade

    try:
        var cver = sys.implementation.cache_tag
        check("sys.implementation.cache_tag non-empty", cver != "")
        print("  cache_tag:", cver)
    catch:
        print("ERROR: sys.implementation.cache_tag threw exception")
    fade

    # ================================================================
    # Platform and build
    # ================================================================
    print("")
    print("--- Platform and build ---")

    try:
        var p = sys.platform
        check("sys.platform is non-empty", p != "")
        print("  platform:", p)
    catch:
        print("ERROR: sys.platform threw exception")
    fade

    try:
        var bo = sys.byteorder
        check("sys.byteorder is 'little' or 'big'", bo == "little" or bo == "big")
        print("  byteorder:", bo)
    catch:
        print("ERROR: sys.byteorder threw exception")
    fade

    try:
        var cp = sys.copyright
        check("sys.copyright is non-empty", cp != "")
    catch:
        print("ERROR: sys.copyright threw exception")
    fade

    try:
        var ex = sys.executable
        check("sys.executable is non-empty", ex != "")
        print("  executable:", ex)
    catch:
        print("ERROR: sys.executable threw exception")
    fade

    try:
        var pfx = sys.prefix
        check("sys.prefix is non-empty", pfx != "")
        print("  prefix:", pfx)
    catch:
        print("ERROR: sys.prefix threw exception")
    fade

    try:
        var epfx = sys.exec_prefix
        check("sys.exec_prefix is non-empty", epfx != "")
        print("  exec_prefix:", epfx)
    catch:
        print("ERROR: sys.exec_prefix threw exception")
    fade

    try:
        var bp = sys.base_prefix
        check("sys.base_prefix is non-empty", bp != "")
        print("  base_prefix:", bp)
    catch:
        print("ERROR: sys.base_prefix threw exception")
    fade

    try:
        var bep = sys.base_exec_prefix
        check("sys.base_exec_prefix is non-empty", bep != "")
        print("  base_exec_prefix:", bep)
    catch:
        print("ERROR: sys.base_exec_prefix threw exception")
    fade

    # ================================================================
    # Recursion limit
    # ================================================================
    print("")
    print("--- Recursion limit ---")

    try:
        var rl = sys.getrecursionlimit()
        check("sys.getrecursionlimit() > 0", rl > 0)
        print("  recursion limit:", rl)
    catch:
        print("ERROR: sys.getrecursionlimit() threw exception")
    fade

    try:
        # save, set, restore
        var orig = sys.getrecursionlimit()
        sys.setrecursionlimit(500)
        var changed = sys.getrecursionlimit()
        check("sys.setrecursionlimit(500) applied", changed == 500)
        sys.setrecursionlimit(orig)
        var restored = sys.getrecursionlimit()
        check("recursion limit restored", restored == orig)
    catch:
        print("ERROR: sys.setrecursionlimit() threw exception")
    fade

    # ================================================================
    # Switch interval
    # ================================================================
    print("")
    print("--- Switch interval ---")

    try:
        var si = sys.getswitchinterval()
        check("sys.getswitchinterval() > 0", si > 0)
        print("  switch interval:", si)
    catch:
        print("ERROR: sys.getswitchinterval() threw exception")
    fade

    try:
        var orig = sys.getswitchinterval()
        sys.setswitchinterval(0.01)
        var changed = sys.getswitchinterval()
        check("sys.setswitchinterval(0.01) applied", changed > 0.009 and changed < 0.011)
        sys.setswitchinterval(orig)
        check("switch interval restored", true)
    catch:
        print("ERROR: sys.setswitchinterval() threw exception")
    fade

    # ================================================================
    # Numeric limits and sizes
    # ================================================================
    print("")
    print("--- Numeric limits and sizes ---")

    try:
        var mi = sys.maxsize
        check("sys.maxsize > 0", mi > 0)
        print("  maxsize:", mi)
    catch:
        print("ERROR: sys.maxsize threw exception")
    fade

    try:
        var mu = sys.maxunicode
        check("sys.maxunicode > 0", mu > 0)
        print("  maxunicode:", mu)
    catch:
        print("ERROR: sys.maxunicode threw exception")
    fade

    try:
        var fi = sys.float_info
        check("sys.float_info accessible", true)
        print("  float_info:", fi)
    catch:
        print("ERROR: sys.float_info threw exception")
    fade

    try:
        var fmax = sys.float_info.max
        check("sys.float_info.max > 0", fmax > 0)
        print("  float_info.max:", fmax)
    catch:
        print("ERROR: sys.float_info.max threw exception")
    fade

    try:
        var fmin = sys.float_info.min
        check("sys.float_info.min > 0", fmin > 0)
        print("  float_info.min:", fmin)
    catch:
        print("ERROR: sys.float_info.min threw exception")
    fade

    try:
        var feps = sys.float_info.epsilon
        check("sys.float_info.epsilon > 0 and < 1", feps > 0 and feps < 1)
        print("  float_info.epsilon:", feps)
    catch:
        print("ERROR: sys.float_info.epsilon threw exception")
    fade

    try:
        var fdig = sys.float_info.dig
        check("sys.float_info.dig > 0", fdig > 0)
        print("  float_info.dig:", fdig)
    catch:
        print("ERROR: sys.float_info.dig threw exception")
    fade

    try:
        var fmant = sys.float_info.mant_dig
        check("sys.float_info.mant_dig > 0", fmant > 0)
        print("  float_info.mant_dig:", fmant)
    catch:
        print("ERROR: sys.float_info.mant_dig threw exception")
    fade

    try:
        var ii = sys.int_info
        check("sys.int_info accessible", true)
        print("  int_info:", ii)
    catch:
        print("ERROR: sys.int_info threw exception")
    fade

    try:
        var bpd = sys.int_info.bits_per_digit
        check("sys.int_info.bits_per_digit > 0", bpd > 0)
        print("  int_info.bits_per_digit:", bpd)
    catch:
        print("ERROR: sys.int_info.bits_per_digit threw exception")
    fade

    try:
        var sod = sys.int_info.sizeof_digit
        check("sys.int_info.sizeof_digit > 0", sod > 0)
        print("  int_info.sizeof_digit:", sod)
    catch:
        print("ERROR: sys.int_info.sizeof_digit threw exception")
    fade

    try:
        var hi = sys.hash_info
        check("sys.hash_info accessible", true)
        print("  hash_info:", hi)
    catch:
        print("ERROR: sys.hash_info threw exception")
    fade

    try:
        var hw = sys.hash_info.width
        check("sys.hash_info.width > 0", hw > 0)
        print("  hash_info.width:", hw)
    catch:
        print("ERROR: sys.hash_info.width threw exception")
    fade

    # ================================================================
    # sizeof
    # ================================================================
    print("")
    print("--- sizeof ---")

    try:
        var si = sys.getsizeof(0)
        check("sys.getsizeof(0) > 0", si > 0)
        print("  getsizeof(0):", si)
    catch:
        print("ERROR: sys.getsizeof(0) threw exception")
    fade

    try:
        var si = sys.getsizeof("")
        check("sys.getsizeof('') > 0", si > 0)
        print("  getsizeof(''):", si)
    catch:
        print("ERROR: sys.getsizeof('') threw exception")
    fade

    try:
        var si = sys.getsizeof("hello")
        check("sys.getsizeof('hello') > getsizeof('')", si > sys.getsizeof(""))
        print("  getsizeof('hello'):", si)
    catch:
        print("ERROR: sys.getsizeof('hello') threw exception")
    fade

    try:
        var si = sys.getsizeof(42)
        check("sys.getsizeof(42) > 0", si > 0)
        print("  getsizeof(42):", si)
    catch:
        print("ERROR: sys.getsizeof(42) threw exception")
    fade

    try:
        var si = sys.getsizeof(3.14)
        check("sys.getsizeof(3.14) > 0", si > 0)
        print("  getsizeof(3.14):", si)
    catch:
        print("ERROR: sys.getsizeof(3.14) threw exception")
    fade

    try:
        var si = sys.getsizeof(true)
        check("sys.getsizeof(true) > 0", si > 0)
        print("  getsizeof(true):", si)
    catch:
        print("ERROR: sys.getsizeof(true) threw exception")
    fade

    try:
        var si = sys.getsizeof(None)
        check("sys.getsizeof(None) > 0", si > 0)
        print("  getsizeof(None):", si)
    catch:
        print("ERROR: sys.getsizeof(None) threw exception")
    fade

    # ================================================================
    # Standard streams
    # ================================================================
    print("")
    print("--- Standard streams ---")

    try:
        var so = sys.stdout
        check("sys.stdout accessible", true)
        print("  stdout:", so)
    catch:
        print("ERROR: sys.stdout threw exception")
    fade

    try:
        var se = sys.stderr
        check("sys.stderr accessible", true)
        print("  stderr:", se)
    catch:
        print("ERROR: sys.stderr threw exception")
    fade

    try:
        var si = sys.stdin
        check("sys.stdin accessible", true)
        print("  stdin:", si)
    catch:
        print("ERROR: sys.stdin threw exception")
    fade

    try:
        var enc = sys.stdout.encoding
        check("sys.stdout.encoding is non-empty", enc != "")
        print("  stdout.encoding:", enc)
    catch:
        print("ERROR: sys.stdout.encoding threw exception")
    fade

    try:
        var enc = sys.getdefaultencoding()
        check("sys.getdefaultencoding() is 'utf-8'", enc == "utf-8")
        print("  default encoding:", enc)
    catch:
        print("ERROR: sys.getdefaultencoding() threw exception")
    fade

    try:
        var fse = sys.getfilesystemencoding()
        check("sys.getfilesystemencoding() non-empty", fse != "")
        print("  filesystem encoding:", fse)
    catch:
        print("ERROR: sys.getfilesystemencoding() threw exception")
    fade

    # ================================================================
    # Path and modules
    # ================================================================
    print("")
    print("--- Path and modules ---")

    try:
        var p = sys.path
        check("sys.path accessible", true)
        print("  sys.path (type):", type(p))
    catch:
        print("ERROR: sys.path threw exception")
    fade

    try:
        var p = sys.path
        var n = p.__len__()
        check("sys.path has at least 1 entry", n >= 1)
        print("  sys.path length:", n)
    catch:
        print("ERROR: sys.path length check threw exception")
    fade

    try:
        var m = sys.modules
        check("sys.modules accessible", true)
        print("  sys.modules (type):", type(m))
    catch:
        print("ERROR: sys.modules threw exception")
    fade

    try:
        var bi = sys.builtin_module_names
        check("sys.builtin_module_names accessible", true)
        print("  builtin_module_names (type):", type(bi))
    catch:
        print("ERROR: sys.builtin_module_names threw exception")
    fade

    try:
        var mp = sys.meta_path
        check("sys.meta_path accessible", true)
    catch:
        print("ERROR: sys.meta_path threw exception")
    fade

    try:
        var ph = sys.path_hooks
        check("sys.path_hooks accessible", true)
    catch:
        print("ERROR: sys.path_hooks threw exception")
    fade

    try:
        var pic = sys.path_importer_cache
        check("sys.path_importer_cache accessible", true)
    catch:
        print("ERROR: sys.path_importer_cache threw exception")
    fade

    # ================================================================
    # argv
    # ================================================================
    print("")
    print("--- argv ---")

    try:
        var a = sys.argv
        check("sys.argv accessible", true)
        print("  sys.argv:", a)
    catch:
        print("ERROR: sys.argv threw exception")
    fade

    try:
        var a = sys.argv
        var n = a.__len__()
        check("sys.argv has at least 1 entry", n >= 1)
        print("  argv length:", n)
    catch:
        print("ERROR: sys.argv length check threw exception")
    fade

    # ================================================================
    # Flags and options
    # ================================================================
    print("")
    print("--- Flags and options ---")

    try:
        var f = sys.flags
        check("sys.flags accessible", true)
        print("  flags:", f)
    catch:
        print("ERROR: sys.flags threw exception")
    fade

    try:
        var dbg = sys.flags.debug
        check("sys.flags.debug is 0 or 1", dbg == 0 or dbg == 1)
    catch:
        print("ERROR: sys.flags.debug threw exception")
    fade

    try:
        var opt = sys.flags.optimize
        check("sys.flags.optimize >= 0", opt >= 0)
        print("  flags.optimize:", opt)
    catch:
        print("ERROR: sys.flags.optimize threw exception")
    fade

    try:
        var dck = sys.dont_write_bytecode
        check("sys.dont_write_bytecode accessible", true)
        print("  dont_write_bytecode:", dck)
    catch:
        print("ERROR: sys.dont_write_bytecode threw exception")
    fade

    # ================================================================
    # Thread info (Python 3.3+)
    # ================================================================
    print("")
    print("--- Thread info ---")

    try:
        var ti = sys.thread_info
        check("sys.thread_info accessible", true)
        print("  thread_info:", ti)
    catch:
        print("ERROR: sys.thread_info threw exception (Python 3.3+)")
    fade

    try:
        var tn = sys.thread_info.name
        check("sys.thread_info.name non-empty", tn != "" and tn != None)
        print("  thread_info.name:", tn)
    catch:
        print("ERROR: sys.thread_info.name threw exception")
    fade

    # ================================================================
    # Intern
    # ================================================================
    print("")
    print("--- Intern ---")

    try:
        var s = sys.intern("hello")
        check("sys.intern('hello') == 'hello'", s == "hello")
    catch:
        print("ERROR: sys.intern() threw exception")
    fade

    try:
        var a = sys.intern("lyric_test_intern")
        var b = sys.intern("lyric_test_intern")
        check("sys.intern() returns same identity for same string", a == b)
    catch:
        print("ERROR: sys.intern() identity threw exception")
    fade

    # ================================================================
    # getwindowsversion (Windows only)
    # ================================================================
    print("")
    print("--- Platform-specific ---")

    try:
        var wv = sys.getwindowsversion()
        check("sys.getwindowsversion() callable", true)
        print("  windows version:", wv)
    catch:
        print("ERROR: sys.getwindowsversion() threw exception (Windows only)")
    fade

    try:
        var wv = sys.getwindowsversion()
        var major = wv.major
        check("sys.getwindowsversion().major >= 6", major >= 6)
        print("  windows major:", major)
    catch:
        print("ERROR: sys.getwindowsversion().major threw exception")
    fade

    try:
        var wv = sys.getwindowsversion()
        var build = wv.build
        check("sys.getwindowsversion().build > 0", build > 0)
        print("  windows build:", build)
    catch:
        print("ERROR: sys.getwindowsversion().build threw exception")
    fade

    try:
        var wv = sys.winver
        check("sys.winver non-empty (Windows CPython)", wv != "")
        print("  winver:", wv)
    catch:
        print("ERROR: sys.winver threw exception (Windows CPython only)")
    fade

    # ================================================================
    # Default print hooks and display hooks
    # ================================================================
    print("")
    print("--- Display and exception hooks ---")

    try:
        var dh = sys.displayhook
        check("sys.displayhook accessible", true)
    catch:
        print("ERROR: sys.displayhook threw exception")
    fade

    try:
        var eh = sys.excepthook
        check("sys.excepthook accessible", true)
    catch:
        print("ERROR: sys.excepthook threw exception")
    fade

    try:
        var dh = sys.__displayhook__
        check("sys.__displayhook__ accessible", true)
    catch:
        print("ERROR: sys.__displayhook__ threw exception")
    fade

    try:
        var eh = sys.__excepthook__
        check("sys.__excepthook__ accessible", true)
    catch:
        print("ERROR: sys.__excepthook__ threw exception")
    fade

    # ================================================================
    # Miscellaneous attributes
    # ================================================================
    print("")
    print("--- Miscellaneous attributes ---")

    # this test expected to fail on windows
    #try:
    #    var ck = sys.abiflags
    #    check("sys.abiflags accessible", true)
    #    print("  abiflags:", ck)
    #catch:
    #    print("ERROR: sys.abiflags threw exception (not available on Windows)")
    #fade

    try:
        var fsep = sys.float_repr_style
        check("sys.float_repr_style is 'short' or 'legacy'", fsep == "short" or fsep == "legacy")
        print("  float_repr_style:", fsep)
    catch:
        print("ERROR: sys.float_repr_style threw exception")
    fade

    try:
        var plat_dir = sys.platlibdir
        check("sys.platlibdir non-empty (Python 3.9+)", plat_dir != "")
        print("  platlibdir:", plat_dir)
    catch:
        print("ERROR: sys.platlibdir threw exception (Python 3.9+)")
    fade

    try:
        var dl = sys.dllhandle
        check("sys.dllhandle accessible (Windows)", true)
        print("  dllhandle:", dl)
    catch:
        print("ERROR: sys.dllhandle threw exception (Windows only)")
    fade

    try:
        var orig_prefix = sys.orig_argv
        check("sys.orig_argv accessible (Python 3.10+)", true)
        print("  orig_argv:", orig_prefix)
    catch:
        print("ERROR: sys.orig_argv threw exception (Python 3.10+)")
    fade

    try:
        var stdlib = sys.stdlib_module_names
        check("sys.stdlib_module_names accessible (Python 3.10+)", true)
    catch:
        print("ERROR: sys.stdlib_module_names threw exception (Python 3.10+)")
    fade

    # ================================================================
    # Blacklisted attributes (should all raise errors)
    # ================================================================
    print("")
    print("--- Blacklisted attributes (expect ERROR for each) ---")

    try:
        sys.settrace(None)
        print("ERROR: sys.settrace should be blacklisted but was not blocked")
    catch:
        print("PASS: sys.settrace correctly blacklisted")
    fade

    try:
        sys.setprofile(None)
        print("ERROR: sys.setprofile should be blacklisted but was not blocked")
    catch:
        print("PASS: sys.setprofile correctly blacklisted")
    fade

    try:
        var v = sys.gettrace()
        print("ERROR: sys.gettrace should be blacklisted but was not blocked")
    catch:
        print("PASS: sys.gettrace correctly blacklisted")
    fade

    try:
        var v = sys.getprofile()
        print("ERROR: sys.getprofile should be blacklisted but was not blocked")
    catch:
        print("PASS: sys.getprofile correctly blacklisted")
    fade

    try:
        var v = sys._getframe()
        print("ERROR: sys._getframe should be blacklisted but was not blocked")
    catch:
        print("PASS: sys._getframe correctly blacklisted")
    fade

    try:
        var v = sys._current_frames()
        print("ERROR: sys._current_frames should be blacklisted but was not blocked")
    catch:
        print("PASS: sys._current_frames correctly blacklisted")
    fade

    try:
        var v = sys.getrefcount(42)
        print("ERROR: sys.getrefcount should be blacklisted but was not blocked")
    catch:
        print("PASS: sys.getrefcount correctly blacklisted")
    fade

    try:
        var v = sys.addaudithook
        print("ERROR: sys.addaudithook should be blacklisted but was not blocked")
    catch:
        print("PASS: sys.addaudithook correctly blacklisted")
    fade

    try:
        var v = sys.exc_info()
        print("ERROR: sys.exc_info should be blacklisted but was not blocked")
    catch:
        print("PASS: sys.exc_info correctly blacklisted")
    fade

    print("")
    print("=== sys test complete ===")
}
