# test_lyric.ly
# Lyric adhoc test -- exercises every public function in the lyric standard library.
#
# Run with:  lyric run lyric/tests/lib/test_lyric.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions

import lyric

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
    print("=== Lyric standard library test ===")
    print("")

    # ================================================================
    # pwd() — print working directory
    # ================================================================
    print("--- pwd ---")

    try:
        var cwd = lyric.pwd()
        check("pwd() returns non-empty string", cwd != "")
        check("pwd() returns a string", cwd.len() > 0)
        print("  cwd:", cwd)
    catch Error as e:
        print("ERROR: pwd() threw exception:", e)
    fade

    # ================================================================
    # exists() — check file/dir existence
    # ================================================================
    print("")
    print("--- exists ---")

    try:
        var v = lyric.exists(".")
        check("exists('.') is true", v == true)
    catch Error as e:
        print("ERROR: exists('.') threw exception:", e)
    fade

    try:
        var v = lyric.exists("__nonexistent_lyric_test_xyz__")
        check("exists() is false for missing path", v == false)
    catch Error as e:
        print("ERROR: exists() for missing path threw exception:", e)
    fade

    # ================================================================
    # isfile() / isdir()
    # ================================================================
    print("")
    print("--- isfile / isdir ---")

    try:
        var v = lyric.isdir(".")
        check("isdir('.') is true", v == true)
    catch Error as e:
        print("ERROR: isdir('.') threw exception:", e)
    fade

    try:
        var v = lyric.isfile(".")
        check("isfile('.') is false (directory, not file)", v == false)
    catch Error as e:
        print("ERROR: isfile('.') threw exception:", e)
    fade

    try:
        var v = lyric.isdir("__nonexistent__")
        check("isdir() is false for missing path", v == false)
    catch Error as e:
        print("ERROR: isdir() for missing path threw exception:", e)
    fade

    try:
        var v = lyric.isfile("__nonexistent__")
        check("isfile() is false for missing path", v == false)
    catch Error as e:
        print("ERROR: isfile() for missing path threw exception:", e)
    fade

    # ================================================================
    # join() — path joining
    # ================================================================
    print("")
    print("--- join ---")

    try:
        var p = lyric.join("usr", "local")
        check("join('usr', 'local') returns non-empty", p != "")
        check("join('usr', 'local') contains both parts", p.len() > 3)
        print("  join:", p)
    catch Error as e:
        print("ERROR: join() threw exception:", e)
    fade

    try:
        var p = lyric.join("a", "b")
        check("join('a', 'b') non-empty", p.len() > 0)
        print("  join('a','b'):", p)
    catch Error as e:
        print("ERROR: join('a','b') threw exception:", e)
    fade

    # ================================================================
    # path() — absolute path
    # ================================================================
    print("")
    print("--- path ---")

    try:
        var p = lyric.path(".")
        check("path('.') returns non-empty", p != "")
        check("path('.') returns long path", p.len() > 1)
        print("  path('.'):", p)
    catch Error as e:
        print("ERROR: path('.') threw exception:", e)
    fade

    try:
        var p = lyric.path("somefile.txt")
        str raw = "somefile.txt"
        check("path('somefile.txt') returns absolute", p.len() > raw.len())
        print("  path('somefile.txt'):", p)
    catch Error as e:
        print("ERROR: path('somefile.txt') threw exception:", e)
    fade

    # ================================================================
    # base() — basename
    # ================================================================
    print("")
    print("--- base ---")

    try:
        var b = lyric.base("/home/user/file.txt")
        check("base('/home/user/file.txt') == 'file.txt'", b == "file.txt")
    catch Error as e:
        print("ERROR: base() threw exception:", e)
    fade

    try:
        var b = lyric.base("file.txt")
        check("base('file.txt') == 'file.txt'", b == "file.txt")
    catch Error as e:
        print("ERROR: base('file.txt') threw exception:", e)
    fade

    try:
        var b = lyric.base("/just/a/dir/")
        check("base('/just/a/dir/') == '' (trailing slash)", b == "")
    catch Error as e:
        print("ERROR: base() trailing slash threw exception:", e)
    fade

    # ================================================================
    # dir() — dirname
    # ================================================================
    print("")
    print("--- dir ---")

    try:
        var d = lyric.dir("/home/user/file.txt")
        check("dir('/home/user/file.txt') returns non-empty", d != "")
        print("  dir:", d)
    catch Error as e:
        print("ERROR: dir() threw exception:", e)
    fade

    try:
        var d = lyric.dir("file.txt")
        check("dir('file.txt') == '' (no directory part)", d == "")
    catch Error as e:
        print("ERROR: dir('file.txt') threw exception:", e)
    fade

    # ================================================================
    # env() — get environment variable
    # ================================================================
    print("")
    print("--- env ---")

    try:
        var p = lyric.env("PATH")
        check("env('PATH') returns non-empty", p != "" and p != None)
    catch Error as e:
        print("ERROR: env('PATH') threw exception:", e)
    fade

    try:
        var v = lyric.env("LYRIC_NONEXISTENT_VAR_99")
        check("env() returns None for missing var", v == None)
    catch Error as e:
        print("ERROR: env() for missing var threw exception:", e)
    fade

    # ================================================================
    # set() — set environment variable
    # ================================================================
    print("")
    print("--- set ---")

    try:
        lyric.set("LYRIC_TEST_VAR", "hello_lyric")
        var v = lyric.env("LYRIC_TEST_VAR")
        check("set() then env() returns the value", v == "hello_lyric")
    catch Error as e:
        print("ERROR: set()/env() threw exception:", e)
    fade

    try:
        lyric.set("LYRIC_TEST_VAR", "updated")
        var v = lyric.env("LYRIC_TEST_VAR")
        check("set() overwrites existing var", v == "updated")
    catch Error as e:
        print("ERROR: set() overwrite threw exception:", e)
    fade

    # ================================================================
    # pid() — process id
    # ================================================================
    print("")
    print("--- pid ---")

    try:
        var p = lyric.pid()
        check("pid() > 0", p > 0)
        print("  pid:", p)
    catch Error as e:
        print("ERROR: pid() threw exception:", e)
    fade

    # ================================================================
    # now() — unix timestamp
    # ================================================================
    print("")
    print("--- now ---")

    try:
        var t = lyric.now()
        check("now() > 1000000000 (after 2001)", t > 1000000000)
        print("  now:", t)
    catch Error as e:
        print("ERROR: now() threw exception:", e)
    fade

    try:
        var t1 = lyric.now()
        var t2 = lyric.now()
        check("now() is non-decreasing", t2 >= t1)
    catch Error as e:
        print("ERROR: now() ordering threw exception:", e)
    fade

    # ================================================================
    # date() — returns (date, time) tuple
    # ================================================================
    print("")
    print("--- date ---")

    try:
        tup d = lyric.date()
        check("date() returns a tuple", true)
        print("  date:", d)
    catch Error as e:
        print("ERROR: date() threw exception:", e)
    fade

    try:
        tup d = lyric.date()
        str datepart = d[0]
        str timepart = d[1]
        check("date()[0] is 10-char date string", datepart.len() == 10)
        check("date()[1] is 8-char time string", timepart.len() == 8)
        print("  date part:", datepart)
        print("  time part:", timepart)
    catch Error as e:
        print("ERROR: date() tuple access threw exception:", e)
    fade

    # ================================================================
    # datefmt() — formatted date string
    # ================================================================
    print("")
    print("--- datefmt ---")

    try:
        str s = lyric.datefmt("%Y")
        check("datefmt('%Y') returns 4-char year", s.len() == 4)
        print("  year:", s)
    catch Error as e:
        print("ERROR: datefmt('%Y') threw exception:", e)
    fade

    try:
        str s = lyric.datefmt("%Y-%m-%d")
        check("datefmt('%Y-%m-%d') returns 10-char date", s.len() == 10)
        print("  date:", s)
    catch Error as e:
        print("ERROR: datefmt('%Y-%m-%d') threw exception:", e)
    fade

    try:
        str s = lyric.datefmt("%H:%M:%S")
        check("datefmt('%H:%M:%S') returns 8-char time", s.len() == 8)
        print("  time:", s)
    catch Error as e:
        print("ERROR: datefmt('%H:%M:%S') threw exception:", e)
    fade

    # ================================================================
    # randflt() — random float between 0.0 and 1.0
    # ================================================================
    print("")
    print("--- randflt ---")

    try:
        var r = lyric.randflt()
        check("randflt() >= 0.0 and < 1.0", r >= 0.0 and r < 1.0)
        print("  randflt:", r)
    catch Error as e:
        print("ERROR: randflt() threw exception:", e)
    fade

    try:
        # call multiple times to check range
        var r1 = lyric.randflt()
        var r2 = lyric.randflt()
        var r3 = lyric.randflt()
        var r4 = lyric.randflt()
        var r5 = lyric.randflt()
        god ok1 = r1 >= 0.0 and r1 < 1.0
        god ok2 = r2 >= 0.0 and r2 < 1.0
        god ok3 = r3 >= 0.0 and r3 < 1.0
        god ok4 = r4 >= 0.0 and r4 < 1.0
        god ok5 = r5 >= 0.0 and r5 < 1.0
        check("randflt() x5 all in [0.0, 1.0)", ok1 and ok2 and ok3 and ok4 and ok5)
    catch Error as e:
        print("ERROR: randflt() x5 threw exception:", e)
    fade

    # ================================================================
    # randint() — random integer in range
    # ================================================================
    print("")
    print("--- randint ---")

    try:
        var r = lyric.randint(1, 10)
        check("randint(1, 10) >= 1 and <= 10", r >= 1 and r <= 10)
        print("  randint(1,10):", r)
    catch Error as e:
        print("ERROR: randint() threw exception:", e)
    fade

    try:
        var r = lyric.randint(5, 5)
        check("randint(5, 5) == 5", r == 5)
    catch Error as e:
        print("ERROR: randint(5,5) threw exception:", e)
    fade

    try:
        var r = lyric.randint(-100, -50)
        check("randint(-100, -50) in range", r >= -100 and r <= -50)
        print("  randint(-100,-50):", r)
    catch Error as e:
        print("ERROR: randint(-100,-50) threw exception:", e)
    fade

    try:
        var r1 = lyric.randint(1, 3)
        var r2 = lyric.randint(1, 3)
        var r3 = lyric.randint(1, 3)
        var r4 = lyric.randint(1, 3)
        var r5 = lyric.randint(1, 3)
        god ok1 = r1 >= 1 and r1 <= 3
        god ok2 = r2 >= 1 and r2 <= 3
        god ok3 = r3 >= 1 and r3 <= 3
        god ok4 = r4 >= 1 and r4 <= 3
        god ok5 = r5 >= 1 and r5 <= 3
        check("randint(1,3) x5 all in [1,3]", ok1 and ok2 and ok3 and ok4 and ok5)
    catch Error as e:
        print("ERROR: randint() x5 threw exception:", e)
    fade

    # ================================================================
    # randarr() — random element from array
    # ================================================================
    print("")
    print("--- randarr ---")

    try:
        arr items = ["a", "b", "c"]
        var r = lyric.randarr(items)
        check("randarr() returns element from array", r == "a" or r == "b" or r == "c")
        print("  randarr:", r)
    catch Error as e:
        print("ERROR: randarr() threw exception:", e)
    fade

    try:
        arr nums = [42]
        var r = lyric.randarr(nums)
        check("randarr() from single-element array == 42", r == 42)
    catch Error as e:
        print("ERROR: randarr() single element threw exception:", e)
    fade

    # ================================================================
    # sleep() — pause execution
    # ================================================================
    print("")
    print("--- sleep ---")

    try:
        lyric.sleep(0.05)
        check("sleep(0.05) completed without error", true)
    catch Error as e:
        print("ERROR: sleep() threw exception:", e)
    fade

    try:
        lyric.sleep(0)
        check("sleep(0) completed without error", true)
    catch Error as e:
        print("ERROR: sleep(0) threw exception:", e)
    fade

    # ================================================================
    # ls() — list directory / glob
    # ================================================================
    print("")
    print("--- ls ---")

    try:
        arr entries = lyric.ls(".")
        check("ls('.') returns a list", entries.len() >= 0)
        check("ls('.') returns at least 1 entry", entries.len() > 0)
        print("  ls('.') count:", entries.len())
    catch Error as e:
        print("ERROR: ls('.') threw exception:", e)
    fade

    try:
        arr entries = lyric.ls("..")
        check("ls('..') returns a list", entries.len() >= 0)
    catch Error as e:
        print("ERROR: ls('..') threw exception:", e)
    fade

    try:
        arr entries = lyric.ls("*.ly")
        check("ls('*.ly') returns a list", entries.len() >= 0)
        print("  ls('*.ly') count:", entries.len())
    catch Error as e:
        print("ERROR: ls('*.ly') threw exception:", e)
    fade

    # ================================================================
    # mkdir / rmdir — directory creation and removal
    # ================================================================
    print("")
    print("--- mkdir / rmdir ---")

    str testdir = "_lyric_lib_test_tmp"

    try:
        lyric.mkdir(testdir)
        check("mkdir() creates directory", lyric.isdir(testdir) == true)
        check("mkdir() directory exists", lyric.exists(testdir) == true)
    catch Error as e:
        print("ERROR: mkdir() threw exception:", e)
    fade

    try:
        lyric.rmdir(testdir)
        check("rmdir() removes directory", lyric.exists(testdir) == false)
    catch Error as e:
        print("ERROR: rmdir() threw exception:", e)
    fade

    # ================================================================
    # cd() — change directory
    # ================================================================
    print("")
    print("--- cd ---")

    try:
        var original = lyric.pwd()
        lyric.mkdir(testdir)
        lyric.cd(testdir)
        var newcwd = lyric.pwd()
        check("cd() changes working directory", newcwd != original)
        print("  changed to:", newcwd)
        lyric.cd(original)
        lyric.rmdir(testdir)
        check("cd() back to original", lyric.pwd() == original)
    catch Error as e:
        print("ERROR: cd() threw exception:", e)
        # attempt cleanup
        try:
            lyric.cd(lyric.path("."))
            lyric.rmdir(testdir)
        catch:
        fade
    fade

    # ================================================================
    # rm() — remove file
    # ================================================================
    print("")
    print("--- rm ---")

    str testfile = "_lyric_lib_test_file.txt"

    try:
        dsk f = disk(testfile)
        f.write("test content")
        f.close()
        check("created test file", lyric.isfile(testfile) == true)

        lyric.rm(testfile)
        check("rm() removes file", lyric.exists(testfile) == false)
    catch Error as e:
        print("ERROR: rm() threw exception:", e)
        # attempt cleanup
        try:
            lyric.rm(testfile)
        catch:
        fade
    fade

    # ================================================================
    # Integration: mkdir + disk + isfile + rm + rmdir
    # ================================================================
    print("")
    print("--- Integration: file ops ---")

    str intdir = "_lyric_lib_int_test"
    str intfile = "_lyric_lib_int_test/data.txt"

    try:
        lyric.mkdir(intdir)
        check("created integration test dir", lyric.isdir(intdir))

        dsk f = disk(intfile)
        f.write("integration test data")
        f.close()
        check("created file inside test dir", lyric.isfile(intfile))

        # verify join + base + dir work on the path
        str b = lyric.base(intfile)
        check("base() of test file == 'data.txt'", b == "data.txt")

        str d = lyric.dir(intfile)
        check("dir() of test file is non-empty", d != "")

        # cleanup
        lyric.rm(intfile)
        check("rm() cleaned up file", lyric.exists(intfile) == false)
        lyric.rmdir(intdir)
        check("rmdir() cleaned up dir", lyric.exists(intdir) == false)
    catch Error as e:
        print("ERROR: integration test threw exception:", e)
        # attempt cleanup
        try:
            lyric.rm(intfile)
        catch:
        fade
        try:
            lyric.rmdir(intdir)
        catch:
        fade
    fade

    # ================================================================
    # Summary
    # ================================================================
    print("")
    print("=== lyric library test complete ===")
}
