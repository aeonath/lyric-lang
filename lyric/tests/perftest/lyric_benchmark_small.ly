#!/usr/bin/env lyric
# Simple Lyric Performance Benchmark (Small)

importpy time

def simple_add(int a, int b) {
    return a + b
}

def simple_multiply(int a, int b) {
    return a * b
}

def count_to_n(int n) {
    var sum = 0
    var i = 1
    given i <= n:
        sum = sum + i
        i = i + 1
    done
    return sum
}

def main() {
    print("Simple Lyric Performance Benchmark (Small)")
    print("=" * 40)

    var start_time = time.time()

    # Simple function calls
    print("Performing simple function calls...")
    var total = 0
    var i
    var result1
    var result2
    i = 1
    given i <= 100000:
        result1 = simple_add(i, i)
        result2 = simple_multiply(i, 2)
        total = total + result1 + result2
        i = i + 1
    done
    print("Function calls completed. Total:", total)

    # Simple counting
    print("Performing counting operations...")
    var count_result = count_to_n(10000)
    print("Count result:", count_result)

    # Simple arithmetic loop
    print("Performing arithmetic operations...")
    var arithmetic_sum = 0
    i = 1
    given i <= 100000:
        arithmetic_sum = arithmetic_sum + i * i
        i = i + 1
    done
    print("Arithmetic sum:", arithmetic_sum)

    var end_time = time.time()
    var execution_time = end_time - start_time

    print("")
    print("Results Summary:")
    print("Execution time:", execution_time, "seconds")
}
