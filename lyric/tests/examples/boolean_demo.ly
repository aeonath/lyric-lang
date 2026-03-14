def main() {
    print("Testing Boolean and Comparison Operations in Lyric")
    
    # Test comparison operators
    print("\n=== Comparison Operators ===")
    var x = 5
    var y = 3
    
    if x == 5
        print("x equals 5")
    end
    
    if x != 3
        print("x does not equal 3")
    end
    
    if x > 3
        print("x is greater than 3")
    end
    
    if x >= 5
        print("x is greater than or equal to 5")
    end
    
    if y < 5
        print("y is less than 5")
    end
    
    if y <= 3
        print("y is less than or equal to 3")
    end
    
    # Test logical operators
    print("\n=== Logical Operators ===")
    var a = 10
    var b = 0
    
    if a > 0 and b == 0
        print("Both conditions true: a > 0 and b == 0")
    end
    
    if a == 0 or b == 0
        print("At least one condition true: a == 0 or b == 0")
    end
    
    if not (a == 0)
        print("a is not zero")
    end
    
    # Test truthiness rules
    print("\n=== Truthiness Rules ===")
    
    # Numbers
    if 5
        print("5 is truthy")
    end
    
    if not 0
        print("0 is falsy")
    end
    
    # Strings
    if "hello"
        print("non-empty string is truthy")
    end
    
    if not ""
        print("empty string is falsy")
    end
    
    # Boolean literals
    if true
        print("true is truthy")
    end
    
    if not false
        print("false is falsy")
    end
    
    # Test range with comparisons
    print("\n=== Range with Comparisons ===")
    for i in range(3)
        if i == 0
            print("First iteration")
        elif i == 1
            print("Second iteration")
        else
            print("Third iteration")
        end
    done
    
    # Test complex boolean expressions
    print("\n=== Complex Boolean Expressions ===")
    var p = 5
    var q = 3
    var r = 0
    
    if p > q and q > r
        print("p > q and q > r")
    end
    
    if p == 5 or q == 5
        print("p or q equals 5")
    end
    
    if not (p == 0 and q == 0)
        print("not (p == 0 and q == 0)")
    end
}