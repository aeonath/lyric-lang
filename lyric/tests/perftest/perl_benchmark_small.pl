#!/usr/bin/env perl
# Simple Perl Performance Benchmark (Small)
# Performs simple computations for timing comparison with Lyric.

use strict;
use warnings;
use Time::HiRes qw(time);

sub simple_add {
    my ($a, $b) = @_;
    return $a + $b;
}

sub simple_multiply {
    my ($a, $b) = @_;
    return $a * $b;
}

sub count_to_n {
    my ($n) = @_;
    my $total = 0;
    my $i = 1;
    while ($i <= $n) {
        $total += $i;
        $i += 1;
    }
    return $total;
}

sub main {
    print "Simple Perl Performance Benchmark (Small)\n";
    print "=" x 40, "\n";

    my $start_time = time();

    # Simple function calls
    print "Performing simple function calls...\n";
    my $total = 0;
    my $i = 1;
    while ($i <= 100000) {
        my $result1 = simple_add($i, $i);
        my $result2 = simple_multiply($i, 2);
        $total += $result1 + $result2;
        $i += 1;
    }
    print "Function calls completed. Total: $total\n";

    # Simple counting
    print "Performing counting operations...\n";
    my $count_result = count_to_n(10000);
    print "Count result: $count_result\n";

    # Simple arithmetic loop
    print "Performing arithmetic operations...\n";
    my $arithmetic_sum = 0;
    $i = 1;
    while ($i <= 100000) {
        $arithmetic_sum += $i * $i;
        $i += 1;
    }
    print "Arithmetic sum: $arithmetic_sum\n";

    my $end_time = time();
    my $execution_time = $end_time - $start_time;

    print "\n";
    print "Results Summary:\n";
    printf "Execution time: %.4f seconds\n", $execution_time;
}

main();
