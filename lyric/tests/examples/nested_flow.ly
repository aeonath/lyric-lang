def main() {
    print("Testing nested control flow in Lyric")
    
    # Test nested if statements
    var x = 5
    if x > 0:
        print("x is positive")
        if x > 3:
            print("x is greater than 3")
        else:
            print("x is 3 or less")
        end
    else:
        print("x is not positive")
    end
    
    # Test nested loops
    print("\nTesting nested loops:")
    int i
    int j
    for i in range(2):
        print("Outer loop:", i)
        for j in range(2):
            print("  Inner loop:", j)
        done
    done
    
    # Test if statements inside loops
    print("\nTesting if statements inside loops:")
    for i in range(3):
        if i == 0:
            print("First iteration")
        elif i == 1:
            print("Second iteration")
        else:
            print("Third iteration")
        end
    done
    
    # Test complex nested structure
    print("\nTesting complex nested structure:")
    var y = 2
    if x > 0:
        print("x is positive")
        if y > 1:
            print("y is greater than 1")
            for i in range(2):
                print("Loop iteration:", i)
                if i == 0:
                    print("  First loop iteration")
                else:
                    print("  Second loop iteration")
                end
            done
        else:
            print("y is not greater than 1")
        end
    else:
        print("x is not positive")
    end
}