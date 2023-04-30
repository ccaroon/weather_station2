import time

from lib.adafruit_io import AdafruitIO
from lib.chronos import Chronos
from lib.weather_station import WeatherStation
from lib.wifi import MyWifi
# ------------------------------------------------------------------------------
IS_DEV = False
# ------------------------------------------------------------------------------
AIO          = None
BASE_NAME    = 'weather-station'
HAS_ERRORED  = False
MEASURE_FREQ = 4.50 * 60 # In Seconds
NAME         = "%s-dev" % (BASE_NAME) if IS_DEV else BASE_NAME
STATION      = None
# ------------------------------------------------------------------------------
def print_error(name, err):
    print("%s: (%s) --> '%s'" % (name, type(err), str(err)))
# ------------------------------------------------------------------------------
def recover_error(err):
    recovered = False

    if 'CONN_LOST' in str(err) or 'ECONNABORTED' in str(err):
        if MyWifi.reconnect():
            recovered = True
            print("Successfully reconnected to WiFi!")

    return recovered
# ------------------------------------------------------------------------------
def handle_error(name, err):
    global HAS_ERRORED

    print_error(name, err)

    if not recover_error(err):
        HAS_ERRORED = True
# ------------------------------------------------------------------------------
try:
    STATION = WeatherStation(NAME, logger=None, maintain_state=True, publish=True)
    AIO = AdafruitIO(STATION.name())
except Exception as err:
    handle_error("MAIN.GlobalsInit.Error", err)
# ------------------------------------------------------------------------------
def reset_high_low(timestamp):
    """Chronos Callback for resetting the daily low & hi temps"""
    msg = "Chronos: Resetting High/Low @ %s" % (timestamp)

    STATION.reset_high_low()
    AIO.publish_data("notifications", msg, dry_run=False)
# ------------------------------------------------------------------------------
def main():
    """The App Entry Point"""

    try:
        last_run = list(time.localtime())
        for i in range(3,8):
            last_run[i] = 0

        Chronos.every("24h", "Reset High/Low", reset_high_low, last_run=last_run)

        print("NAME: [%s] | FREQ: [%.1fs] | HI/LOW RESET: %s" %
            (
                STATION.name(),
                MEASURE_FREQ,
                last_run[0:3]
            )
        )
    except Exception as err:
        handle_error("MAIN.Init.Error", err)

    while (not HAS_ERRORED):
        try:
            STATION.measure()

            Chronos.tick(True)
            time.sleep(MEASURE_FREQ)
        except Exception as err:
            # TODO: log exception to file before exiting
            handle_error("MAIN.Loop.Error", err)
# ------------------------------------------------------------------------------
main()
# ------------------------------------------------------------------------------
