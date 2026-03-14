#!/usr/bin/env lyric

# Example demonstrating elif keyword in Lyric
def main() {
    var x = 2
    
    if x == 1:
        print("x is one")
    elif x == 2:
        print("x is two")
    elif x == 3:
        print("x is three")
    else:
        print("x is something else")
    end
    
    # Test with elif syntax
    var y = 0
    if y > 0:
        print("positive")
    elif y < 0:
        print("negative")
    else:
        print("zero")
    end
}

main()
