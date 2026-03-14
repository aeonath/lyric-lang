#!/usr/bin/env python3
"""
Simple Python Performance Benchmark (Small)
Performs simple computations for timing comparison with Lyric.
"""

import time

def simple_add(a, b):
    return a + b

def simple_multiply(a, b):
    return a * b

def count_to_n(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

def main():
    print("Simple Python Performance Benchmark (Small)")
    print("=" * 40)

    start_time = time.time()

    # Simple function calls
    print("Performing simple function calls...")
    total = 0
    for i in range(1, 100001):  # 100,000
        result1 = simple_add(i, i)
        result2 = simple_multiply(i, 2)
        total += result1 + result2
    print(f"Function calls completed. Total: {total}")

    # Simple counting
    print("Performing counting operations...")
    count_result = count_to_n(10000)  # 10,000
    print(f"Count result: {count_result}")

    # Simple arithmetic loop
    print("Performing arithmetic operations...")
    arithmetic_sum = 0
    for i in range(1, 100001):  # 100,000
        arithmetic_sum += i * i
    print(f"Arithmetic sum: {arithmetic_sum}")

    end_time = time.time()
    execution_time = end_time - start_time

    print("\nResults Summary:")
    print(f"Execution time: {execution_time:.4f} seconds")

    return execution_time

if __name__ == "__main__":
    main()
