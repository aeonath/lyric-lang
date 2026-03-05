var cleanup_done = False
var x = 10
var counter = 0

def risky_function(int divisor) {
    if divisor == 0:
        raise ZeroDivisionErrorLyric
    end
    return 10 / divisor
}

def safe_divide(int a, int b) {
    try:
        return a / b
    catch:
        print("Division failed, returning 0")
        return 0
    finally:
        print("Division attempt completed")
    fade
}

class Calculator
    def divide(int a, int b) {
        try:
            return a / b
        catch:
            print("Division error in calculator")
            return 0
        fade
    }
+++

def main() {
    # Exception Handling Tests for Sprint 3
    # Tests try/catch/finally blocks and raise statements
    
    # Test 1: Basic try/catch
    try:
        var result1 = 10 / 0
    catch:
        print("Caught division by zero error")
    fade
    
    # Test 2: Try/catch with finally
    var result2 = 10 / 2
    try:
        print("Division successful:", result2)
    catch:
        print("Caught an error")
    finally:
        cleanup_done = True
        print("Cleanup completed")
    fade
    
    # Test 3: Try/catch with variable access
    try:
        var y = x / 0
    catch:
        x = 20  # Modify variable in catch block
    finally:
        print("Final x value:", x)
    fade
    
    # Test 7: Multiple statements in try block
    try:
        var result3 = 10 / 0
        counter = counter + 1
        counter = counter + 1
    catch:
        counter = counter + 10
    finally:
        counter = counter + 100
    fade
    
    # Test 8: Exception with method calls
    var calc = Calculator()
    var result4 = calc.divide(10, 0)
    
    # Test 10: Exception with indexing
    try:
        var numbers = [1, 2, 3]
        var index_result = numbers[10]
    catch:
        print("Caught index error")
    fade
}
