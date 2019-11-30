import ujson
import os

from lib.adafruit_io import AdafruitIO
from lib.sensor import Sensor

class WeatherStation:

    def __init__(self, name, **kwargs):
        self.__name = name

        self.__aio     = AdafruitIO(name)
        self.__sensor  = Sensor(14)

        self.__publish = kwargs.get("publish", True)
        self.__maintain_state = kwargs.get("maintain_state", False)

        self.reset_high_low()
        self.__load_state()

    def name(self):
        return self.__name

    def enable_publish(self, enable):
        self.__publish = enable

    def measure(self):
        data = self.__sensor.get_temp_and_humidity()

        tempF = round(data['tempF'])
        humidity = round(data['humidity'])

        self.__update_high_temp(tempF)
        self.__update_low_temp(tempF)

        responses = []

        temp_resp = self.__aio.publish_data("temperature", tempF, dry_run=not self.__publish)
        responses.append(temp_resp)

        humd_resp = self.__aio.publish_data("humidity", humidity, dry_run=not self.__publish)
        responses.append(humd_resp)

        for resp in responses:
            self.__aio.handle_response(resp)

        self.__save_state()

    def reset_high_low(self):
        self.__temp_high = -999
        self.__temp_low  = 999

    def __save_state(self):
        if self.__maintain_state:
            state = {
                "publish": self.__publish,
                "temp_high": self.__temp_high,
                "temp_low": self.__temp_low
            }
            try:
                with open("%s.json" % self.__name, "w") as file:
                    ujson.dump(state, file)
            except Exception as e:
                print(str(e))

    def __load_state(self):
        if self.__maintain_state:
            filename = "%s.json" % self.__name
            try:
                os.stat(filename)
                with open(filename, "r") as file:
                    state = ujson.load(file)

                self.__publish = state['publish']
                self.__temp_high = state['temp_high']
                self.__temp_low = state['temp_low']
            except Exception as e:
                print(str(e))

    def __update_high_temp(self, tempF):
        if tempF > self.__temp_high:
            self.__temp_high = tempF
            resp = self.__aio.publish_data("temperature-high", tempF, dry_run=not self.__publish)
            self.__aio.handle_response(resp)

    def __update_low_temp(self, tempF):
        if tempF < self.__temp_low:
            self.__temp_low = tempF
            resp = self.__aio.publish_data("temperature-low", tempF, dry_run=not self.__publish)
            self.__aio.handle_response(resp)
