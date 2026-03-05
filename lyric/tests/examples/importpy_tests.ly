
importpy math

var r = math.sqrt(9)

var pi = math.pi

var sin_result = math.sin(0)

importpy datetime

var now = datetime.datetime.now()

var today = datetime.date.today()

var datetime_module = datetime.datetime
var now_method = datetime_module.now
var current_time = now_method()

importpy os

var current_dir = os.getcwd()

var math_functions = [math.sqrt, math.sin, math.cos]

var math_obj = math
var datetime_obj = datetime

def test_pyobject_param(var func, var value) {
    return func(value)
}

var result1 = test_pyobject_param(math.sqrt, 16)

var result2 = test_pyobject_param(math.sin, math.pi/2)

def get_math_function() {
    return math.sqrt
}

var sqrt_func = get_math_function()
var result3 = sqrt_func(25)

var math_constants = {
}


var i = 0
    var angle = i * math.pi / 2
    var sin_val = math.sin(angle)


def main() {
    # ImportPy Integration Tests
    # Tests the importpy functionality with various Python modules
    # Basic math module test
    print(r)        # expect 3.0 (pyobject okay with var)
    print(pi)       # expect 3.141592653589793
    print(sin_result)  # expect 0.0
    # DateTime module test
    print(now.year) # prints current year
    print(today)    # prints current date
    # Test chained member access
    print(current_time.year)
    # Test with multiple modules
    print(current_dir)
    # Test error handling (this should work without errors)
    print("Math functions available")
    # Test pyobject type integration
    print("Objects imported successfully")
    # Test function calls with pyobject parameters
    print(result1)  # expect 4.0
    print(result2)  # expect 1.0
    # Test return values
    print(result3)  # expect 5.0
    # Test nested access
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau
    print(math_constants.pi)
    # Test with conditional logic
    if math.pi > 3:
        print("Pi is greater than 3")
    else:
        print("Pi is not greater than 3")
    end
    # Test in loops
    given i < 3:
        print(sin_val)
        i = i + 1
    done
    print("All importpy tests completed successfully!")
}
