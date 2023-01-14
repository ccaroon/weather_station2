import re

# time.mktime() : tuple -> seconds
# time.localtime() : seconds -> tuple
import time
import urequests

from machine import RTC

class Chronos:
    CLOCK   = RTC()
    CRONTAB = {}

    def __init__(self):
        pass

    @classmethod
    def sync(cls):
        """Sync with 'Internet' Time"""
        data = None

        api_url = "http://worldtimeapi.org/api/timezone/America/New_York"
        resp = urequests.get(api_url)
        if resp.status_code == 200:
            data = resp.json()
        else:
            raise Exception("Error Sync'ing Time: [%d]" % (resp.status_code))

        # 2022-12-20T12:51:23.758998-05:00
        current_time = data['datetime']

        matches = re.match("(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)\.\d+(\+|-)(\d+):\d+", current_time)

        if not matches:
            raise Exception("Error Parsing DateTime: %s" % (current_time))

        now = []

        # year, month, day, weekday, hour, minute, second, microsecond
        # 1-3 == YYYY, MM, DD
        for i in range(1,4):
            now.append(int(matches.group(i)))

        # weekday
        now.append(None)

        # 4-6 = HH, mm, ss
        for i in range(4,7):
            now.append(int(matches.group(i)))

        # Add microseconds
        now.append(0)

        # 6-7 == (+|-), TZOffset
        # tz = int(matches.group(8))
        # if matches.group(7) == '-':
        #     tz *= -1
        # now.append(tz)

        cls.CLOCK.datetime(now)

    @classmethod
    def every(cls, period, name, handler, **kwargs):
        matches = re.match("(\d+)([DdHhMm])", period)
        if matches == None:
            raise ValueError("Invalid period [%s]" % (period))

        period_value = int(matches.group(1))
        period_units = matches.group(2).upper()

        period_in_secs = cls.__convert_period_to_seconds(period_value, period_units)

        last_run = time.mktime(time.localtime())
        lrun = kwargs.get('last_run', None)
        if lrun:
            last_run = time.mktime(lrun)

        cls.CRONTAB[name] = {
            "period": period_in_secs,
            "last_run": last_run,
            "handler": handler
        }

    @classmethod
    def tick(cls, debug=False):
        now = time.mktime(time.localtime())

        for name, cron in cls.CRONTAB.items():
            passed = now - cron['last_run']

            if debug:
                print("Chronos.tick(%s) - Time Passed: %ds / %ds" % (name, passed, cron['period']))

            if  passed >= cron['period']:
                cron['handler'](now)
                cron['last_run'] = now

    @classmethod
    def now_str(cls):
        now = cls.CLOCK.datetime()
        return "%4d-%02d-%02d @ %02d:%02d:%02d" % (now[0], now[1], now[2], now[4], now[5], now[6])

    @classmethod
    def check(cls):
        print(cls.now_str())

    @classmethod
    def __convert_period_to_seconds(cls, value, units):
        seconds = None

        if units == 'D':
            seconds = value * 86400
        elif units == 'H':
            seconds = value * (60 * 60)
        elif units == 'M':
            seconds = value * 60

        return (seconds)







#
