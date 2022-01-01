import time

from lib.adafruit_io import AdafruitIO
from lib.chronos import Chronos
from lib.indicator import Indicator
from lib.logger import Log
from lib.weather_station import WeatherStation

# ------------------------------------------------------------------------------
IS_DEV = True
# ------------------------------------------------------------------------------
AIO          = None
BASE_NAME    = 'weather-station'
HAS_ERRORED  = False
INDICATE     = None
LOG          = None
MEASURE_FREQ = 1.00 * 60 # In Seconds
NAME         = "%s-dev" % (BASE_NAME) if IS_DEV else BASE_NAME
STATION      = None
# ------------------------------------------------------------------------------
def exit_error(name, msg):
    global HAS_ERRORED
    HAS_ERRORED = True

    if LOG:
        LOG.log("%s: '%s'" % (name, msg), stdout=True)
    else:
        print("%s: %s" % (name,msg))

    if INDICATE:
        INDICATE.blue(False)
        INDICATE.red(True)
# ------------------------------------------------------------------------------
try:
    INDICATE = Indicator()
    LOG = Log("%s.log" % (NAME))
    STATION = WeatherStation(NAME, logger=LOG, maintain_state=True, publish=True)
    AIO = AdafruitIO(STATION.name())
except Exception as e:
    exit_error("MAIN.GlobalsInit.Error", str(e))
# ------------------------------------------------------------------------------
def reset_high_low(timestamp):
    """Chronos Callback for resetting the daily low & hi temps"""
    msg = "Chronos: Resetting High/Low @ %s" % (timestamp)

    STATION.reset_high_low()

    LOG.log(msg)
    AIO.publish_data("notifications", msg, dry_run=False)
# ------------------------------------------------------------------------------
def main():
    """The App Entry Point"""

    try:
        last_run = list(time.localtime())
        for i in range(3,8):
            last_run[i] = 0

        Chronos.every("24h", "Reset High/Low", reset_high_low, last_run=last_run)

        LOG.log("NAME: [%s] | FREQ: [%.1fs] | HI/LOW RESET: %s" %
            (
                STATION.name(),
                MEASURE_FREQ,
                last_run[0:3]
            ),
            stdout=True
        )
    except Exception as e:
        exit_error("MAIN.Init.Error", str(e))

    while (not HAS_ERRORED):
        try:
            INDICATE.red(False)
            INDICATE.blue(False)

            INDICATE.blue(True)
            STATION.measure()
            INDICATE.blue(False)

            Chronos.tick(True)
            time.sleep(MEASURE_FREQ)
        except Exception as e:
            exit_error("MAIN.Loop.Error", str(e))
# ------------------------------------------------------------------------------
main()
if LOG:
    LOG.log('***** Exiting *****', stdout=True)
# ------------------------------------------------------------------------------
