import time

from adafruit_io import AdafruitIO
from chronos import Chronos
from indicator import Indicator
from weather_station import WeatherStation

# ------------------------------------------------------------------------------
station = WeatherStation('weather-station-dev', maintain_state=True, publish=True)
aio = AdafruitIO(station.name())
# ------------------------------------------------------------------------------
def reset_high_low():
    station.reset_high_low()
    aio.publish_data("notifications",
        "Chronos: Resetting High/Low",
        dry_run=False
    )

# ------------------------------------------------------------------------------
def main():
    MEASURE_FREQ = 1.00 * 60 # In Seconds

    indicate = Indicator()

    last_run = list(time.localtime())
    for i in range(3,8):
        last_run[i] = 0

    Chronos.every("24h", "Reset High/Low", reset_high_low, last_run=last_run)

    while (True):
        try:
            indicate.red(False)
            indicate.blue(False)

            indicate.blue(True)
            station.measure()
            indicate.blue(False)
        except Exception as e:
            indicate.blue(False)
            indicate.red(True)
            print(str(e))
        finally:
            Chronos.tick(True)
            time.sleep(MEASURE_FREQ)
# ------------------------------------------------------------------------------
main()
# ------------------------------------------------------------------------------
