# core_datetime.ly
# Lyric adhoc test — exercises every public method and attribute of Python's datetime module.
#
# Run with:  lyric run lyric/tests/python_modules/core_datetime.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions

importpy datetime

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
    print("=== Lyric datetime module adhoc test ===")
    print("")

    # ================================================================
    # datetime.datetime
    # ================================================================
    print("--- datetime.datetime ---")

    # now()
    try:
        var now = datetime.datetime.now()
        check("datetime.datetime.now() works", true)
    catch:
        print("ERROR: datetime.datetime.now() threw exception")
    fade

    # today()
    try:
        var today_dt = datetime.datetime.today()
        check("datetime.datetime.today() works", true)
    catch:
        print("ERROR: datetime.datetime.today() threw exception")
    fade

    # utcnow()
    try:
        var utc_now = datetime.datetime.utcnow()
        check("datetime.datetime.utcnow() works", true)
    catch:
        print("ERROR: datetime.datetime.utcnow() threw exception (deprecated in 3.12+)")
    fade

    # .year .month .day .hour .minute .second .microsecond
    try:
        var now = datetime.datetime.now()
        var yr = now.year
        var mo = now.month
        var dy = now.day
        var hr = now.hour
        var mn = now.minute
        var sc = now.second
        var us = now.microsecond
        check("now.year >= 2025", yr >= 2025)
        check("now.month in 1-12", mo >= 1 and mo <= 12)
        check("now.day in 1-31", dy >= 1 and dy <= 31)
        check("now.hour in 0-23", hr >= 0 and hr <= 23)
        check("now.minute in 0-59", mn >= 0 and mn <= 59)
        check("now.second in 0-59", sc >= 0 and sc <= 59)
        check("now.microsecond in 0-999999", us >= 0 and us <= 999999)
    catch:
        print("ERROR: datetime instance attributes (.year etc.) threw exception")
    fade

    # constructor
    try:
        var dt = datetime.datetime(2024, 6, 15, 10, 30, 45)
        check("datetime.datetime(2024,6,15,10,30,45) constructor works", true)
        check("constructor .year == 2024", dt.year == 2024)
        check("constructor .month == 6", dt.month == 6)
        check("constructor .day == 15", dt.day == 15)
        check("constructor .hour == 10", dt.hour == 10)
        check("constructor .minute == 30", dt.minute == 30)
        check("constructor .second == 45", dt.second == 45)
        check("constructor .microsecond == 0", dt.microsecond == 0)
    catch:
        print("ERROR: datetime.datetime() constructor threw exception")
    fade

    # .isoformat()
    try:
        var dt = datetime.datetime(2024, 6, 15, 10, 30, 45)
        var iso = dt.isoformat()
        check("datetime.isoformat() works", true)
        print("  isoformat:", iso)
    catch:
        print("ERROR: datetime.isoformat() threw exception")
    fade

    # .ctime()
    try:
        var dt = datetime.datetime(2024, 6, 15, 10, 30, 45)
        var ct = dt.ctime()
        check("datetime.ctime() works", true)
        print("  ctime:", ct)
    catch:
        print("ERROR: datetime.ctime() threw exception")
    fade

    # .strftime()
    try:
        var dt = datetime.datetime(2024, 6, 15, 10, 30, 45)
        var fmt = dt.strftime("%Y-%m-%d %H:%M:%S")
        check("datetime.strftime() works", true)
        print("  strftime:", fmt)
    catch:
        print("ERROR: datetime.strftime() threw exception")
    fade

    # .date()
    try:
        var dt = datetime.datetime(2024, 6, 15, 10, 30, 45)
        var d = dt.date()
        check("datetime.date() returns object", true)
        check("datetime.date().year == 2024", d.year == 2024)
        check("datetime.date().month == 6", d.month == 6)
        check("datetime.date().day == 15", d.day == 15)
    catch:
        print("ERROR: datetime.date() threw exception")
    fade

    # .time()
    try:
        var dt = datetime.datetime(2024, 6, 15, 10, 30, 45)
        var t = dt.time()
        check("datetime.time() returns object", true)
        check("datetime.time().hour == 10", t.hour == 10)
        check("datetime.time().minute == 30", t.minute == 30)
        check("datetime.time().second == 45", t.second == 45)
    catch:
        print("ERROR: datetime.time() threw exception")
    fade

    # .weekday()  — 2024-06-15 is Saturday = 5
    try:
        var dt = datetime.datetime(2024, 6, 15, 0, 0, 0)
        var wd = dt.weekday()
        check("datetime(2024,6,15).weekday() == 5 (Saturday)", wd == 5)
    catch:
        print("ERROR: datetime.weekday() threw exception")
    fade

    # .isoweekday()  — Saturday = 6
    try:
        var dt = datetime.datetime(2024, 6, 15, 0, 0, 0)
        var iwd = dt.isoweekday()
        check("datetime(2024,6,15).isoweekday() == 6 (Saturday)", iwd == 6)
    catch:
        print("ERROR: datetime.isoweekday() threw exception")
    fade

    # .isocalendar()
    try:
        var dt = datetime.datetime(2024, 6, 15, 0, 0, 0)
        var ic = dt.isocalendar()
        check("datetime.isocalendar() works", true)
        print("  isocalendar:", ic)
    catch:
        print("ERROR: datetime.isocalendar() threw exception")
    fade

    # .timestamp()
    try:
        var dt = datetime.datetime(2024, 1, 1, 0, 0, 0)
        var ts = dt.timestamp()
        check("datetime.timestamp() > 1700000000", ts > 1700000000)
        print("  timestamp:", ts)
    catch:
        print("ERROR: datetime.timestamp() threw exception")
    fade

    # .toordinal()
    try:
        var dt = datetime.datetime(2024, 1, 1, 0, 0, 0)
        var ord_val = dt.toordinal()
        check("datetime.toordinal() > 738000", ord_val > 738000)
        print("  toordinal:", ord_val)
    catch:
        print("ERROR: datetime.toordinal() threw exception")
    fade

    # .timetuple()
    try:
        var dt = datetime.datetime(2024, 6, 15, 10, 30, 45)
        var tt = dt.timetuple()
        check("datetime.timetuple() works", true)
        print("  timetuple:", tt)
    catch:
        print("ERROR: datetime.timetuple() threw exception")
    fade

    # .utctimetuple()
    try:
        var dt = datetime.datetime(2024, 6, 15, 10, 30, 45)
        var utt = dt.utctimetuple()
        check("datetime.utctimetuple() works", true)
    catch:
        print("ERROR: datetime.utctimetuple() threw exception")
    fade

    # .replace() — positional: replace year
    try:
        var dt = datetime.datetime(2024, 6, 15, 10, 30, 45)
        var dt2 = dt.replace(2025)
        check("datetime.replace(2025) sets year", dt2.year == 2025)
        check("datetime.replace(2025) keeps month", dt2.month == 6)
        check("datetime.replace(2025) keeps day", dt2.day == 15)
    catch:
        print("ERROR: datetime.replace() threw exception (may require keyword args)")
    fade

    # .fromtimestamp()
    try:
        var dt = datetime.datetime.fromtimestamp(1000000000)
        check("datetime.fromtimestamp(1e9) works", true)
        check("datetime.fromtimestamp(1e9).year > 2000", dt.year > 2000)
        print("  fromtimestamp(1e9):", dt.year, dt.month, dt.day)
    catch:
        print("ERROR: datetime.fromtimestamp() threw exception")
    fade

    # .utcfromtimestamp()
    try:
        var dt = datetime.datetime.utcfromtimestamp(1000000000)
        check("datetime.utcfromtimestamp(1e9) works", true)
        print("  utcfromtimestamp(1e9):", dt.year, dt.month, dt.day)
    catch:
        print("ERROR: datetime.utcfromtimestamp() threw exception")
    fade

    # .fromordinal()
    try:
        var dt = datetime.datetime.fromordinal(738521)
        check("datetime.fromordinal(738521) works", true)
        print("  fromordinal(738521):", dt.year, dt.month, dt.day)
    catch:
        print("ERROR: datetime.fromordinal() threw exception")
    fade

    # .fromisoformat()
    try:
        var dt = datetime.datetime.fromisoformat("2024-06-15T10:30:45")
        check("datetime.fromisoformat() .year == 2024", dt.year == 2024)
        check("datetime.fromisoformat() .hour == 10", dt.hour == 10)
        check("datetime.fromisoformat() .second == 45", dt.second == 45)
    catch:
        print("ERROR: datetime.fromisoformat() threw exception")
    fade

    # .strptime()
    try:
        var dt = datetime.datetime.strptime("2024-06-15 10:30:45", "%Y-%m-%d %H:%M:%S")
        check("datetime.strptime() .year == 2024", dt.year == 2024)
        check("datetime.strptime() .month == 6", dt.month == 6)
        check("datetime.strptime() .hour == 10", dt.hour == 10)
    catch:
        print("ERROR: datetime.strptime() threw exception")
    fade

    # .combine()
    try:
        var d = datetime.date(2024, 6, 15)
        var t = datetime.time(10, 30, 0)
        var combined = datetime.datetime.combine(d, t)
        check("datetime.combine(date, time) works", true)
        check("combined.year == 2024", combined.year == 2024)
        check("combined.month == 6", combined.month == 6)
        check("combined.day == 15", combined.day == 15)
        check("combined.hour == 10", combined.hour == 10)
        check("combined.minute == 30", combined.minute == 30)
    catch:
        print("ERROR: datetime.combine() threw exception")
    fade

    # .min and .max
    try:
        var dt_min = datetime.datetime.min
        var dt_max = datetime.datetime.max
        check("datetime.datetime.min exists", true)
        check("datetime.datetime.max exists", true)
        check("datetime.min.year == 1", dt_min.year == 1)
        check("datetime.max.year == 9999", dt_max.year == 9999)
        print("  datetime.min:", dt_min)
        print("  datetime.max:", dt_max)
    catch:
        print("ERROR: datetime.datetime.min/max threw exception")
    fade

    # .resolution
    try:
        var res = datetime.datetime.resolution
        check("datetime.datetime.resolution exists", true)
        print("  datetime.resolution:", res)
    catch:
        print("ERROR: datetime.datetime.resolution threw exception")
    fade

    # ================================================================
    # datetime.date
    # ================================================================
    print("")
    print("--- datetime.date ---")

    # today()
    try:
        var today = datetime.date.today()
        check("datetime.date.today() works", true)
        check("date.today().year >= 2025", today.year >= 2025)
        print("  today:", today)
    catch:
        print("ERROR: datetime.date.today() threw exception")
    fade

    # constructor
    try:
        var d = datetime.date(2024, 6, 15)
        check("datetime.date(2024,6,15) constructor works", true)
        check("date .year == 2024", d.year == 2024)
        check("date .month == 6", d.month == 6)
        check("date .day == 15", d.day == 15)
    catch:
        print("ERROR: datetime.date() constructor threw exception")
    fade

    # .isoformat()
    try:
        var d = datetime.date(2024, 6, 15)
        var iso = d.isoformat()
        check("date.isoformat() works", true)
        print("  date.isoformat:", iso)
    catch:
        print("ERROR: date.isoformat() threw exception")
    fade

    # .ctime()
    try:
        var d = datetime.date(2024, 6, 15)
        var ct = d.ctime()
        check("date.ctime() works", true)
        print("  date.ctime:", ct)
    catch:
        print("ERROR: date.ctime() threw exception")
    fade

    # .strftime()
    try:
        var d = datetime.date(2024, 6, 15)
        var fmt = d.strftime("%d/%m/%Y")
        check("date.strftime() works", true)
        print("  date.strftime:", fmt)
    catch:
        print("ERROR: date.strftime() threw exception")
    fade

    # .weekday()  — 2024-06-15 = Saturday = 5
    try:
        var d = datetime.date(2024, 6, 15)
        check("date(2024,6,15).weekday() == 5 (Saturday)", d.weekday() == 5)
    catch:
        print("ERROR: date.weekday() threw exception")
    fade

    # .isoweekday()  — Saturday = 6
    try:
        var d = datetime.date(2024, 6, 15)
        check("date(2024,6,15).isoweekday() == 6 (Saturday)", d.isoweekday() == 6)
    catch:
        print("ERROR: date.isoweekday() threw exception")
    fade

    # .isocalendar()
    try:
        var d = datetime.date(2024, 6, 15)
        var ic = d.isocalendar()
        check("date.isocalendar() works", true)
        print("  date.isocalendar:", ic)
    catch:
        print("ERROR: date.isocalendar() threw exception")
    fade

    # .timetuple()
    try:
        var d = datetime.date(2024, 6, 15)
        var tt = d.timetuple()
        check("date.timetuple() works", true)
        print("  date.timetuple:", tt)
    catch:
        print("ERROR: date.timetuple() threw exception")
    fade

    # .toordinal()
    try:
        var d = datetime.date(2024, 6, 15)
        var ord_val = d.toordinal()
        check("date.toordinal() > 738000", ord_val > 738000)
        print("  date.toordinal:", ord_val)
    catch:
        print("ERROR: date.toordinal() threw exception")
    fade

    # .fromordinal()
    try:
        var d = datetime.date(2024, 1, 1)
        var ord_val = d.toordinal()
        var d2 = datetime.date.fromordinal(ord_val)
        check("date.fromordinal(ordinal).year == 2024", d2.year == 2024)
        check("date.fromordinal(ordinal).month == 1", d2.month == 1)
        check("date.fromordinal(ordinal).day == 1", d2.day == 1)
    catch:
        print("ERROR: date.fromordinal() threw exception")
    fade

    # .fromisoformat()
    try:
        var d = datetime.date.fromisoformat("2024-06-15")
        check("date.fromisoformat() .year == 2024", d.year == 2024)
        check("date.fromisoformat() .month == 6", d.month == 6)
        check("date.fromisoformat() .day == 15", d.day == 15)
    catch:
        print("ERROR: date.fromisoformat() threw exception")
    fade

    # .fromtimestamp()
    try:
        var d = datetime.date.fromtimestamp(1000000000)
        check("date.fromtimestamp(1e9) works", true)
        print("  date.fromtimestamp(1e9):", d.year, d.month, d.day)
    catch:
        print("ERROR: date.fromtimestamp() threw exception")
    fade

    # .replace()
    try:
        var d = datetime.date(2024, 6, 15)
        var d2 = d.replace(2025)
        check("date.replace(2025) sets year", d2.year == 2025)
        check("date.replace(2025) keeps month", d2.month == 6)
        check("date.replace(2025) keeps day", d2.day == 15)
    catch:
        print("ERROR: date.replace() threw exception (may require keyword args)")
    fade

    # .min and .max
    try:
        var d_min = datetime.date.min
        var d_max = datetime.date.max
        check("datetime.date.min exists", true)
        check("datetime.date.max exists", true)
        check("date.min.year == 1", d_min.year == 1)
        check("date.max.year == 9999", d_max.year == 9999)
        print("  date.min:", d_min)
        print("  date.max:", d_max)
    catch:
        print("ERROR: datetime.date.min/max threw exception")
    fade

    # .resolution
    try:
        var res = datetime.date.resolution
        check("datetime.date.resolution exists", true)
        print("  date.resolution:", res)
    catch:
        print("ERROR: date.resolution threw exception")
    fade

    # ================================================================
    # datetime.time
    # ================================================================
    print("")
    print("--- datetime.time ---")

    # constructor (midnight)
    try:
        var t = datetime.time(0, 0, 0)
        check("datetime.time(0,0,0) constructor works", true)
        check("time(0,0,0).hour == 0", t.hour == 0)
        check("time(0,0,0).minute == 0", t.minute == 0)
        check("time(0,0,0).second == 0", t.second == 0)
        check("time(0,0,0).microsecond == 0", t.microsecond == 0)
    catch:
        print("ERROR: datetime.time(0,0,0) constructor threw exception")
    fade

    # constructor with values
    try:
        var t = datetime.time(14, 30, 59)
        check("time(14,30,59).hour == 14", t.hour == 14)
        check("time(14,30,59).minute == 30", t.minute == 30)
        check("time(14,30,59).second == 59", t.second == 59)
    catch:
        print("ERROR: datetime.time(14,30,59) constructor threw exception")
    fade

    # constructor with microseconds
    try:
        var t = datetime.time(10, 30, 45, 123456)
        check("time(10,30,45,123456).microsecond == 123456", t.microsecond == 123456)
    catch:
        print("ERROR: time constructor with microseconds threw exception")
    fade

    # .isoformat()
    try:
        var t = datetime.time(14, 30, 59)
        var iso = t.isoformat()
        check("time.isoformat() works", true)
        print("  time.isoformat:", iso)
    catch:
        print("ERROR: time.isoformat() threw exception")
    fade

    # .strftime()
    try:
        var t = datetime.time(14, 30, 59)
        var fmt = t.strftime("%H:%M:%S")
        check("time.strftime('%H:%M:%S') works", true)
        print("  time.strftime:", fmt)
    catch:
        print("ERROR: time.strftime() threw exception")
    fade

    # .replace()
    try:
        var t = datetime.time(14, 30, 59)
        var t2 = t.replace(10)
        check("time.replace(10) sets hour", t2.hour == 10)
        check("time.replace(10) keeps minute", t2.minute == 30)
    catch:
        print("ERROR: time.replace() threw exception (may require keyword args)")
    fade

    # .min and .max
    try:
        var t_min = datetime.time.min
        var t_max = datetime.time.max
        check("datetime.time.min exists", true)
        check("datetime.time.max exists", true)
        check("time.min.hour == 0", t_min.hour == 0)
        check("time.max.hour == 23", t_max.hour == 23)
        print("  time.min:", t_min)
        print("  time.max:", t_max)
    catch:
        print("ERROR: datetime.time.min/max threw exception")
    fade

    # .resolution
    try:
        var res = datetime.time.resolution
        check("datetime.time.resolution exists", true)
        print("  time.resolution:", res)
    catch:
        print("ERROR: time.resolution threw exception")
    fade

    # ================================================================
    # datetime.timedelta
    # ================================================================
    print("")
    print("--- datetime.timedelta ---")

    # constructor: days (positional arg 1)
    try:
        var td = datetime.timedelta(7)
        check("timedelta(7).days == 7", td.days == 7)
        check("timedelta(7).seconds == 0", td.seconds == 0)
        check("timedelta(7).microseconds == 0", td.microseconds == 0)
    catch:
        print("ERROR: datetime.timedelta(7) threw exception")
    fade

    # constructor: days, seconds (positional args 1-2)
    try:
        var td = datetime.timedelta(0, 3600)
        check("timedelta(0,3600).days == 0", td.days == 0)
        check("timedelta(0,3600).seconds == 3600", td.seconds == 3600)
    catch:
        print("ERROR: datetime.timedelta(0,3600) threw exception")
    fade

    # constructor: days, seconds, microseconds (positional args 1-3)
    try:
        var td = datetime.timedelta(0, 0, 500000)
        check("timedelta(0,0,500000).microseconds == 500000", td.microseconds == 500000)
    catch:
        print("ERROR: datetime.timedelta(0,0,500000) threw exception")
    fade

    # negative timedelta
    try:
        var td = datetime.timedelta(-1)
        check("timedelta(-1).days == -1", td.days == -1)
    catch:
        print("ERROR: datetime.timedelta(-1) threw exception")
    fade

    # .total_seconds() — 1 day = 86400.0
    try:
        var td = datetime.timedelta(1)
        var ts = td.total_seconds()
        check("timedelta(1).total_seconds() == 86400.0", ts == 86400.0)
        print("  total_seconds(1 day):", ts)
    catch:
        print("ERROR: timedelta.total_seconds() threw exception")
    fade

    # .total_seconds() — 1 hour = 3600.0
    try:
        var td = datetime.timedelta(0, 3600)
        var ts = td.total_seconds()
        check("timedelta(0,3600).total_seconds() == 3600.0", ts == 3600.0)
    catch:
        print("ERROR: timedelta.total_seconds() (1 hour) threw exception")
    fade

    # .min and .max
    try:
        var td_min = datetime.timedelta.min
        var td_max = datetime.timedelta.max
        check("datetime.timedelta.min exists", true)
        check("datetime.timedelta.max exists", true)
        check("timedelta.min.days < 0", td_min.days < 0)
        check("timedelta.max.days > 0", td_max.days > 0)
        print("  timedelta.min:", td_min)
        print("  timedelta.max:", td_max)
    catch:
        print("ERROR: datetime.timedelta.min/max threw exception")
    fade

    # .resolution
    try:
        var res = datetime.timedelta.resolution
        check("datetime.timedelta.resolution exists", true)
        print("  timedelta.resolution:", res)
    catch:
        print("ERROR: timedelta.resolution threw exception")
    fade

    # ================================================================
    # datetime.timezone
    # ================================================================
    print("")
    print("--- datetime.timezone ---")

    # .utc class attribute
    try:
        var utc = datetime.timezone.utc
        check("datetime.timezone.utc exists", true)
        print("  timezone.utc:", utc)
    catch:
        print("ERROR: datetime.timezone.utc threw exception")
    fade

    # constructor with positive offset (UTC+1 = 3600 seconds)
    try:
        var offset = datetime.timedelta(0, 3600)
        var tz_plus1 = datetime.timezone(offset)
        check("datetime.timezone(timedelta(0,3600)) creates UTC+1", true)
        print("  timezone(UTC+1):", tz_plus1)
    catch:
        print("ERROR: datetime.timezone() constructor threw exception")
    fade

    # constructor with negative offset (UTC-5 = timedelta(-1, 68400))
    try:
        var offset = datetime.timedelta(-1, 68400)
        var tz_minus5 = datetime.timezone(offset)
        check("datetime.timezone(UTC-5) works", true)
        print("  timezone(UTC-5):", tz_minus5)
    catch:
        print("ERROR: datetime.timezone(UTC-5) constructor threw exception")
    fade

    # .utcoffset() on timezone.utc
    try:
        var utc = datetime.timezone.utc
        var now = datetime.datetime.now()
        var off = utc.utcoffset(now)
        check("timezone.utc.utcoffset(dt) works", true)
        print("  utc.utcoffset:", off)
    catch:
        print("ERROR: timezone.utcoffset() threw exception")
    fade

    # .tzname() on timezone.utc
    try:
        var utc = datetime.timezone.utc
        var now = datetime.datetime.now()
        var name = utc.tzname(now)
        check("timezone.utc.tzname(dt) == 'UTC'", name == "UTC")
        print("  utc.tzname:", name)
    catch:
        print("ERROR: timezone.tzname() threw exception")
    fade

    # .dst() on timezone.utc
    try:
        var utc = datetime.timezone.utc
        var now = datetime.datetime.now()
        var dst_val = utc.dst(now)
        check("timezone.utc.dst(dt) works", true)
        print("  utc.dst:", dst_val)
    catch:
        print("ERROR: timezone.dst() threw exception")
    fade

    print("")
    print("=== datetime test complete ===")
}
