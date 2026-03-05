# core_math.ly
# Lyric adhoc test -- exercises every public function and constant of Python's math module.
#
# Run with:  lyric run lyric/tests/python_modules/core_math.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions

importpy math

# -----------------------------------------------------------------------
# Helper: print PASS or ERROR based on a condition
# -----------------------------------------------------------------------
def check(var label, var cond) {
    if cond
        print("PASS:", label)
    else
        print("ERROR:", label)
    end
}

def main() {
    print("=== Lyric math module adhoc test ===")
    print("")

    # ================================================================
    # Constants
    # ================================================================
    print("--- Constants ---")

    try:
        var pi = math.pi
        check("math.pi exists", true)
        check("math.pi > 3.14 and < 3.15", pi > 3.14 and pi < 3.15)
        print("  math.pi:", pi)
    catch:
        print("ERROR: math.pi threw exception")
    fade

    try:
        var e = math.e
        check("math.e exists", true)
        check("math.e > 2.71 and < 2.72", e > 2.71 and e < 2.72)
        print("  math.e:", e)
    catch:
        print("ERROR: math.e threw exception")
    fade

    try:
        var tau = math.tau
        check("math.tau exists", true)
        check("math.tau > 6.28 and < 6.29", tau > 6.28 and tau < 6.29)
        print("  math.tau:", tau)
    catch:
        print("ERROR: math.tau threw exception")
    fade

    try:
        var inf = math.inf
        check("math.inf exists", true)
        check("math.inf > 999999999999.0", inf > 999999999999.0)
        print("  math.inf:", inf)
    catch:
        print("ERROR: math.inf threw exception")
    fade

    try:
        var nan = math.nan
        check("math.nan exists", true)
        print("  math.nan:", nan)
    catch:
        print("ERROR: math.nan threw exception")
    fade

    # ================================================================
    # Rounding and truncation
    # ================================================================
    print("")
    print("--- Rounding and truncation ---")

    try:
        var v = math.ceil(4.2)
        check("math.ceil(4.2) == 5", v == 5)
    catch:
        print("ERROR: math.ceil(4.2) threw exception")
    fade

    try:
        var v = math.ceil(-4.2)
        check("math.ceil(-4.2) == -4", v == -4)
    catch:
        print("ERROR: math.ceil(-4.2) threw exception")
    fade

    try:
        var v = math.ceil(5.0)
        check("math.ceil(5.0) == 5", v == 5)
    catch:
        print("ERROR: math.ceil(5.0) threw exception")
    fade

    try:
        var v = math.floor(4.7)
        check("math.floor(4.7) == 4", v == 4)
    catch:
        print("ERROR: math.floor(4.7) threw exception")
    fade

    try:
        var v = math.floor(-4.7)
        check("math.floor(-4.7) == -5", v == -5)
    catch:
        print("ERROR: math.floor(-4.7) threw exception")
    fade

    try:
        var v = math.floor(5.0)
        check("math.floor(5.0) == 5", v == 5)
    catch:
        print("ERROR: math.floor(5.0) threw exception")
    fade

    try:
        var v = math.trunc(4.9)
        check("math.trunc(4.9) == 4", v == 4)
    catch:
        print("ERROR: math.trunc(4.9) threw exception")
    fade

    try:
        var v = math.trunc(-4.9)
        check("math.trunc(-4.9) == -4", v == -4)
    catch:
        print("ERROR: math.trunc(-4.9) threw exception")
    fade

    try:
        var v = math.trunc(0.0)
        check("math.trunc(0.0) == 0", v == 0)
    catch:
        print("ERROR: math.trunc(0.0) threw exception")
    fade

    # ================================================================
    # Absolute value (float)
    # ================================================================
    print("")
    print("--- Absolute value ---")

    try:
        var v = math.fabs(-5.0)
        check("math.fabs(-5.0) == 5.0", v == 5.0)
    catch:
        print("ERROR: math.fabs(-5.0) threw exception")
    fade

    try:
        var v = math.fabs(3.14)
        check("math.fabs(3.14) == 3.14", v == 3.14)
    catch:
        print("ERROR: math.fabs(3.14) threw exception")
    fade

    try:
        var v = math.fabs(0.0)
        check("math.fabs(0.0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.fabs(0.0) threw exception")
    fade

    # ================================================================
    # Factorial
    # ================================================================
    print("")
    print("--- Factorial ---")

    try:
        var v = math.factorial(0)
        check("math.factorial(0) == 1", v == 1)
    catch:
        print("ERROR: math.factorial(0) threw exception")
    fade

    try:
        var v = math.factorial(1)
        check("math.factorial(1) == 1", v == 1)
    catch:
        print("ERROR: math.factorial(1) threw exception")
    fade

    try:
        var v = math.factorial(5)
        check("math.factorial(5) == 120", v == 120)
    catch:
        print("ERROR: math.factorial(5) threw exception")
    fade

    try:
        var v = math.factorial(10)
        check("math.factorial(10) == 3628800", v == 3628800)
    catch:
        print("ERROR: math.factorial(10) threw exception")
    fade

    try:
        var v = math.factorial(12)
        check("math.factorial(12) == 479001600", v == 479001600)
    catch:
        print("ERROR: math.factorial(12) threw exception")
    fade

    # ================================================================
    # GCD and LCM
    # ================================================================
    print("")
    print("--- GCD and LCM ---")

    try:
        var v = math.gcd(12, 8)
        check("math.gcd(12, 8) == 4", v == 4)
    catch:
        print("ERROR: math.gcd(12, 8) threw exception")
    fade

    try:
        var v = math.gcd(100, 75)
        check("math.gcd(100, 75) == 25", v == 25)
    catch:
        print("ERROR: math.gcd(100, 75) threw exception")
    fade

    try:
        var v = math.gcd(17, 5)
        check("math.gcd(17, 5) == 1  (coprime)", v == 1)
    catch:
        print("ERROR: math.gcd(17, 5) threw exception")
    fade

    try:
        var v = math.gcd(0, 7)
        check("math.gcd(0, 7) == 7", v == 7)
    catch:
        print("ERROR: math.gcd(0, 7) threw exception")
    fade

    try:
        var v = math.lcm(4, 6)
        check("math.lcm(4, 6) == 12", v == 12)
    catch:
        print("ERROR: math.lcm(4, 6) threw exception (Python 3.9+ only)")
    fade

    try:
        var v = math.lcm(3, 5)
        check("math.lcm(3, 5) == 15", v == 15)
    catch:
        print("ERROR: math.lcm(3, 5) threw exception")
    fade

    # ================================================================
    # Integer square root
    # ================================================================
    print("")
    print("--- Integer square root ---")

    try:
        var v = math.isqrt(0)
        check("math.isqrt(0) == 0", v == 0)
    catch:
        print("ERROR: math.isqrt(0) threw exception")
    fade

    try:
        var v = math.isqrt(1)
        check("math.isqrt(1) == 1", v == 1)
    catch:
        print("ERROR: math.isqrt(1) threw exception")
    fade

    try:
        var v = math.isqrt(16)
        check("math.isqrt(16) == 4", v == 4)
    catch:
        print("ERROR: math.isqrt(16) threw exception")
    fade

    try:
        var v = math.isqrt(17)
        check("math.isqrt(17) == 4  (floor)", v == 4)
    catch:
        print("ERROR: math.isqrt(17) threw exception")
    fade

    try:
        var v = math.isqrt(100)
        check("math.isqrt(100) == 10", v == 10)
    catch:
        print("ERROR: math.isqrt(100) threw exception")
    fade

    # ================================================================
    # Combinatorics
    # ================================================================
    print("")
    print("--- Combinatorics ---")

    try:
        var v = math.comb(5, 0)
        check("math.comb(5, 0) == 1", v == 1)
    catch:
        print("ERROR: math.comb(5, 0) threw exception (Python 3.8+)")
    fade

    try:
        var v = math.comb(5, 1)
        check("math.comb(5, 1) == 5", v == 5)
    catch:
        print("ERROR: math.comb(5, 1) threw exception")
    fade

    try:
        var v = math.comb(5, 2)
        check("math.comb(5, 2) == 10", v == 10)
    catch:
        print("ERROR: math.comb(5, 2) threw exception")
    fade

    try:
        var v = math.comb(10, 3)
        check("math.comb(10, 3) == 120", v == 120)
    catch:
        print("ERROR: math.comb(10, 3) threw exception")
    fade

    try:
        var v = math.perm(5, 0)
        check("math.perm(5, 0) == 1", v == 1)
    catch:
        print("ERROR: math.perm(5, 0) threw exception (Python 3.8+)")
    fade

    try:
        var v = math.perm(5, 1)
        check("math.perm(5, 1) == 5", v == 5)
    catch:
        print("ERROR: math.perm(5, 1) threw exception")
    fade

    try:
        var v = math.perm(5, 2)
        check("math.perm(5, 2) == 20", v == 20)
    catch:
        print("ERROR: math.perm(5, 2) threw exception")
    fade

    try:
        var v = math.perm(5, 5)
        check("math.perm(5, 5) == 120", v == 120)
    catch:
        print("ERROR: math.perm(5, 5) threw exception")
    fade

    # ================================================================
    # Finite / infinite / NaN checks
    # ================================================================
    print("")
    print("--- Finite / infinite / NaN checks ---")

    try:
        var v = math.isfinite(42.0)
        check("math.isfinite(42.0) is true", v == true)
    catch:
        print("ERROR: math.isfinite(42.0) threw exception")
    fade

    try:
        var v = math.isfinite(0.0)
        check("math.isfinite(0.0) is true", v == true)
    catch:
        print("ERROR: math.isfinite(0.0) threw exception")
    fade

    try:
        var inf = math.inf
        var v = math.isfinite(inf)
        check("math.isfinite(inf) is false", v == false)
    catch:
        print("ERROR: math.isfinite(inf) threw exception")
    fade

    try:
        var nan = math.nan
        var v = math.isfinite(nan)
        check("math.isfinite(nan) is false", v == false)
    catch:
        print("ERROR: math.isfinite(nan) threw exception")
    fade

    try:
        var v = math.isinf(0.0)
        check("math.isinf(0.0) is false", v == false)
    catch:
        print("ERROR: math.isinf(0.0) threw exception")
    fade

    try:
        var inf = math.inf
        var v = math.isinf(inf)
        check("math.isinf(inf) is true", v == true)
    catch:
        print("ERROR: math.isinf(inf) threw exception")
    fade

    try:
        var v = math.isnan(0.0)
        check("math.isnan(0.0) is false", v == false)
    catch:
        print("ERROR: math.isnan(0.0) threw exception")
    fade

    try:
        var nan = math.nan
        var v = math.isnan(nan)
        check("math.isnan(nan) is true", v == true)
    catch:
        print("ERROR: math.isnan(nan) threw exception")
    fade

    # ================================================================
    # Square root
    # ================================================================
    print("")
    print("--- Square root ---")

    try:
        var v = math.sqrt(0.0)
        check("math.sqrt(0.0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.sqrt(0.0) threw exception")
    fade

    try:
        var v = math.sqrt(1.0)
        check("math.sqrt(1.0) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.sqrt(1.0) threw exception")
    fade

    try:
        var v = math.sqrt(4.0)
        check("math.sqrt(4.0) == 2.0", v == 2.0)
    catch:
        print("ERROR: math.sqrt(4.0) threw exception")
    fade

    try:
        var v = math.sqrt(9.0)
        check("math.sqrt(9.0) == 3.0", v == 3.0)
    catch:
        print("ERROR: math.sqrt(9.0) threw exception")
    fade

    try:
        var v = math.sqrt(25.0)
        check("math.sqrt(25.0) == 5.0", v == 5.0)
    catch:
        print("ERROR: math.sqrt(25.0) threw exception")
    fade

    try:
        var v = math.sqrt(2.0)
        check("math.sqrt(2.0) > 1.4142 and < 1.4143", v > 1.4142 and v < 1.4143)
        print("  sqrt(2):", v)
    catch:
        print("ERROR: math.sqrt(2.0) threw exception")
    fade

    # ================================================================
    # Power
    # ================================================================
    print("")
    print("--- Power ---")

    try:
        var v = math.pow(2.0, 0.0)
        check("math.pow(2, 0) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.pow(2, 0) threw exception")
    fade

    try:
        var v = math.pow(2.0, 1.0)
        check("math.pow(2, 1) == 2.0", v == 2.0)
    catch:
        print("ERROR: math.pow(2, 1) threw exception")
    fade

    try:
        var v = math.pow(2.0, 10.0)
        check("math.pow(2, 10) == 1024.0", v == 1024.0)
    catch:
        print("ERROR: math.pow(2, 10) threw exception")
    fade

    try:
        var v = math.pow(3.0, 3.0)
        check("math.pow(3, 3) == 27.0", v == 27.0)
    catch:
        print("ERROR: math.pow(3, 3) threw exception")
    fade

    try:
        var v = math.pow(9.0, 0.5)
        check("math.pow(9, 0.5) == 3.0", v == 3.0)
    catch:
        print("ERROR: math.pow(9, 0.5) threw exception")
    fade

    # ================================================================
    # Exponential
    # ================================================================
    print("")
    print("--- Exponential ---")

    try:
        var v = math.exp(0.0)
        check("math.exp(0) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.exp(0) threw exception")
    fade

    try:
        var v = math.exp(1.0)
        check("math.exp(1) > 2.718 and < 2.719", v > 2.718 and v < 2.719)
        print("  exp(1):", v)
    catch:
        print("ERROR: math.exp(1) threw exception")
    fade

    try:
        var v = math.expm1(0.0)
        check("math.expm1(0) == 0.0  (e^0 - 1)", v == 0.0)
    catch:
        print("ERROR: math.expm1(0) threw exception")
    fade

    try:
        var v = math.expm1(1.0)
        check("math.expm1(1) > 1.718 and < 1.719", v > 1.718 and v < 1.719)
        print("  expm1(1):", v)
    catch:
        print("ERROR: math.expm1(1) threw exception")
    fade

    # ================================================================
    # Logarithm
    # ================================================================
    print("")
    print("--- Logarithm ---")

    try:
        var v = math.log(1.0)
        check("math.log(1) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.log(1) threw exception")
    fade

    try:
        var e = math.e
        var v = math.log(e)
        check("math.log(e) ~= 1.0", v > 0.9999 and v < 1.0001)
    catch:
        print("ERROR: math.log(e) threw exception")
    fade

    try:
        var v = math.log(100.0, 10.0)
        check("math.log(100, 10) ~= 2.0", v > 1.9999 and v < 2.0001)
    catch:
        print("ERROR: math.log(100, 10) threw exception")
    fade

    try:
        var v = math.log(8.0, 2.0)
        check("math.log(8, 2) ~= 3.0", v > 2.9999 and v < 3.0001)
    catch:
        print("ERROR: math.log(8, 2) threw exception")
    fade

    try:
        var v = math.log2(1.0)
        check("math.log2(1) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.log2(1) threw exception")
    fade

    try:
        var v = math.log2(2.0)
        check("math.log2(2) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.log2(2) threw exception")
    fade

    try:
        var v = math.log2(8.0)
        check("math.log2(8) == 3.0", v == 3.0)
    catch:
        print("ERROR: math.log2(8) threw exception")
    fade

    try:
        var v = math.log2(1024.0)
        check("math.log2(1024) == 10.0", v == 10.0)
    catch:
        print("ERROR: math.log2(1024) threw exception")
    fade

    try:
        var v = math.log10(1.0)
        check("math.log10(1) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.log10(1) threw exception")
    fade

    try:
        var v = math.log10(10.0)
        check("math.log10(10) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.log10(10) threw exception")
    fade

    try:
        var v = math.log10(1000.0)
        check("math.log10(1000) == 3.0", v == 3.0)
    catch:
        print("ERROR: math.log10(1000) threw exception")
    fade

    try:
        var v = math.log1p(0.0)
        check("math.log1p(0) == 0.0  (log(1+0))", v == 0.0)
    catch:
        print("ERROR: math.log1p(0) threw exception")
    fade

    # ================================================================
    # Angle conversion
    # ================================================================
    print("")
    print("--- Angle conversion ---")

    try:
        var v = math.degrees(0.0)
        check("math.degrees(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.degrees(0) threw exception")
    fade

    try:
        var pi = math.pi
        var v = math.degrees(pi)
        check("math.degrees(pi) ~= 180.0", v > 179.9999 and v < 180.0001)
        print("  degrees(pi):", v)
    catch:
        print("ERROR: math.degrees(pi) threw exception")
    fade

    try:
        var pi = math.pi
        var half_pi = pi / 2
        var v = math.degrees(half_pi)
        check("math.degrees(pi/2) ~= 90.0", v > 89.9999 and v < 90.0001)
    catch:
        print("ERROR: math.degrees(pi/2) threw exception")
    fade

    try:
        var v = math.radians(0.0)
        check("math.radians(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.radians(0) threw exception")
    fade

    try:
        var pi = math.pi
        var v = math.radians(180.0)
        check("math.radians(180) ~= pi", v > 3.14159 and v < 3.14160)
        print("  radians(180):", v)
    catch:
        print("ERROR: math.radians(180) threw exception")
    fade

    try:
        var v = math.radians(90.0)
        check("math.radians(90) ~= pi/2", v > 1.5707 and v < 1.5708)
    catch:
        print("ERROR: math.radians(90) threw exception")
    fade

    try:
        var tau = math.tau
        var v = math.radians(360.0)
        check("math.radians(360) ~= tau", v > 6.283 and v < 6.284)
    catch:
        print("ERROR: math.radians(360) threw exception")
    fade

    # ================================================================
    # Trigonometry -- sin
    # ================================================================
    print("")
    print("--- Trigonometry: sin ---")

    try:
        var v = math.sin(0.0)
        check("math.sin(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.sin(0) threw exception")
    fade

    try:
        var pi = math.pi
        var half_pi = pi / 2
        var v = math.sin(half_pi)
        check("math.sin(pi/2) ~= 1.0", v > 0.9999 and v < 1.0001)
    catch:
        print("ERROR: math.sin(pi/2) threw exception")
    fade

    try:
        var pi = math.pi
        var v = math.sin(pi)
        check("math.sin(pi) ~= 0.0", v > -0.00001 and v < 0.00001)
    catch:
        print("ERROR: math.sin(pi) threw exception")
    fade

    try:
        var pi = math.pi
        var three_half_pi = pi * 1.5
        var v = math.sin(three_half_pi)
        check("math.sin(3*pi/2) ~= -1.0", v > -1.0001 and v < -0.9999)
    catch:
        print("ERROR: math.sin(3*pi/2) threw exception")
    fade

    # ================================================================
    # Trigonometry -- cos
    # ================================================================
    print("")
    print("--- Trigonometry: cos ---")

    try:
        var v = math.cos(0.0)
        check("math.cos(0) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.cos(0) threw exception")
    fade

    try:
        var pi = math.pi
        var half_pi = pi / 2
        var v = math.cos(half_pi)
        check("math.cos(pi/2) ~= 0.0", v > -0.00001 and v < 0.00001)
    catch:
        print("ERROR: math.cos(pi/2) threw exception")
    fade

    try:
        var pi = math.pi
        var v = math.cos(pi)
        check("math.cos(pi) ~= -1.0", v > -1.0001 and v < -0.9999)
    catch:
        print("ERROR: math.cos(pi) threw exception")
    fade

    try:
        var tau = math.tau
        var v = math.cos(tau)
        check("math.cos(tau) ~= 1.0  (full circle)", v > 0.9999 and v < 1.0001)
    catch:
        print("ERROR: math.cos(tau) threw exception")
    fade

    # ================================================================
    # Trigonometry -- tan
    # ================================================================
    print("")
    print("--- Trigonometry: tan ---")

    try:
        var v = math.tan(0.0)
        check("math.tan(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.tan(0) threw exception")
    fade

    try:
        var pi = math.pi
        var quarter_pi = pi / 4
        var v = math.tan(quarter_pi)
        check("math.tan(pi/4) ~= 1.0", v > 0.9999 and v < 1.0001)
    catch:
        print("ERROR: math.tan(pi/4) threw exception")
    fade

    try:
        var pi = math.pi
        var v = math.tan(pi)
        check("math.tan(pi) ~= 0.0", v > -0.0001 and v < 0.0001)
    catch:
        print("ERROR: math.tan(pi) threw exception")
    fade

    # ================================================================
    # Inverse trig -- asin / acos / atan / atan2
    # ================================================================
    print("")
    print("--- Inverse trig: asin / acos / atan / atan2 ---")

    try:
        var v = math.asin(0.0)
        check("math.asin(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.asin(0) threw exception")
    fade

    try:
        var v = math.asin(1.0)
        check("math.asin(1) ~= pi/2", v > 1.5707 and v < 1.5708)
    catch:
        print("ERROR: math.asin(1) threw exception")
    fade

    try:
        var v = math.asin(-1.0)
        check("math.asin(-1) ~= -pi/2", v > -1.5708 and v < -1.5707)
    catch:
        print("ERROR: math.asin(-1) threw exception")
    fade

    try:
        var v = math.acos(1.0)
        check("math.acos(1) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.acos(1) threw exception")
    fade

    try:
        var v = math.acos(0.0)
        check("math.acos(0) ~= pi/2", v > 1.5707 and v < 1.5708)
    catch:
        print("ERROR: math.acos(0) threw exception")
    fade

    try:
        var v = math.acos(-1.0)
        check("math.acos(-1) ~= pi", v > 3.14159 and v < 3.14160)
    catch:
        print("ERROR: math.acos(-1) threw exception")
    fade

    try:
        var v = math.atan(0.0)
        check("math.atan(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.atan(0) threw exception")
    fade

    try:
        var v = math.atan(1.0)
        check("math.atan(1) ~= pi/4", v > 0.7853 and v < 0.7854)
    catch:
        print("ERROR: math.atan(1) threw exception")
    fade

    try:
        var v = math.atan(-1.0)
        check("math.atan(-1) ~= -pi/4", v > -0.7854 and v < -0.7853)
    catch:
        print("ERROR: math.atan(-1) threw exception")
    fade

    try:
        var v = math.atan2(0.0, 1.0)
        check("math.atan2(0, 1) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.atan2(0, 1) threw exception")
    fade

    try:
        var v = math.atan2(1.0, 0.0)
        check("math.atan2(1, 0) ~= pi/2", v > 1.5707 and v < 1.5708)
    catch:
        print("ERROR: math.atan2(1, 0) threw exception")
    fade

    try:
        var v = math.atan2(1.0, 1.0)
        check("math.atan2(1, 1) ~= pi/4", v > 0.7853 and v < 0.7854)
    catch:
        print("ERROR: math.atan2(1, 1) threw exception")
    fade

    try:
        var v = math.atan2(0.0, -1.0)
        check("math.atan2(0, -1) ~= pi", v > 3.14159 and v < 3.14160)
    catch:
        print("ERROR: math.atan2(0, -1) threw exception")
    fade

    # ================================================================
    # Hypot
    # ================================================================
    print("")
    print("--- Hypot ---")

    try:
        var v = math.hypot(0.0, 0.0)
        check("math.hypot(0, 0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.hypot(0, 0) threw exception")
    fade

    try:
        var v = math.hypot(3.0, 4.0)
        check("math.hypot(3, 4) == 5.0  (3-4-5 triangle)", v == 5.0)
    catch:
        print("ERROR: math.hypot(3, 4) threw exception")
    fade

    try:
        var v = math.hypot(5.0, 12.0)
        check("math.hypot(5, 12) == 13.0  (5-12-13 triangle)", v == 13.0)
    catch:
        print("ERROR: math.hypot(5, 12) threw exception")
    fade

    try:
        var v = math.hypot(1.0, 0.0)
        check("math.hypot(1, 0) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.hypot(1, 0) threw exception")
    fade

    # ================================================================
    # Hyperbolic functions
    # ================================================================
    print("")
    print("--- Hyperbolic functions ---")

    try:
        var v = math.sinh(0.0)
        check("math.sinh(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.sinh(0) threw exception")
    fade

    try:
        var v = math.sinh(1.0)
        check("math.sinh(1) > 1.17 and < 1.18", v > 1.17 and v < 1.18)
        print("  sinh(1):", v)
    catch:
        print("ERROR: math.sinh(1) threw exception")
    fade

    try:
        var v = math.cosh(0.0)
        check("math.cosh(0) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.cosh(0) threw exception")
    fade

    try:
        var v = math.cosh(1.0)
        check("math.cosh(1) > 1.54 and < 1.55", v > 1.54 and v < 1.55)
        print("  cosh(1):", v)
    catch:
        print("ERROR: math.cosh(1) threw exception")
    fade

    try:
        var v = math.tanh(0.0)
        check("math.tanh(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.tanh(0) threw exception")
    fade

    try:
        var v = math.tanh(1.0)
        check("math.tanh(1) > 0.761 and < 0.762", v > 0.761 and v < 0.762)
        print("  tanh(1):", v)
    catch:
        print("ERROR: math.tanh(1) threw exception")
    fade

    try:
        var v = math.asinh(0.0)
        check("math.asinh(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.asinh(0) threw exception")
    fade

    try:
        var v = math.asinh(1.0)
        check("math.asinh(1) > 0.881 and < 0.882", v > 0.881 and v < 0.882)
        print("  asinh(1):", v)
    catch:
        print("ERROR: math.asinh(1) threw exception")
    fade

    try:
        var v = math.acosh(1.0)
        check("math.acosh(1) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.acosh(1) threw exception")
    fade

    try:
        var v = math.acosh(2.0)
        check("math.acosh(2) > 1.316 and < 1.317", v > 1.316 and v < 1.317)
        print("  acosh(2):", v)
    catch:
        print("ERROR: math.acosh(2) threw exception")
    fade

    try:
        var v = math.atanh(0.0)
        check("math.atanh(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.atanh(0) threw exception")
    fade

    try:
        var v = math.atanh(0.5)
        check("math.atanh(0.5) > 0.549 and < 0.550", v > 0.549 and v < 0.550)
        print("  atanh(0.5):", v)
    catch:
        print("ERROR: math.atanh(0.5) threw exception")
    fade

    # ================================================================
    # Special float operations
    # ================================================================
    print("")
    print("--- Special float operations ---")

    try:
        var v = math.copysign(3.0, -1.0)
        check("math.copysign(3, -1) == -3.0", v == -3.0)
    catch:
        print("ERROR: math.copysign(3, -1) threw exception")
    fade

    try:
        var v = math.copysign(-3.0, 1.0)
        check("math.copysign(-3, 1) == 3.0", v == 3.0)
    catch:
        print("ERROR: math.copysign(-3, 1) threw exception")
    fade

    try:
        var v = math.copysign(0.0, -1.0)
        check("math.copysign(0, -1) == 0.0 (negative zero)", v == 0.0)
    catch:
        print("ERROR: math.copysign(0, -1) threw exception")
    fade

    try:
        var v = math.fmod(10.0, 3.0)
        check("math.fmod(10, 3) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.fmod(10, 3) threw exception")
    fade

    try:
        var v = math.fmod(7.5, 2.5)
        check("math.fmod(7.5, 2.5) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.fmod(7.5, 2.5) threw exception")
    fade

    try:
        var v = math.fmod(-10.0, 3.0)
        check("math.fmod(-10, 3) == -1.0", v == -1.0)
    catch:
        print("ERROR: math.fmod(-10, 3) threw exception")
    fade

    try:
        var v = math.remainder(10.0, 3.0)
        check("math.remainder(10, 3) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.remainder(10, 3) threw exception")
    fade

    try:
        var v = math.remainder(11.0, 3.0)
        check("math.remainder(11, 3) == -1.0  (IEEE nearest)", v == -1.0)
    catch:
        print("ERROR: math.remainder(11, 3) threw exception")
    fade

    try:
        var v = math.ldexp(1.0, 0)
        check("math.ldexp(1.0, 0) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.ldexp(1.0, 0) threw exception")
    fade

    try:
        var v = math.ldexp(1.0, 10)
        check("math.ldexp(1.0, 10) == 1024.0", v == 1024.0)
    catch:
        print("ERROR: math.ldexp(1.0, 10) threw exception")
    fade

    try:
        var v = math.ldexp(0.5, 4)
        check("math.ldexp(0.5, 4) == 8.0", v == 8.0)
    catch:
        print("ERROR: math.ldexp(0.5, 4) threw exception")
    fade

    try:
        var result = math.modf(3.75)
        check("math.modf(3.75) works", true)
        print("  modf(3.75):", result)
    catch:
        print("ERROR: math.modf(3.75) threw exception")
    fade

    try:
        var result = math.modf(-2.5)
        check("math.modf(-2.5) works", true)
        print("  modf(-2.5):", result)
    catch:
        print("ERROR: math.modf(-2.5) threw exception")
    fade

    try:
        var result = math.frexp(8.0)
        check("math.frexp(8.0) works  (mantissa * 2^exp)", true)
        print("  frexp(8.0):", result)
    catch:
        print("ERROR: math.frexp(8.0) threw exception")
    fade

    try:
        var result = math.frexp(0.0)
        check("math.frexp(0.0) works", true)
        print("  frexp(0.0):", result)
    catch:
        print("ERROR: math.frexp(0.0) threw exception")
    fade

    try:
        var v = math.fsum([1.0, 2.0, 3.0])
        check("math.fsum([1,2,3]) == 6.0", v == 6.0)
    catch:
        print("ERROR: math.fsum([1,2,3]) threw exception  (list arg may not be supported yet)")
    fade

    try:
        var v = math.prod([1, 2, 3, 4, 5])
        check("math.prod([1..5]) == 120", v == 120)
    catch:
        print("ERROR: math.prod([1..5]) threw exception  (list arg / Python 3.8+ only)")
    fade

    # ================================================================
    # Special functions (erf, gamma)
    # ================================================================
    print("")
    print("--- Special functions: erf, gamma ---")

    try:
        var v = math.erf(0.0)
        check("math.erf(0) == 0.0", v == 0.0)
    catch:
        print("ERROR: math.erf(0) threw exception")
    fade

    try:
        var v = math.erf(1.0)
        check("math.erf(1) > 0.842 and < 0.843", v > 0.842 and v < 0.843)
        print("  erf(1):", v)
    catch:
        print("ERROR: math.erf(1) threw exception")
    fade

    try:
        var v = math.erfc(0.0)
        check("math.erfc(0) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.erfc(0) threw exception")
    fade

    try:
        var ve = math.erf(1.0)
        var vc = math.erfc(1.0)
        var sum = ve + vc
        check("erf(x) + erfc(x) == 1.0", sum > 0.9999 and sum < 1.0001)
    catch:
        print("ERROR: erf + erfc identity threw exception")
    fade

    try:
        var v = math.gamma(1.0)
        check("math.gamma(1) == 1.0", v == 1.0)
    catch:
        print("ERROR: math.gamma(1) threw exception")
    fade

    try:
        var v = math.gamma(2.0)
        check("math.gamma(2) == 1.0  (1!)", v == 1.0)
    catch:
        print("ERROR: math.gamma(2) threw exception")
    fade

    try:
        var v = math.gamma(3.0)
        check("math.gamma(3) == 2.0  (2!)", v == 2.0)
    catch:
        print("ERROR: math.gamma(3) threw exception")
    fade

    try:
        var v = math.gamma(5.0)
        check("math.gamma(5) == 24.0  (4!)", v == 24.0)
    catch:
        print("ERROR: math.gamma(5) threw exception")
    fade

    try:
        var v = math.lgamma(1.0)
        check("math.lgamma(1) == 0.0  (log(1!))", v == 0.0)
    catch:
        print("ERROR: math.lgamma(1) threw exception")
    fade

    try:
        var v = math.lgamma(2.0)
        check("math.lgamma(2) == 0.0  (log(1!))", v == 0.0)
    catch:
        print("ERROR: math.lgamma(2) threw exception")
    fade

    try:
        var v = math.lgamma(5.0)
        check("math.lgamma(5) ~= 3.178  (log(24))", v > 3.17 and v < 3.19)
        print("  lgamma(5):", v)
    catch:
        print("ERROR: math.lgamma(5) threw exception")
    fade

    print("")
    print("=== math test complete ===")
}
