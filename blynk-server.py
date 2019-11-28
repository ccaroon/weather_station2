#!/usr/bin/env python
import blynklib
import random

from lib.adafruit_io import AdafruitIO

# AIO
aio = AdafruitIO("weather-station")

# Blynk
BLYNK_AUTH = 'ePczqByz8YHSJJnYJDow8Dgb6K0TIAi-'
blynk = blynklib.Blynk(BLYNK_AUTH)

T_COLOR = '#f5b041'
H_COLOR = '#85c1e9'
ERR_COLOR = '#444444'

T_VPIN = 1
H_VPIN = 2

@blynk.handle_event('read V{}'.format(T_VPIN))
def read_handler(vpin):
    temperature = 0.0
    humidity = 0.0

    try:
        data = aio.get_data("temperature")
        if data['success']:
            temperature = int(data['results'][0]['value'])

        data = aio.get_data("humidity")
        if data['success']:
            humidity = int(data['results'][0]['value'])

        # change widget values and colors according read results
        if temperature != 0.0 and humidity != 0.0:
            color = "#0000FF"
            if temperature >= 90:
                color = "#ff0000"
            blynk.set_property(T_VPIN, 'color', color)

            color = "#FFFFFF"
            if humidity >= 85:
                color = "#00AAFF"
            blynk.set_property(H_VPIN, 'color', color)

            print(F"OK ... T[{temperature}] H[{humidity}]")

            blynk.virtual_write(T_VPIN, temperature)
            blynk.virtual_write(H_VPIN, humidity)
        else:
            print(F"NOK ... T[{temperature}] H[{humidity}]")
            # show widgets aka 'disabled' that mean we had errors during read sensor operation
            blynk.set_property(T_VPIN, 'color', ERR_COLOR)
            blynk.set_property(H_VPIN, 'color', ERR_COLOR)
    except Exception as e:
        print(e)


while True:
    blynk.run()






#
