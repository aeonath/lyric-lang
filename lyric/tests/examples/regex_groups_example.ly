
rex title = regex("/<title>(.*?)</title>/")
var match = title.search("<title>Hello</title>")

def main() {
    # Regex Group Handling Example
    # This demonstrates the regex group functionality from Sprint 7 Task 2
    if match:
        print match.group(1)
    else:
        print "No match found"
    end
}
