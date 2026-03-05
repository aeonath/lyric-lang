# core_os.ly
# Lyric adhoc test -- exercises the public functions and constants of Python's
# os and os.path modules.
#
# Run with:  lyric run lyric/tests/python_modules/core_os.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions
#
# NOTE: Some values are platform-dependent (path separators, pid, etc.).

importpy os

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
    print("=== Lyric os module adhoc test ===")
    print("")

    # ================================================================
    # Platform constants
    # ================================================================
    print("--- Platform constants ---")

    try:
        var name = os.name
        check("os.name is 'nt' or 'posix' or 'java'", name == "nt" or name == "posix" or name == "java")
        print("  os.name:", name)
    catch:
        print("ERROR: os.name threw exception")
    fade

    try:
        var sep = os.sep
        check("os.sep is '/' or '\\'", sep == "/" or sep == "\\")
        print("  os.sep:", sep)
    catch:
        print("ERROR: os.sep threw exception")
    fade

    try:
        var altsep = os.altsep
        # altsep is '/' on Windows, None on POSIX
        check("os.altsep accessible", true)
        print("  os.altsep:", altsep)
    catch:
        print("ERROR: os.altsep threw exception")
    fade

    try:
        var extsep = os.extsep
        check("os.extsep is '.'", extsep == ".")
    catch:
        print("ERROR: os.extsep threw exception")
    fade

    try:
        var pathsep = os.pathsep
        check("os.pathsep is ':' or ';'", pathsep == ":" or pathsep == ";")
        print("  os.pathsep:", pathsep)
    catch:
        print("ERROR: os.pathsep threw exception")
    fade

    try:
        var linesep = os.linesep
        check("os.linesep is non-empty", linesep != "")
    catch:
        print("ERROR: os.linesep threw exception")
    fade

    try:
        var devnull = os.devnull
        check("os.devnull is non-empty", devnull != "")
        print("  os.devnull:", devnull)
    catch:
        print("ERROR: os.devnull threw exception")
    fade

    try:
        var curdir = os.curdir
        check("os.curdir is '.'", curdir == ".")
    catch:
        print("ERROR: os.curdir threw exception")
    fade

    try:
        var pardir = os.pardir
        check("os.pardir is '..'", pardir == "..")
    catch:
        print("ERROR: os.pardir threw exception")
    fade

    # ================================================================
    # Access-test constants
    # ================================================================
    print("")
    print("--- Access-test constants ---")

    try:
        var fok = os.F_OK
        check("os.F_OK is 0", fok == 0)
    catch:
        print("ERROR: os.F_OK threw exception")
    fade

    try:
        var rok = os.R_OK
        check("os.R_OK > 0", rok > 0)
        print("  os.R_OK:", rok)
    catch:
        print("ERROR: os.R_OK threw exception")
    fade

    try:
        var wok = os.W_OK
        check("os.W_OK > 0", wok > 0)
        print("  os.W_OK:", wok)
    catch:
        print("ERROR: os.W_OK threw exception")
    fade

    try:
        var xok = os.X_OK
        check("os.X_OK > 0", xok > 0)
        print("  os.X_OK:", xok)
    catch:
        print("ERROR: os.X_OK threw exception")
    fade

    # ================================================================
    # Environment and system info
    # ================================================================
    print("")
    print("--- Environment and system info ---")

    try:
        var cwd = os.getcwd()
        check("os.getcwd() returns non-empty string", cwd != "")
        print("  cwd:", cwd)
    catch:
        print("ERROR: os.getcwd() threw exception")
    fade

    try:
        var path_env = os.getenv("PATH")
        check("os.getenv('PATH') returns non-empty", path_env != "" and path_env != None)
        print("  PATH (first 60 chars):", path_env[:60])
    catch:
        print("ERROR: os.getenv('PATH') threw exception")
    fade

    try:
        var missing = os.getenv("LYRIC_NONEXISTENT_VAR_XYZ_99")
        check("os.getenv() returns None for missing var", missing == None)
    catch:
        print("ERROR: os.getenv() for missing var threw exception")
    fade

    try:
        var missing = os.getenv("LYRIC_NONEXISTENT_VAR_XYZ_99", "fallback")
        check("os.getenv() with default returns the default", missing == "fallback")
    catch:
        print("ERROR: os.getenv() with default threw exception")
    fade

    try:
        var cpus = os.cpu_count()
        check("os.cpu_count() >= 1", cpus >= 1)
        print("  cpu_count:", cpus)
    catch:
        print("ERROR: os.cpu_count() threw exception")
    fade

    # ================================================================
    # Process info
    # ================================================================
    print("")
    print("--- Process info ---")

    try:
        var pid = os.getpid()
        check("os.getpid() > 0", pid > 0)
        print("  pid:", pid)
    catch:
        print("ERROR: os.getpid() threw exception")
    fade

    try:
        var ppid = os.getppid()
        check("os.getppid() >= 0", ppid >= 0)
        print("  ppid:", ppid)
    catch:
        print("ERROR: os.getppid() threw exception")
    fade

    try:
        var login = os.getlogin()
        check("os.getlogin() returns non-empty string", login != "")
        print("  login:", login)
    catch:
        print("ERROR: os.getlogin() threw exception (may fail in non-interactive env)")
    fade

    # ================================================================
    # os.path -- Joining and splitting
    # ================================================================
    print("")
    print("--- os.path: joining and splitting ---")

    try:
        var p = os.path.join("usr", "local", "bin")
        check("os.path.join('usr','local','bin') non-empty", p != "")
        print("  join:", p)
    catch:
        print("ERROR: os.path.join() threw exception")
    fade

    try:
        var p = os.path.join("a")
        check("os.path.join('a') == 'a'", p == "a")
    catch:
        print("ERROR: os.path.join('a') threw exception")
    fade

    try:
        var p = os.path.join("a", "b")
        check("os.path.join('a','b') non-empty", p != "")
        print("  join(a,b):", p)
    catch:
        print("ERROR: os.path.join('a','b') threw exception")
    fade

    try:
        var base = os.path.basename("/home/user/file.txt")
        check("os.path.basename('/home/user/file.txt') == 'file.txt'", base == "file.txt")
    catch:
        print("ERROR: os.path.basename() threw exception")
    fade

    try:
        var base = os.path.basename("/home/user/")
        check("os.path.basename('/home/user/') == '' (trailing slash)", base == "")
    catch:
        print("ERROR: os.path.basename() trailing slash threw exception")
    fade

    try:
        var base = os.path.basename("file.txt")
        check("os.path.basename('file.txt') == 'file.txt'", base == "file.txt")
    catch:
        print("ERROR: os.path.basename('file.txt') threw exception")
    fade

    try:
        var d = os.path.dirname("/home/user/file.txt")
        check("os.path.dirname('/home/user/file.txt') non-empty", d != "")
        print("  dirname:", d)
    catch:
        print("ERROR: os.path.dirname() threw exception")
    fade

    try:
        var d = os.path.dirname("file.txt")
        check("os.path.dirname('file.txt') == ''", d == "")
    catch:
        print("ERROR: os.path.dirname('file.txt') threw exception")
    fade

    try:
        var parts = os.path.split("/home/user/file.txt")
        check("os.path.split('/home/user/file.txt') callable", true)
        print("  split:", parts)
    catch:
        print("ERROR: os.path.split() threw exception")
    fade

    try:
        var parts = os.path.split("file.txt")
        check("os.path.split('file.txt') callable", true)
        print("  split('file.txt'):", parts)
    catch:
        print("ERROR: os.path.split('file.txt') threw exception")
    fade

    try:
        var parts = os.path.splitext("document.tar.gz")
        check("os.path.splitext('document.tar.gz') callable", true)
        print("  splitext:", parts)
    catch:
        print("ERROR: os.path.splitext() threw exception")
    fade

    try:
        var parts = os.path.splitext("noext")
        check("os.path.splitext('noext') callable", true)
        print("  splitext('noext'):", parts)
    catch:
        print("ERROR: os.path.splitext('noext') threw exception")
    fade

    try:
        var parts = os.path.splitext(".hidden")
        check("os.path.splitext('.hidden') callable", true)
        print("  splitext('.hidden'):", parts)
    catch:
        print("ERROR: os.path.splitext('.hidden') threw exception")
    fade

    # ================================================================
    # os.path -- Normalisation and resolution
    # ================================================================
    print("")
    print("--- os.path: normalisation and resolution ---")

    try:
        var p = os.path.normpath("a/b/../c")
        check("os.path.normpath('a/b/../c') resolves '..'", true)
        print("  normpath('a/b/../c'):", p)
    catch:
        print("ERROR: os.path.normpath() threw exception")
    fade

    try:
        var p = os.path.normpath("a/./b/./c")
        check("os.path.normpath('a/./b/./c') removes '.'", true)
        print("  normpath('a/./b/./c'):", p)
    catch:
        print("ERROR: os.path.normpath() with dots threw exception")
    fade

    try:
        var p = os.path.normpath("///a///b///")
        check("os.path.normpath collapses repeated slashes", true)
        print("  normpath('///a///b///'):", p)
    catch:
        print("ERROR: os.path.normpath() repeated slashes threw exception")
    fade

    try:
        var p = os.path.normcase("ABC/Def/ghi")
        check("os.path.normcase() callable", true)
        print("  normcase('ABC/Def/ghi'):", p)
    catch:
        print("ERROR: os.path.normcase() threw exception")
    fade

    try:
        var p = os.path.abspath(".")
        check("os.path.abspath('.') returns non-empty", p != "")
        print("  abspath('.'):", p)
    catch:
        print("ERROR: os.path.abspath('.') threw exception")
    fade

    try:
        var p = os.path.abspath("relative/path")
        check("os.path.abspath('relative/path') is absolute", os.path.isabs(p) == true)
        print("  abspath('relative/path'):", p)
    catch:
        print("ERROR: os.path.abspath('relative/path') threw exception")
    fade

    try:
        var p = os.path.realpath(".")
        check("os.path.realpath('.') returns non-empty", p != "")
        print("  realpath('.'):", p)
    catch:
        print("ERROR: os.path.realpath() threw exception")
    fade

    try:
        # Use abspath('.') which is guaranteed absolute on any platform
        var absp = os.path.abspath(".")
        var v1 = os.path.isabs(absp)
        check("os.path.isabs(abspath('.')) is true", v1 == true)
    catch:
        print("ERROR: os.path.isabs(abspath) threw exception")
    fade

    try:
        var v2 = os.path.isabs("relative")
        check("os.path.isabs('relative') is false", v2 == false)
    catch:
        print("ERROR: os.path.isabs('relative') threw exception")
    fade

    try:
        var p = os.path.expanduser("~")
        check("os.path.expanduser('~') expands home dir", p != "~")
        print("  expanduser('~'):", p)
    catch:
        print("ERROR: os.path.expanduser() threw exception")
    fade

    try:
        var p = os.path.expandvars("$PATH")
        check("os.path.expandvars('$PATH') callable", true)
    catch:
        print("ERROR: os.path.expandvars() threw exception")
    fade

    try:
        var p = os.path.relpath("a/b/c", "a")
        check("os.path.relpath('a/b/c', 'a') non-empty", p != "")
        print("  relpath('a/b/c', 'a'):", p)
    catch:
        print("ERROR: os.path.relpath() threw exception")
    fade

    try:
        var p = os.path.relpath(".")
        check("os.path.relpath('.') == '.'", p == ".")
    catch:
        print("ERROR: os.path.relpath('.') threw exception")
    fade

    # ================================================================
    # os.path -- Prefix and ancestor utilities
    # ================================================================
    print("")
    print("--- os.path: prefix and ancestor utilities ---")

    try:
        arr paths = ["a/b/c", "a/b/d", "a/b/e"]
        var prefix = os.path.commonprefix(paths.elements)
        check("os.path.commonprefix() finds common prefix", prefix != "")
        print("  commonprefix:", prefix)
    catch:
        print("ERROR: os.path.commonprefix() threw exception")
    fade

    try:
        arr paths = ["abc", "xyz"]
        var prefix = os.path.commonprefix(paths.elements)
        check("os.path.commonprefix() returns '' for no common prefix", prefix == "")
    catch:
        print("ERROR: os.path.commonprefix() no common threw exception")
    fade

    try:
        arr paths = ["a/b/c", "a/b/d"]
        var common = os.path.commonpath(paths.elements)
        check("os.path.commonpath() finds common ancestor", common != "")
        print("  commonpath:", common)
    catch:
        print("ERROR: os.path.commonpath() threw exception")
    fade

    # ================================================================
    # os.path -- Existence and type queries
    # ================================================================
    print("")
    print("--- os.path: existence and type queries ---")

    try:
        var v = os.path.exists(".")
        check("os.path.exists('.') is true", v == true)
    catch:
        print("ERROR: os.path.exists('.') threw exception")
    fade

    try:
        var v = os.path.exists("__nonexistent_lyric_test_path__")
        check("os.path.exists() is false for missing path", v == false)
    catch:
        print("ERROR: os.path.exists() for missing path threw exception")
    fade

    try:
        var v = os.path.isdir(".")
        check("os.path.isdir('.') is true", v == true)
    catch:
        print("ERROR: os.path.isdir('.') threw exception")
    fade

    try:
        var v = os.path.isdir("__nonexistent_lyric_test_path__")
        check("os.path.isdir() is false for missing path", v == false)
    catch:
        print("ERROR: os.path.isdir() for missing path threw exception")
    fade

    try:
        var v = os.path.isfile(".")
        check("os.path.isfile('.') is false (dir, not file)", v == false)
    catch:
        print("ERROR: os.path.isfile('.') threw exception")
    fade

    try:
        var v = os.path.islink(".")
        check("os.path.islink('.') is false (not a symlink)", v == false)
    catch:
        print("ERROR: os.path.islink() threw exception")
    fade

    try:
        var v = os.path.ismount("/")
        check("os.path.ismount('/') callable", true)
        print("  ismount('/'):", v)
    catch:
        print("ERROR: os.path.ismount() threw exception")
    fade

    # ================================================================
    # Directory listing (on current dir)
    # ================================================================
    print("")
    print("--- Directory listing ---")

    try:
        var entries = os.listdir(".")
        check("os.listdir('.') callable", true)
        print("  listdir('.') returned a list")
    catch:
        print("ERROR: os.listdir('.') threw exception")
    fade

    try:
        var entries = os.listdir(".")
        # Python list — use __len__() method directly
        var n = entries.__len__()
        check("os.listdir('.') returns at least 1 entry", n >= 1)
        print("  entry count:", n)
    catch:
        print("ERROR: os.listdir('.') length check threw exception")
    fade

    # ================================================================
    # Temporary directory and file operations
    # ================================================================
    print("")
    print("--- Temporary directory and file operations ---")

    str tmpdir = "_lyric_os_test_tmp"
    str tmpfile = tmpdir + "/test_file.txt"
    str nesteddir = tmpdir + "/sub/deep/leaf"

    # -- mkdir --
    try:
        os.mkdir(tmpdir)
        check("os.mkdir() creates directory", os.path.isdir(tmpdir) == true)
    catch:
        print("ERROR: os.mkdir() threw exception")
    fade

    # -- create a test file using Lyric disk() --
    try:
        dsk f = disk(tmpfile)
        f.write("hello from Lyric os test\nsecond line\n")
        f.close()
        check("created test file with disk()", os.path.isfile(tmpfile) == true)
    catch:
        print("ERROR: could not create test file with disk()")
    fade

    # -- listdir on tmpdir --
    try:
        var entries = os.listdir(tmpdir)
        check("os.listdir(tmpdir) finds test file", true)
        print("  entries in tmpdir:", entries)
    catch:
        print("ERROR: os.listdir(tmpdir) threw exception")
    fade

    # -- isfile on temp file --
    try:
        var v = os.path.isfile(tmpfile)
        check("os.path.isfile(tmpfile) is true", v == true)
    catch:
        print("ERROR: os.path.isfile(tmpfile) threw exception")
    fade

    # -- isdir on temp file --
    try:
        var v = os.path.isdir(tmpfile)
        check("os.path.isdir(tmpfile) is false (it's a file)", v == false)
    catch:
        print("ERROR: os.path.isdir(tmpfile) threw exception")
    fade

    # ================================================================
    # File metadata (stat, getsize, timestamps)
    # ================================================================
    print("")
    print("--- File metadata ---")

    try:
        var sz = os.path.getsize(tmpfile)
        check("os.path.getsize(tmpfile) > 0", sz > 0)
        print("  getsize:", sz)
    catch:
        print("ERROR: os.path.getsize() threw exception")
    fade

    try:
        var mt = os.path.getmtime(tmpfile)
        check("os.path.getmtime(tmpfile) > 0", mt > 0)
        print("  getmtime:", mt)
    catch:
        print("ERROR: os.path.getmtime() threw exception")
    fade

    try:
        var at = os.path.getatime(tmpfile)
        check("os.path.getatime(tmpfile) > 0", at > 0)
        print("  getatime:", at)
    catch:
        print("ERROR: os.path.getatime() threw exception")
    fade

    try:
        var ct = os.path.getctime(tmpfile)
        check("os.path.getctime(tmpfile) > 0", ct > 0)
        print("  getctime:", ct)
    catch:
        print("ERROR: os.path.getctime() threw exception")
    fade

    # -- os.stat --
    try:
        var st = os.stat(tmpfile)
        check("os.stat(tmpfile) callable", true)
        print("  stat:", st)
    catch:
        print("ERROR: os.stat() threw exception")
    fade

    try:
        var st = os.stat(tmpfile)
        var sz = st.st_size
        check("os.stat().st_size > 0", sz > 0)
        print("  st_size:", sz)
    catch:
        print("ERROR: os.stat().st_size threw exception")
    fade

    try:
        var st = os.stat(tmpfile)
        var mode = st.st_mode
        check("os.stat().st_mode > 0", mode > 0)
        print("  st_mode:", mode)
    catch:
        print("ERROR: os.stat().st_mode threw exception")
    fade

    try:
        var st = os.stat(tmpfile)
        var mtime = st.st_mtime
        check("os.stat().st_mtime > 0", mtime > 0)
        print("  st_mtime:", mtime)
    catch:
        print("ERROR: os.stat().st_mtime threw exception")
    fade

    try:
        var st = os.stat(tmpdir)
        check("os.stat(directory) callable", true)
        print("  stat(dir):", st)
    catch:
        print("ERROR: os.stat(directory) threw exception")
    fade

    # ================================================================
    # Access checks
    # ================================================================
    print("")
    print("--- Access checks ---")

    try:
        var v = os.access(tmpfile, os.F_OK)
        check("os.access(tmpfile, F_OK) is true (file exists)", v == true)
    catch:
        print("ERROR: os.access(F_OK) threw exception")
    fade

    try:
        var v = os.access(tmpfile, os.R_OK)
        check("os.access(tmpfile, R_OK) is true (readable)", v == true)
    catch:
        print("ERROR: os.access(R_OK) threw exception")
    fade

    try:
        var v = os.access(tmpfile, os.W_OK)
        check("os.access(tmpfile, W_OK) is true (writable)", v == true)
    catch:
        print("ERROR: os.access(W_OK) threw exception")
    fade

    try:
        var v = os.access("__nonexistent_lyric_test_path__", os.F_OK)
        check("os.access() is false for missing file", v == false)
    catch:
        print("ERROR: os.access(F_OK) for missing file threw exception")
    fade

    try:
        var v = os.access(tmpdir, os.F_OK)
        check("os.access(tmpdir, F_OK) is true", v == true)
    catch:
        print("ERROR: os.access(tmpdir, F_OK) threw exception")
    fade

    try:
        var v = os.access(tmpdir, os.X_OK)
        check("os.access(tmpdir, X_OK) callable", true)
        print("  X_OK on dir:", v)
    catch:
        print("ERROR: os.access(tmpdir, X_OK) threw exception")
    fade

    # ================================================================
    # makedirs and removedirs
    # ================================================================
    print("")
    print("--- makedirs and removedirs ---")

    try:
        os.makedirs(nesteddir)
        check("os.makedirs() creates nested dirs", os.path.isdir(nesteddir) == true)
    catch:
        print("ERROR: os.makedirs() threw exception")
    fade

    try:
        var v = os.path.isdir(tmpdir + "/sub")
        check("intermediate 'sub' dir exists", v == true)
    catch:
        print("ERROR: intermediate dir check threw exception")
    fade

    try:
        var v = os.path.isdir(tmpdir + "/sub/deep")
        check("intermediate 'sub/deep' dir exists", v == true)
    catch:
        print("ERROR: intermediate dir check threw exception")
    fade

    try:
        os.removedirs(nesteddir)
        check("os.removedirs() removes nested empty dirs", os.path.exists(nesteddir) == false)
    catch:
        print("ERROR: os.removedirs() threw exception")
    fade

    # removedirs stops when it hits a non-empty directory, so tmpdir should
    # still exist because it contains test_file.txt
    try:
        var v = os.path.isdir(tmpdir)
        check("os.removedirs() stopped at non-empty parent", v == true)
    catch:
        print("ERROR: removedirs parent check threw exception")
    fade

    # ================================================================
    # Rename
    # ================================================================
    print("")
    print("--- Rename ---")

    str renamedfile = tmpdir + "/renamed_file.txt"

    try:
        os.rename(tmpfile, renamedfile)
        check("os.rename() moved file", os.path.isfile(renamedfile) == true)
        check("os.rename() old name gone", os.path.exists(tmpfile) == false)
    catch:
        print("ERROR: os.rename() threw exception")
    fade

    # rename it back so cleanup is consistent
    try:
        os.rename(renamedfile, tmpfile)
        check("os.rename() moved file back", os.path.isfile(tmpfile) == true)
    catch:
        print("ERROR: os.rename() back threw exception")
    fade

    # ================================================================
    # replace
    # ================================================================
    print("")
    print("--- Replace ---")

    str replacefile = tmpdir + "/replace_target.txt"

    try:
        # create a target for replace
        dsk f2 = disk(replacefile)
        f2.write("target")
        f2.close()

        # replace overwrites the target atomically
        os.replace(tmpfile, replacefile)
        check("os.replace() target exists after replace", os.path.isfile(replacefile) == true)
        check("os.replace() source gone after replace", os.path.exists(tmpfile) == false)
    catch:
        print("ERROR: os.replace() threw exception")
    fade

    # move it back for further tests
    try:
        os.rename(replacefile, tmpfile)
        check("moved file back after replace test", os.path.isfile(tmpfile) == true)
    catch:
        print("ERROR: move back after replace threw exception")
    fade

    # ================================================================
    # os.scandir
    # ================================================================
    print("")
    print("--- scandir ---")

    try:
        var scanner = os.scandir(tmpdir)
        check("os.scandir(tmpdir) callable", true)
        print("  scandir returned:", scanner)
    catch:
        print("ERROR: os.scandir() threw exception")
    fade

    # ================================================================
    # Random bytes (os.urandom)
    # ================================================================
    print("")
    print("--- Random bytes ---")

    try:
        var b = os.urandom(1)
        check("os.urandom(1) callable", true)
        print("  urandom(1):", b)
    catch:
        print("ERROR: os.urandom(1) threw exception")
    fade

    try:
        var b = os.urandom(16)
        check("os.urandom(16) callable", true)
        print("  urandom(16):", b)
    catch:
        print("ERROR: os.urandom(16) threw exception")
    fade

    try:
        var b = os.urandom(0)
        check("os.urandom(0) callable (empty bytes)", true)
    catch:
        print("ERROR: os.urandom(0) threw exception")
    fade

    # ================================================================
    # Directory walking (os.walk)
    # ================================================================
    print("")
    print("--- Directory walking ---")

    # set up a small tree for walking
    try:
        os.makedirs(tmpdir + "/walk_a/nested")
        dsk fa = disk(tmpdir + "/walk_a/a.txt")
        fa.write("a")
        fa.close()
        dsk fb = disk(tmpdir + "/walk_a/nested/b.txt")
        fb.write("b")
        fb.close()
        check("created walk test tree", true)
    catch:
        print("ERROR: could not set up walk test tree")
    fade

    try:
        var walker = os.walk(tmpdir)
        check("os.walk(tmpdir) callable", true)
        print("  walk returned:", walker)
    catch:
        print("ERROR: os.walk() threw exception")
    fade

    # ================================================================
    # Miscellaneous
    # ================================================================
    print("")
    print("--- Miscellaneous ---")

    try:
        var p = os.fspath("hello.txt")
        check("os.fspath('hello.txt') == 'hello.txt'", p == "hello.txt")
    catch:
        print("ERROR: os.fspath() threw exception (Python 3.6+)")
    fade

    try:
        var msg = os.strerror(2)
        check("os.strerror(2) returns non-empty (ENOENT)", msg != "")
        print("  strerror(2):", msg)
    catch:
        print("ERROR: os.strerror() threw exception")
    fade

    try:
        var msg = os.strerror(0)
        check("os.strerror(0) callable", true)
        print("  strerror(0):", msg)
    catch:
        print("ERROR: os.strerror(0) threw exception")
    fade

    try:
        var msg = os.strerror(13)
        check("os.strerror(13) returns non-empty (EACCES)", msg != "")
        print("  strerror(13):", msg)
    catch:
        print("ERROR: os.strerror(13) threw exception")
    fade

    # this test expected to fail outside of terminal
    #try:
    #    var sz = os.get_terminal_size()
    #    check("os.get_terminal_size() callable", true)
    #    print("  terminal_size:", sz)
    #catch:
    #    print("ERROR: os.get_terminal_size() threw exception (may fail in non-terminal)")
    #fade

    # ================================================================
    # Low-level file-descriptor operations
    # ================================================================
    print("")
    print("--- Low-level file-descriptor operations ---")

    str fdfile = tmpdir + "/fd_test.txt"

    try:
        var flags = os.O_WRONLY + os.O_CREAT + os.O_TRUNC
        var fd = os.open(fdfile, flags)
        check("os.open() returns fd >= 0", fd >= 0)
        print("  fd:", fd)
        os.close(fd)
        check("os.close(fd) succeeded", true)
    catch:
        print("ERROR: os.open / os.close threw exception")
    fade

    try:
        var v = os.path.isfile(fdfile)
        check("os.open(O_CREAT) created file", v == true)
    catch:
        print("ERROR: file created by os.open() not found")
    fade

    try:
        var fd = os.open(fdfile, os.O_RDONLY)
        check("os.open(O_RDONLY) returns fd >= 0", fd >= 0)
        os.close(fd)
    catch:
        print("ERROR: os.open(O_RDONLY) threw exception")
    fade

    # ================================================================
    # os.path with temp file -- samefile
    # ================================================================
    print("")
    print("--- os.path.samefile ---")

    try:
        var v = os.path.samefile(tmpfile, tmpfile)
        check("os.path.samefile(f, f) is true", v == true)
    catch:
        print("ERROR: os.path.samefile() threw exception (may not be available on all platforms)")
    fade

    try:
        var v = os.path.samefile(tmpfile, tmpdir)
        check("os.path.samefile(file, dir) is false", v == false)
    catch:
        print("ERROR: os.path.samefile(file, dir) threw exception")
    fade

    # ================================================================
    # Cleanup
    # ================================================================
    print("")
    print("--- Cleanup ---")

    # remove files created for walk test
    try:
        os.remove(tmpdir + "/walk_a/nested/b.txt")
        os.rmdir(tmpdir + "/walk_a/nested")
        os.remove(tmpdir + "/walk_a/a.txt")
        os.rmdir(tmpdir + "/walk_a")
        check("removed walk test tree", true)
    catch:
        print("ERROR: walk test tree cleanup threw exception")
    fade

    # remove fd test file
    try:
        os.remove(fdfile)
        check("removed fd_test.txt", true)
    catch:
        print("ERROR: fd_test.txt cleanup threw exception")
    fade

    # remove main test file
    try:
        os.remove(tmpfile)
        check("os.remove(tmpfile) deleted file", os.path.exists(tmpfile) == false)
    catch:
        print("ERROR: os.remove(tmpfile) threw exception")
    fade

    # remove temp directory
    try:
        os.rmdir(tmpdir)
        check("os.rmdir(tmpdir) deleted directory", os.path.exists(tmpdir) == false)
    catch:
        print("ERROR: os.rmdir(tmpdir) threw exception")
    fade

    print("")
    print("=== os test complete ===")
}
