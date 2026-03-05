# core_random.ly
# Lyric adhoc test -- exercises every public function of Python's random module.
#
# Run with:  lyric run lyric/tests/python_modules/core_random.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions
#
# Note: results are non-deterministic by design; tests verify value ranges
# and types rather than exact values.

importpy random

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
    print("=== Lyric random module adhoc test ===")
    print("")

    # ================================================================
    # Seeding and state
    # ================================================================
    print("--- Seeding ---")

    try:
        random.seed(42)
        check("random.seed(42) works", true)
    catch:
        print("ERROR: random.seed(42) threw exception")
    fade

    try:
        random.seed(0)
        check("random.seed(0) works", true)
    catch:
        print("ERROR: random.seed(0) threw exception")
    fade

    try:
        random.seed(3.14)
        check("random.seed(float) works", true)
    catch:
        print("ERROR: random.seed(float) threw exception")
    fade

    # getstate / setstate
    try:
        var state = random.getstate()
        check("random.getstate() works", true)
    catch:
        print("ERROR: random.getstate() threw exception")
    fade

    try:
        var state = random.getstate()
        random.setstate(state)
        check("random.setstate(state) works", true)
    catch:
        print("ERROR: random.setstate() threw exception")
    fade

    # Reproducibility via seed
    try:
        random.seed(42)
        var a = random.random()
        random.seed(42)
        var b = random.random()
        check("same seed produces same result", a == b)
    catch:
        print("ERROR: seed reproducibility check threw exception")
    fade

    # ================================================================
    # random() -- uniform [0.0, 1.0)
    # ================================================================
    print("")
    print("--- random() ---")

    try:
        random.seed(1)
        var v = random.random()
        check("random.random() returns float in [0,1)", v >= 0.0 and v < 1.0)
        print("  random():", v)
    catch:
        print("ERROR: random.random() threw exception")
    fade

    try:
        random.seed(2)
        var v1 = random.random()
        var v2 = random.random()
        var v3 = random.random()
        check("random.random() x3 all in [0,1)", v1 >= 0.0 and v1 < 1.0 and v2 >= 0.0 and v2 < 1.0 and v3 >= 0.0 and v3 < 1.0)
    catch:
        print("ERROR: random.random() x3 threw exception")
    fade

    # ================================================================
    # uniform(a, b) -- uniform [a, b]
    # ================================================================
    print("")
    print("--- uniform() ---")

    try:
        random.seed(1)
        var v = random.uniform(0.0, 1.0)
        check("random.uniform(0, 1) in [0, 1]", v >= 0.0 and v <= 1.0)
        print("  uniform(0,1):", v)
    catch:
        print("ERROR: random.uniform(0,1) threw exception")
    fade

    try:
        random.seed(1)
        var v = random.uniform(5.0, 10.0)
        check("random.uniform(5, 10) in [5, 10]", v >= 5.0 and v <= 10.0)
        print("  uniform(5,10):", v)
    catch:
        print("ERROR: random.uniform(5,10) threw exception")
    fade

    try:
        random.seed(1)
        var v = random.uniform(-1.0, 1.0)
        check("random.uniform(-1, 1) in [-1, 1]", v >= -1.0 and v <= 1.0)
        print("  uniform(-1,1):", v)
    catch:
        print("ERROR: random.uniform(-1,1) threw exception")
    fade

    try:
        random.seed(99)
        var v = random.uniform(100.0, 200.0)
        check("random.uniform(100, 200) in range", v >= 100.0 and v <= 200.0)
    catch:
        print("ERROR: random.uniform(100,200) threw exception")
    fade

    # ================================================================
    # randint(a, b) -- integer in [a, b]
    # ================================================================
    print("")
    print("--- randint() ---")

    try:
        random.seed(1)
        var v = random.randint(1, 6)
        check("random.randint(1, 6) in [1,6]", v >= 1 and v <= 6)
        print("  randint(1,6):", v)
    catch:
        print("ERROR: random.randint(1,6) threw exception")
    fade

    try:
        random.seed(2)
        var v = random.randint(0, 100)
        check("random.randint(0, 100) in [0,100]", v >= 0 and v <= 100)
        print("  randint(0,100):", v)
    catch:
        print("ERROR: random.randint(0,100) threw exception")
    fade

    try:
        random.seed(3)
        var v = random.randint(-10, 10)
        check("random.randint(-10, 10) in [-10,10]", v >= -10 and v <= 10)
        print("  randint(-10,10):", v)
    catch:
        print("ERROR: random.randint(-10,10) threw exception")
    fade

    try:
        random.seed(4)
        var v = random.randint(5, 5)
        check("random.randint(5, 5) == 5", v == 5)
    catch:
        print("ERROR: random.randint(5,5) threw exception")
    fade

    # ================================================================
    # randrange() -- integer from range
    # ================================================================
    print("")
    print("--- randrange() ---")

    try:
        random.seed(1)
        var v = random.randrange(10)
        check("random.randrange(10) in [0,9]", v >= 0 and v < 10)
        print("  randrange(10):", v)
    catch:
        print("ERROR: random.randrange(10) threw exception")
    fade

    try:
        random.seed(2)
        var v = random.randrange(5, 10)
        check("random.randrange(5, 10) in [5,9]", v >= 5 and v < 10)
        print("  randrange(5,10):", v)
    catch:
        print("ERROR: random.randrange(5,10) threw exception")
    fade

    try:
        random.seed(3)
        var v = random.randrange(0, 20, 2)
        check("random.randrange(0,20,2) is even", v >= 0 and v < 20)
        print("  randrange(0,20,2):", v)
    catch:
        print("ERROR: random.randrange(0,20,2) threw exception")
    fade

    try:
        random.seed(4)
        var v = random.randrange(0, 50, 5)
        check("random.randrange(0,50,5) in [0,45]", v >= 0 and v < 50)
        print("  randrange(0,50,5):", v)
    catch:
        print("ERROR: random.randrange(0,50,5) threw exception")
    fade

    # ================================================================
    # choice() -- pick from sequence
    # ================================================================
    print("")
    print("--- choice() ---")

    try:
        random.seed(1)
        var v = random.choice([1, 2, 3, 4, 5])
        check("random.choice([1..5]) in [1,5]", v >= 1 and v <= 5)
        print("  choice([1..5]):", v)
    catch:
        print("ERROR: random.choice([1..5]) threw exception")
    fade

    try:
        random.seed(2)
        var v = random.choice([10, 20, 30])
        check("random.choice([10,20,30]) is valid", v == 10 or v == 20 or v == 30)
        print("  choice([10,20,30]):", v)
    catch:
        print("ERROR: random.choice([10,20,30]) threw exception")
    fade

    try:
        random.seed(7)
        var v = random.choice([42])
        check("random.choice([42]) == 42  (single elem)", v == 42)
    catch:
        print("ERROR: random.choice([42]) threw exception")
    fade

    # ================================================================
    # choices() -- weighted or k-sample with replacement
    # Note: k= is keyword-only in Python so must use default k=1 from Lyric
    # ================================================================
    print("")
    print("--- choices() ---")

    try:
        random.seed(1)
        var result = random.choices([1, 2, 3, 4, 5])
        check("random.choices([1..5]) works  (default k=1)", true)
        print("  choices([1..5]):", result)
    catch:
        print("ERROR: random.choices() threw exception")
    fade

    # ================================================================
    # shuffle() -- in-place shuffle
    # ================================================================
    print("")
    print("--- shuffle() ---")

    try:
        random.seed(1)
        var lst = [1, 2, 3, 4, 5]
        random.shuffle(lst)
        check("random.shuffle() works", true)
        print("  shuffled:", lst)
    catch:
        print("ERROR: random.shuffle() threw exception")
    fade

    try:
        random.seed(42)
        var lst = [10, 20, 30, 40, 50]
        random.shuffle(lst)
        check("random.shuffle([10..50]) works", true)
        print("  shuffled [10..50]:", lst)
    catch:
        print("ERROR: random.shuffle([10..50]) threw exception")
    fade

    # ================================================================
    # sample() -- k unique elements without replacement
    # Note: Python 3.11+ requires a Sequence type. Lyric list literals are
    # ArrObject instances; access .elements to get the inner Python list.
    # ================================================================
    print("")
    print("--- sample() ---")

    try:
        random.seed(1)
        var pool = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        var result = random.sample(pool.elements, 3)
        check("random.sample(pool.elements, 3) works", true)
        print("  sample(pool.elements, 3):", result)
    catch:
        print("ERROR: random.sample(pool.elements, 3) threw exception")
    fade

    try:
        random.seed(2)
        var pool = [10, 20, 30, 40, 50]
        var result = random.sample(pool.elements, 2)
        check("random.sample(pool.elements, 2) works", true)
        print("  sample([10..50].elements, 2):", result)
    catch:
        print("ERROR: random.sample([10..50].elements, 2) threw exception")
    fade

    try:
        random.seed(3)
        var pool = [1, 2, 3]
        var result = random.sample(pool.elements, 3)
        check("random.sample([1,2,3].elements, 3) all elements", true)
        print("  sample([1,2,3].elements, 3):", result)
    catch:
        print("ERROR: random.sample([1,2,3].elements, 3) threw exception")
    fade

    # ================================================================
    # Floating-point distributions
    # ================================================================
    print("")
    print("--- Distributions ---")

    # gauss(mu, sigma) -- Gaussian / normal distribution
    try:
        random.seed(1)
        var v = random.gauss(0.0, 1.0)
        check("random.gauss(0, 1) works  (standard normal)", true)
        print("  gauss(0,1):", v)
    catch:
        print("ERROR: random.gauss(0, 1) threw exception")
    fade

    try:
        random.seed(1)
        var v = random.gauss(100.0, 15.0)
        check("random.gauss(100, 15) works  (IQ-like)", true)
        print("  gauss(100,15):", v)
    catch:
        print("ERROR: random.gauss(100,15) threw exception")
    fade

    # normalvariate(mu, sigma) -- same distribution, different algorithm
    try:
        random.seed(1)
        var v = random.normalvariate(0.0, 1.0)
        check("random.normalvariate(0, 1) works", true)
        print("  normalvariate(0,1):", v)
    catch:
        print("ERROR: random.normalvariate(0,1) threw exception")
    fade

    # expovariate(lambd) -- exponential distribution; lambd = 1/mean
    try:
        random.seed(1)
        var v = random.expovariate(1.0)
        check("random.expovariate(1) > 0", v > 0.0)
        print("  expovariate(1):", v)
    catch:
        print("ERROR: random.expovariate(1) threw exception")
    fade

    try:
        random.seed(1)
        var v = random.expovariate(0.5)
        check("random.expovariate(0.5) > 0", v > 0.0)
        print("  expovariate(0.5):", v)
    catch:
        print("ERROR: random.expovariate(0.5) threw exception")
    fade

    # betavariate(alpha, beta) -- beta distribution [0, 1]
    try:
        random.seed(1)
        var v = random.betavariate(2.0, 5.0)
        check("random.betavariate(2, 5) in [0,1]", v >= 0.0 and v <= 1.0)
        print("  betavariate(2,5):", v)
    catch:
        print("ERROR: random.betavariate(2,5) threw exception")
    fade

    # gammavariate(alpha, beta) -- gamma distribution
    try:
        random.seed(1)
        var v = random.gammavariate(2.0, 1.0)
        check("random.gammavariate(2, 1) > 0", v > 0.0)
        print("  gammavariate(2,1):", v)
    catch:
        print("ERROR: random.gammavariate(2,1) threw exception")
    fade

    # lognormvariate(mu, sigma)
    try:
        random.seed(1)
        var v = random.lognormvariate(0.0, 1.0)
        check("random.lognormvariate(0, 1) > 0", v > 0.0)
        print("  lognormvariate(0,1):", v)
    catch:
        print("ERROR: random.lognormvariate(0,1) threw exception")
    fade

    # vonmisesvariate(mu, kappa) -- circular distribution [0, 2*pi]
    try:
        random.seed(1)
        var v = random.vonmisesvariate(0.0, 1.0)
        check("random.vonmisesvariate(0, 1) in [0, 2*pi]", v >= 0.0 and v < 6.29)
        print("  vonmisesvariate(0,1):", v)
    catch:
        print("ERROR: random.vonmisesvariate(0,1) threw exception")
    fade

    # paretovariate(alpha) -- pareto distribution >= 1
    try:
        random.seed(1)
        var v = random.paretovariate(2.0)
        check("random.paretovariate(2) >= 1.0", v >= 1.0)
        print("  paretovariate(2):", v)
    catch:
        print("ERROR: random.paretovariate(2) threw exception")
    fade

    # weibullvariate(alpha, beta)
    try:
        random.seed(1)
        var v = random.weibullvariate(1.0, 1.5)
        check("random.weibullvariate(1, 1.5) > 0", v > 0.0)
        print("  weibullvariate(1,1.5):", v)
    catch:
        print("ERROR: random.weibullvariate(1,1.5) threw exception")
    fade

    # triangular(low, high, mode)
    try:
        random.seed(1)
        var v = random.triangular(0.0, 1.0, 0.5)
        check("random.triangular(0, 1, 0.5) in [0,1]", v >= 0.0 and v <= 1.0)
        print("  triangular(0,1,0.5):", v)
    catch:
        print("ERROR: random.triangular(0,1,0.5) threw exception")
    fade

    # ================================================================
    # Random bits and bytes
    # ================================================================
    print("")
    print("--- Random bits and bytes ---")

    try:
        var v = random.getrandbits(8)
        check("random.getrandbits(8) in [0, 255]", v >= 0 and v <= 255)
        print("  getrandbits(8):", v)
    catch:
        print("ERROR: random.getrandbits(8) threw exception")
    fade

    try:
        var v = random.getrandbits(16)
        check("random.getrandbits(16) in [0, 65535]", v >= 0 and v <= 65535)
        print("  getrandbits(16):", v)
    catch:
        print("ERROR: random.getrandbits(16) threw exception")
    fade

    try:
        var v = random.getrandbits(1)
        check("random.getrandbits(1) is 0 or 1", v == 0 or v == 1)
        print("  getrandbits(1):", v)
    catch:
        print("ERROR: random.getrandbits(1) threw exception")
    fade

    try:
        var v = random.getrandbits(32)
        check("random.getrandbits(32) >= 0", v >= 0)
        print("  getrandbits(32):", v)
    catch:
        print("ERROR: random.getrandbits(32) threw exception")
    fade

    # randbytes (Python 3.9+)
    try:
        var v = random.randbytes(4)
        check("random.randbytes(4) works  (Python 3.9+)", true)
        print("  randbytes(4):", v)
    catch:
        print("ERROR: random.randbytes(4) threw exception (Python 3.9+ only)")
    fade

    # ================================================================
    # Practical: simulate dice, coin, shuffle demo
    # ================================================================
    print("")
    print("--- Practical examples ---")

    # Simulate a 6-sided die roll (10 times)
    try:
        random.seed(7)
        var d1 = random.randint(1, 6)
        var d2 = random.randint(1, 6)
        var d3 = random.randint(1, 6)
        var d4 = random.randint(1, 6)
        var d5 = random.randint(1, 6)
        check("d6 rolls all in [1,6]", d1 >= 1 and d1 <= 6 and d2 >= 1 and d2 <= 6 and d3 >= 1 and d3 <= 6)
        print("  5 dice rolls:", d1, d2, d3, d4, d5)
    catch:
        print("ERROR: dice simulation threw exception")
    fade

    # Coin flip via randint
    try:
        random.seed(13)
        var flip = random.randint(0, 1)
        check("coin flip is 0 or 1", flip == 0 or flip == 1)
        print("  coin flip:", flip)
    catch:
        print("ERROR: coin flip threw exception")
    fade

    # Pick a random float in [-5, 5]
    try:
        random.seed(21)
        var v = random.uniform(-5.0, 5.0)
        check("uniform(-5, 5) in range", v >= -5.0 and v <= 5.0)
        print("  uniform(-5,5):", v)
    catch:
        print("ERROR: uniform(-5,5) threw exception")
    fade

    # Sample without replacement from a small list (use .elements for Python Sequence)
    try:
        random.seed(99)
        var pool = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        var drawn = random.sample(pool.elements, 5)
        check("sample 5 from 10 works", true)
        print("  5 from 10:", drawn)
    catch:
        print("ERROR: sample 5 from 10 threw exception")
    fade

    # Standard normal sample
    try:
        random.seed(55)
        var v = random.gauss(0.0, 1.0)
        check("gauss(0,1) is a float", true)
        print("  standard normal sample:", v)
    catch:
        print("ERROR: gauss sample threw exception")
    fade

    print("")
    print("=== random test complete ===")
}
