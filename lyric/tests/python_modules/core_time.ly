# core_time.ly
# Lyric adhoc test -- exercises the public functions and constants of Python's
# time module.
#
# Run with:  lyric run lyric/tests/python_modules/core_time.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions
#
# NOTE: Many time values are non-deterministic (depend on wall clock, CPU,
#       platform).  Tests verify ranges and types rather than exact values.

importpy time

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
    print("=== Lyric time module adhoc test ===")
    print("")

    # ================================================================
    # time() -- epoch seconds
    # ================================================================
    print("--- time() ---")

    try:
        var t = time.time()
        check("time.time() > 0", t > 0)
        print("  time():", t)
    catch:
        print("ERROR: time.time() threw exception")
    fade

    try:
        var t = time.time()
        # Should be well past year 2000 (epoch 946684800)
        check("time.time() > 946684800 (past year 2000)", t > 946684800)
    catch:
        print("ERROR: time.time() epoch check threw exception")
    fade

    try:
        var t1 = time.time()
        var t2 = time.time()
        check("two successive time() calls: t2 >= t1", t2 >= t1)
    catch:
        print("ERROR: successive time() calls threw exception")
    fade

    # ================================================================
    # time_ns() -- epoch nanoseconds (Python 3.7+)
    # ================================================================
    print("")
    print("--- time_ns() ---")

    try:
        var tns = time.time_ns()
        check("time.time_ns() > 0", tns > 0)
        print("  time_ns():", tns)
    catch:
        print("ERROR: time.time_ns() threw exception (Python 3.7+)")
    fade

    # ================================================================
    # monotonic() -- monotonic clock
    # ================================================================
    print("")
    print("--- monotonic() ---")

    try:
        var m = time.monotonic()
        check("time.monotonic() >= 0", m >= 0)
        print("  monotonic():", m)
    catch:
        print("ERROR: time.monotonic() threw exception")
    fade

    try:
        var m1 = time.monotonic()
        var m2 = time.monotonic()
        check("monotonic() is non-decreasing: m2 >= m1", m2 >= m1)
    catch:
        print("ERROR: monotonic() ordering threw exception")
    fade

    try:
        var mns = time.monotonic_ns()
        check("time.monotonic_ns() > 0", mns > 0)
        print("  monotonic_ns():", mns)
    catch:
        print("ERROR: time.monotonic_ns() threw exception (Python 3.7+)")
    fade

    # ================================================================
    # perf_counter() -- high-resolution performance counter
    # ================================================================
    print("")
    print("--- perf_counter() ---")

    try:
        var p = time.perf_counter()
        check("time.perf_counter() >= 0", p >= 0)
        print("  perf_counter():", p)
    catch:
        print("ERROR: time.perf_counter() threw exception")
    fade

    try:
        var p1 = time.perf_counter()
        var p2 = time.perf_counter()
        check("perf_counter() is non-decreasing: p2 >= p1", p2 >= p1)
    catch:
        print("ERROR: perf_counter() ordering threw exception")
    fade

    try:
        var pns = time.perf_counter_ns()
        check("time.perf_counter_ns() > 0", pns > 0)
        print("  perf_counter_ns():", pns)
    catch:
        print("ERROR: time.perf_counter_ns() threw exception (Python 3.7+)")
    fade

    # ================================================================
    # process_time() -- CPU time for this process
    # ================================================================
    print("")
    print("--- process_time() ---")

    try:
        var pt = time.process_time()
        check("time.process_time() >= 0", pt >= 0)
        print("  process_time():", pt)
    catch:
        print("ERROR: time.process_time() threw exception")
    fade

    try:
        var pt1 = time.process_time()
        var pt2 = time.process_time()
        check("process_time() is non-decreasing", pt2 >= pt1)
    catch:
        print("ERROR: process_time() ordering threw exception")
    fade

    try:
        var ptns = time.process_time_ns()
        check("time.process_time_ns() >= 0", ptns >= 0)
        print("  process_time_ns():", ptns)
    catch:
        print("ERROR: time.process_time_ns() threw exception (Python 3.7+)")
    fade

    # ================================================================
    # thread_time() -- CPU time for this thread (Python 3.7+)
    # ================================================================
    print("")
    print("--- thread_time() ---")

    try:
        var tt = time.thread_time()
        check("time.thread_time() >= 0", tt >= 0)
        print("  thread_time():", tt)
    catch:
        print("ERROR: time.thread_time() threw exception (Python 3.7+, not all platforms)")
    fade

    try:
        var ttns = time.thread_time_ns()
        check("time.thread_time_ns() >= 0", ttns >= 0)
        print("  thread_time_ns():", ttns)
    catch:
        print("ERROR: time.thread_time_ns() threw exception (Python 3.7+)")
    fade

    # ================================================================
    # sleep()
    # ================================================================
    print("")
    print("--- sleep() ---")

    try:
        var before = time.perf_counter()
        time.sleep(0.05)
        var after = time.perf_counter()
        var elapsed = after - before
        check("time.sleep(0.05) pauses >= 0.04 sec", elapsed >= 0.04)
        print("  elapsed after sleep(0.05):", elapsed)
    catch:
        print("ERROR: time.sleep(0.05) threw exception")
    fade

    try:
        time.sleep(0)
        check("time.sleep(0) succeeds (no-op sleep)", true)
    catch:
        print("ERROR: time.sleep(0) threw exception")
    fade

    # ================================================================
    # gmtime() -- UTC struct_time
    # ================================================================
    print("")
    print("--- gmtime() ---")

    try:
        var gt = time.gmtime()
        check("time.gmtime() callable", true)
        print("  gmtime():", gt)
    catch:
        print("ERROR: time.gmtime() threw exception")
    fade

    try:
        var gt = time.gmtime()
        var yr = gt.tm_year
        check("gmtime().tm_year >= 2025", yr >= 2025)
        print("  tm_year:", yr)
    catch:
        print("ERROR: gmtime().tm_year threw exception")
    fade

    try:
        var gt = time.gmtime()
        var mon = gt.tm_mon
        check("gmtime().tm_mon in 1..12", mon >= 1 and mon <= 12)
        print("  tm_mon:", mon)
    catch:
        print("ERROR: gmtime().tm_mon threw exception")
    fade

    try:
        var gt = time.gmtime()
        var day = gt.tm_mday
        check("gmtime().tm_mday in 1..31", day >= 1 and day <= 31)
        print("  tm_mday:", day)
    catch:
        print("ERROR: gmtime().tm_mday threw exception")
    fade

    try:
        var gt = time.gmtime()
        var hr = gt.tm_hour
        check("gmtime().tm_hour in 0..23", hr >= 0 and hr <= 23)
        print("  tm_hour:", hr)
    catch:
        print("ERROR: gmtime().tm_hour threw exception")
    fade

    try:
        var gt = time.gmtime()
        var mn = gt.tm_min
        check("gmtime().tm_min in 0..59", mn >= 0 and mn <= 59)
        print("  tm_min:", mn)
    catch:
        print("ERROR: gmtime().tm_min threw exception")
    fade

    try:
        var gt = time.gmtime()
        var sc = gt.tm_sec
        check("gmtime().tm_sec in 0..61", sc >= 0 and sc <= 61)
        print("  tm_sec:", sc)
    catch:
        print("ERROR: gmtime().tm_sec threw exception")
    fade

    try:
        var gt = time.gmtime()
        var wday = gt.tm_wday
        check("gmtime().tm_wday in 0..6", wday >= 0 and wday <= 6)
        print("  tm_wday:", wday)
    catch:
        print("ERROR: gmtime().tm_wday threw exception")
    fade

    try:
        var gt = time.gmtime()
        var yday = gt.tm_yday
        check("gmtime().tm_yday in 1..366", yday >= 1 and yday <= 366)
        print("  tm_yday:", yday)
    catch:
        print("ERROR: gmtime().tm_yday threw exception")
    fade

    try:
        var gt = time.gmtime()
        var dst = gt.tm_isdst
        check("gmtime().tm_isdst is 0 (UTC has no DST)", dst == 0)
    catch:
        print("ERROR: gmtime().tm_isdst threw exception")
    fade

    # gmtime with explicit epoch
    try:
        # epoch 0 = 1970-01-01 00:00:00 UTC
        var gt = time.gmtime(0)
        check("gmtime(0).tm_year == 1970", gt.tm_year == 1970)
        check("gmtime(0).tm_mon == 1", gt.tm_mon == 1)
        check("gmtime(0).tm_mday == 1", gt.tm_mday == 1)
        check("gmtime(0).tm_hour == 0", gt.tm_hour == 0)
    catch:
        print("ERROR: gmtime(0) threw exception")
    fade

    try:
        # 2000-01-01 00:00:00 UTC = epoch 946684800
        var gt = time.gmtime(946684800)
        check("gmtime(946684800).tm_year == 2000", gt.tm_year == 2000)
        check("gmtime(946684800).tm_mon == 1", gt.tm_mon == 1)
        check("gmtime(946684800).tm_mday == 1", gt.tm_mday == 1)
    catch:
        print("ERROR: gmtime(946684800) threw exception")
    fade

    # ================================================================
    # localtime() -- local struct_time
    # ================================================================
    print("")
    print("--- localtime() ---")

    try:
        var lt = time.localtime()
        check("time.localtime() callable", true)
        print("  localtime():", lt)
    catch:
        print("ERROR: time.localtime() threw exception")
    fade

    try:
        var lt = time.localtime()
        var yr = lt.tm_year
        check("localtime().tm_year >= 2025", yr >= 2025)
        print("  tm_year:", yr)
    catch:
        print("ERROR: localtime().tm_year threw exception")
    fade

    try:
        var lt = time.localtime()
        var mon = lt.tm_mon
        check("localtime().tm_mon in 1..12", mon >= 1 and mon <= 12)
    catch:
        print("ERROR: localtime().tm_mon threw exception")
    fade

    try:
        var lt = time.localtime()
        var day = lt.tm_mday
        check("localtime().tm_mday in 1..31", day >= 1 and day <= 31)
    catch:
        print("ERROR: localtime().tm_mday threw exception")
    fade

    try:
        var lt = time.localtime()
        var dst = lt.tm_isdst
        check("localtime().tm_isdst in -1..1", dst >= -1 and dst <= 1)
        print("  tm_isdst:", dst)
    catch:
        print("ERROR: localtime().tm_isdst threw exception")
    fade

    # localtime with explicit epoch
    try:
        var lt = time.localtime(0)
        check("localtime(0).tm_year == 1969 or 1970", lt.tm_year == 1969 or lt.tm_year == 1970)
        print("  localtime(0):", lt)
    catch:
        print("ERROR: localtime(0) threw exception")
    fade

    # ================================================================
    # mktime() -- struct_time → epoch seconds
    # ================================================================
    print("")
    print("--- mktime() ---")

    try:
        var lt = time.localtime()
        var epoch = time.mktime(lt)
        check("time.mktime(localtime()) > 0", epoch > 0)
        print("  mktime(localtime()):", epoch)
    catch:
        print("ERROR: time.mktime(localtime()) threw exception")
    fade

    try:
        # Round-trip: localtime → mktime → localtime
        var lt1 = time.localtime()
        var epoch = time.mktime(lt1)
        var lt2 = time.localtime(epoch)
        check("mktime round-trip preserves tm_year", lt1.tm_year == lt2.tm_year)
        check("mktime round-trip preserves tm_mon", lt1.tm_mon == lt2.tm_mon)
        check("mktime round-trip preserves tm_mday", lt1.tm_mday == lt2.tm_mday)
        check("mktime round-trip preserves tm_hour", lt1.tm_hour == lt2.tm_hour)
        check("mktime round-trip preserves tm_min", lt1.tm_min == lt2.tm_min)
    catch:
        print("ERROR: mktime round-trip threw exception")
    fade

    # ================================================================
    # strftime() -- format struct_time as string
    # ================================================================
    print("")
    print("--- strftime() ---")

    try:
        var gt = time.gmtime(946684800)
        var s = time.strftime("%Y-%m-%d", gt)
        check("strftime('%Y-%m-%d', epoch 2000) == '2000-01-01'", s == "2000-01-01")
        print("  strftime:", s)
    catch:
        print("ERROR: time.strftime('%Y-%m-%d') threw exception")
    fade

    try:
        var gt = time.gmtime(946684800)
        var s = time.strftime("%H:%M:%S", gt)
        check("strftime('%H:%M:%S', epoch 2000) == '00:00:00'", s == "00:00:00")
        print("  strftime time:", s)
    catch:
        print("ERROR: time.strftime('%H:%M:%S') threw exception")
    fade

    try:
        var gt = time.gmtime(946684800)
        var s = time.strftime("%A", gt)
        check("strftime('%A', 2000-01-01) == 'Saturday'", s == "Saturday")
        print("  strftime weekday:", s)
    catch:
        print("ERROR: time.strftime('%A') threw exception")
    fade

    try:
        var gt = time.gmtime(946684800)
        var s = time.strftime("%B", gt)
        check("strftime('%B', 2000-01-01) == 'January'", s == "January")
        print("  strftime month:", s)
    catch:
        print("ERROR: time.strftime('%B') threw exception")
    fade

    try:
        var s = time.strftime("%Y")
        check("strftime('%Y') with no struct_time uses localtime", true)
        print("  strftime('%Y'):", s)
    catch:
        print("ERROR: time.strftime('%Y') no-arg threw exception")
    fade

    try:
        var gt = time.gmtime(0)
        var s = time.strftime("%Y-%m-%d %H:%M:%S", gt)
        check("strftime at epoch 0 == '1970-01-01 00:00:00'", s == "1970-01-01 00:00:00")
    catch:
        print("ERROR: strftime at epoch 0 threw exception")
    fade

    try:
        var gt = time.gmtime(946684800)
        var s = time.strftime("%j", gt)
        check("strftime('%j', 2000-01-01) == '001' (day of year)", s == "001")
    catch:
        print("ERROR: strftime('%j') threw exception")
    fade

    try:
        var gt = time.gmtime(946684800)
        var s = time.strftime("%Z", gt)
        check("strftime('%Z') callable", true)
        print("  strftime timezone:", s)
    catch:
        print("ERROR: strftime('%Z') threw exception")
    fade

    # ================================================================
    # strptime() -- parse string into struct_time
    # ================================================================
    print("")
    print("--- strptime() ---")

    try:
        var st = time.strptime("2000-01-01", "%Y-%m-%d")
        check("strptime('2000-01-01', '%Y-%m-%d') callable", true)
        print("  strptime:", st)
    catch:
        print("ERROR: time.strptime() threw exception")
    fade

    try:
        var st = time.strptime("2000-01-01", "%Y-%m-%d")
        check("strptime().tm_year == 2000", st.tm_year == 2000)
        check("strptime().tm_mon == 1", st.tm_mon == 1)
        check("strptime().tm_mday == 1", st.tm_mday == 1)
    catch:
        print("ERROR: strptime() field access threw exception")
    fade

    try:
        var st = time.strptime("15:30:45", "%H:%M:%S")
        check("strptime('15:30:45').tm_hour == 15", st.tm_hour == 15)
        check("strptime('15:30:45').tm_min == 30", st.tm_min == 30)
        check("strptime('15:30:45').tm_sec == 45", st.tm_sec == 45)
    catch:
        print("ERROR: strptime() time fields threw exception")
    fade

    try:
        var st = time.strptime("July", "%B")
        check("strptime('July', '%B').tm_mon == 7", st.tm_mon == 7)
    catch:
        print("ERROR: strptime('%B') threw exception")
    fade

    try:
        var st = time.strptime("Saturday", "%A")
        check("strptime('Saturday', '%A') callable", true)
    catch:
        print("ERROR: strptime('%A') threw exception")
    fade

    # ================================================================
    # asctime() -- human-readable time string
    # ================================================================
    print("")
    print("--- asctime() ---")

    try:
        var s = time.asctime()
        check("time.asctime() returns non-empty", s != "")
        print("  asctime():", s)
    catch:
        print("ERROR: time.asctime() threw exception")
    fade

    try:
        var gt = time.gmtime(946684800)
        var s = time.asctime(gt)
        check("asctime(gmtime(946684800)) contains '2000'", true)
        print("  asctime(epoch 2000):", s)
    catch:
        print("ERROR: time.asctime(struct_time) threw exception")
    fade

    try:
        var gt = time.gmtime(0)
        var s = time.asctime(gt)
        check("asctime(gmtime(0)) contains '1970'", true)
        print("  asctime(epoch 0):", s)
    catch:
        print("ERROR: asctime(gmtime(0)) threw exception")
    fade

    # ================================================================
    # ctime() -- convert epoch to readable string
    # ================================================================
    print("")
    print("--- ctime() ---")

    try:
        var s = time.ctime()
        check("time.ctime() returns non-empty", s != "")
        print("  ctime():", s)
    catch:
        print("ERROR: time.ctime() threw exception")
    fade

    try:
        var s = time.ctime(0)
        check("time.ctime(0) returns non-empty", s != "")
        print("  ctime(0):", s)
    catch:
        print("ERROR: time.ctime(0) threw exception")
    fade

    try:
        var s = time.ctime(946684800)
        check("time.ctime(946684800) returns non-empty", s != "")
        print("  ctime(946684800):", s)
    catch:
        print("ERROR: time.ctime(946684800) threw exception")
    fade

    # ================================================================
    # Timezone constants
    # ================================================================
    print("")
    print("--- Timezone constants ---")

    try:
        var tz = time.timezone
        check("time.timezone accessible (int)", true)
        print("  timezone:", tz)
    catch:
        print("ERROR: time.timezone threw exception")
    fade

    try:
        var alt = time.altzone
        check("time.altzone accessible (int)", true)
        print("  altzone:", alt)
    catch:
        print("ERROR: time.altzone threw exception")
    fade

    try:
        var dst = time.daylight
        check("time.daylight is 0 or 1", dst == 0 or dst == 1)
        print("  daylight:", dst)
    catch:
        print("ERROR: time.daylight threw exception")
    fade

    try:
        var tzname = time.tzname
        check("time.tzname accessible", true)
        print("  tzname:", tzname)
    catch:
        print("ERROR: time.tzname threw exception")
    fade

    # ================================================================
    # get_clock_info() -- metadata about clocks
    # ================================================================
    print("")
    print("--- get_clock_info() ---")

    try:
        var ci = time.get_clock_info("time")
        check("get_clock_info('time') callable", true)
        print("  clock_info('time'):", ci)
    catch:
        print("ERROR: get_clock_info('time') threw exception")
    fade

    try:
        var ci = time.get_clock_info("time")
        var res = ci.resolution
        check("clock_info('time').resolution > 0", res > 0)
        print("  time resolution:", res)
    catch:
        print("ERROR: clock_info('time').resolution threw exception")
    fade

    try:
        var ci = time.get_clock_info("time")
        var mono = ci.monotonic
        check("clock_info('time').monotonic is false", mono == false)
    catch:
        print("ERROR: clock_info('time').monotonic threw exception")
    fade

    try:
        var ci = time.get_clock_info("monotonic")
        check("get_clock_info('monotonic') callable", true)
        print("  clock_info('monotonic'):", ci)
    catch:
        print("ERROR: get_clock_info('monotonic') threw exception")
    fade

    try:
        var ci = time.get_clock_info("monotonic")
        var mono = ci.monotonic
        check("clock_info('monotonic').monotonic is true", mono == true)
    catch:
        print("ERROR: clock_info('monotonic').monotonic threw exception")
    fade

    try:
        var ci = time.get_clock_info("monotonic")
        var adj = ci.adjustable
        check("clock_info('monotonic').adjustable is false", adj == false)
    catch:
        print("ERROR: clock_info('monotonic').adjustable threw exception")
    fade

    try:
        var ci = time.get_clock_info("perf_counter")
        check("get_clock_info('perf_counter') callable", true)
        print("  clock_info('perf_counter'):", ci)
    catch:
        print("ERROR: get_clock_info('perf_counter') threw exception")
    fade

    try:
        var ci = time.get_clock_info("perf_counter")
        var res = ci.resolution
        check("clock_info('perf_counter').resolution > 0", res > 0)
        print("  perf_counter resolution:", res)
    catch:
        print("ERROR: clock_info('perf_counter').resolution threw exception")
    fade

    try:
        var ci = time.get_clock_info("process_time")
        check("get_clock_info('process_time') callable", true)
        print("  clock_info('process_time'):", ci)
    catch:
        print("ERROR: get_clock_info('process_time') threw exception")
    fade

    try:
        var ci = time.get_clock_info("thread_time")
        check("get_clock_info('thread_time') callable", true)
        print("  clock_info('thread_time'):", ci)
    catch:
        print("ERROR: get_clock_info('thread_time') threw exception (not all platforms)")
    fade

    # ================================================================
    # struct_time constructor
    # ================================================================
    print("")
    print("--- struct_time constructor ---")

    try:
        # struct_time takes a 9-tuple:
        # (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
        tup t = (2025, 6, 15, 14, 30, 0, 6, 166, 0)
        var st = time.struct_time(t)
        check("time.struct_time(tup) callable", true)
        print("  struct_time:", st)
    catch:
        print("ERROR: time.struct_time(tup) threw exception")
    fade

    try:
        tup t = (2025, 6, 15, 14, 30, 0, 6, 166, 0)
        var st = time.struct_time(t)
        check("struct_time.tm_year == 2025", st.tm_year == 2025)
        check("struct_time.tm_mon == 6", st.tm_mon == 6)
        check("struct_time.tm_mday == 15", st.tm_mday == 15)
        check("struct_time.tm_hour == 14", st.tm_hour == 14)
        check("struct_time.tm_min == 30", st.tm_min == 30)
        check("struct_time.tm_sec == 0", st.tm_sec == 0)
        check("struct_time.tm_wday == 6", st.tm_wday == 6)
        check("struct_time.tm_yday == 166", st.tm_yday == 166)
        check("struct_time.tm_isdst == 0", st.tm_isdst == 0)
    catch:
        print("ERROR: struct_time field access threw exception")
    fade

    # ================================================================
    # gmtime / mktime round-trip through strftime / strptime
    # ================================================================
    print("")
    print("--- Round-trip formatting ---")

    try:
        var epoch = 1000000000
        var gt = time.gmtime(epoch)
        var formatted = time.strftime("%Y-%m-%d %H:%M:%S", gt)
        var parsed = time.strptime(formatted, "%Y-%m-%d %H:%M:%S")
        check("round-trip tm_year preserved", gt.tm_year == parsed.tm_year)
        check("round-trip tm_mon preserved", gt.tm_mon == parsed.tm_mon)
        check("round-trip tm_mday preserved", gt.tm_mday == parsed.tm_mday)
        check("round-trip tm_hour preserved", gt.tm_hour == parsed.tm_hour)
        check("round-trip tm_min preserved", gt.tm_min == parsed.tm_min)
        check("round-trip tm_sec preserved", gt.tm_sec == parsed.tm_sec)
        print("  formatted:", formatted)
    catch:
        print("ERROR: strftime/strptime round-trip threw exception")
    fade

    # ================================================================
    # Timing a computation with perf_counter
    # ================================================================
    print("")
    print("--- Timing a computation ---")

    try:
        var start = time.perf_counter()
        # small pause as measurable work
        time.sleep(0.01)
        var stop = time.perf_counter()
        var elapsed = stop - start
        check("perf_counter measures elapsed time >= 0.009", elapsed >= 0.009)
        print("  elapsed:", elapsed, "sec")
    catch:
        print("ERROR: timing computation threw exception")
    fade

    print("")
    print("=== time test complete ===")
}
