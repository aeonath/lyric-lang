# test_all.ly
# Runs every core_*.ly script in this directory, counts PASS / ERROR lines
# in each, and prints a summary table.
#
# Run with:  lyric run lyric/tests/python_modules/test_all.ly

importpy os

def main() {
    str dir = "."
    var files = os.listdir(dir)
    var n = files.__len__()

    # collect only .ly scripts (skip ourselves), sorted
    arr scripts = []
    var f = ""
    for i in range(n)
        f = files[i]
        if ".ly" in f
            if f != "test_all.ly"
                scripts.append(f)
            end
        end
    done
    scripts.sort()

    int total_pass  = 0
    int total_error = 0
    int total_scripts = scripts.len()

    rex re_pass  = regex("PASS:")
    rex re_error = regex("ERROR:")

    print("=" * 60)
    print("  Lyric Python-Module Test Runner")
    print("=" * 60)
    print("")

    # pre-declare loop variables (Lyric scoping: no redeclaration)
    str cmd    = ""
    str output = ""
    var passes = None
    var errors = None
    int p = 0
    int e = 0
    str tag   = ""

    for s in scripts
        cmd = "lyric run " + dir + "/" + s
        output = ""
        exec(cmd) -> output

        # findall returns a Python list; convert to arr for .len()
        passes = arr(re_pass.findall(output))
        errors = arr(re_error.findall(output))
        p = passes.len()
        e = errors.len()

        total_pass  = total_pass  + p
        total_error = total_error + e

        tag = "OK"
        if e > 0
            tag = "<<<"
        end

        print("  " + s, " | ", str(p) + " pass, " + str(e) + " error", " | " + tag)
    done

    print("")
    print("-" * 60)
    print("  Scripts : " + str(total_scripts))
    print("  PASS    : " + str(total_pass))
    print("  ERROR   : " + str(total_error))
    print("-" * 60)

    if total_error == 0
        print("  All tests passed!")
    else
        print("  Some tests reported errors.")
    end

    print("")
}
