#!/usr/bin/env ruby
# Simple Ruby Performance Benchmark
# Performs simple computations for timing comparison with Lyric.

def simple_add(a, b)
  a + b
end

def simple_multiply(a, b)
  a * b
end

def count_to_n(n)
  total = 0
  i = 1
  while i <= n
    total += i
    i += 1
  end
  total
end

def main()
  puts "Simple Ruby Performance Benchmark"
  puts "=" * 40

  start_time = Time.now

  # Simple function calls
  puts "Performing simple function calls..."
  total = 0
  i = 1
  while i <= 10000000
    result1 = simple_add(i, i)
    result2 = simple_multiply(i, 2)
    total += result1 + result2
    i += 1
  end
  puts "Function calls completed. Total: #{total}"

  # Simple counting
  puts "Performing counting operations..."
  count_result = count_to_n(1000000)
  puts "Count result: #{count_result}"

  # Simple arithmetic loop
  puts "Performing arithmetic operations..."
  arithmetic_sum = 0
  i = 1
  while i <= 10000000
    arithmetic_sum += i * i
    i += 1
  end
  puts "Arithmetic sum: #{arithmetic_sum}"

  end_time = Time.now
  execution_time = end_time - start_time

  puts ""
  puts "Results Summary:"
  puts "Execution time: #{format('%.4f', execution_time)} seconds"
end

main()
