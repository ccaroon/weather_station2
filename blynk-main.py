#!/usr/bin/env python
import arrow
import blynklib
import random
from lib.secrets import SECRETS

from lib.adafruit_io import AdafruitIO

# AIO
aio = AdafruitIO("weather-station")

# Blynk
blynk = blynklib.Blynk(SECRETS['blynk_key'])

ERR_COLOR = '#444444'

T_VPIN = 1
H_VPIN = 3

def temp_to_color(temp):
    color = "#FFFFFF"

    if temp <= 25:
        color = "#ffffff"
    elif temp > 25 and temp <= 32:
        color = "#e4f0fb"
    elif temp > 32 and temp <= 55:
        color = "#047ffb"
    elif temp > 55 and temp <= 64:
        color = "#04fbe8"
    elif temp > 64 and temp <=75:
        color = "#33e108"
    elif temp > 75 and temp <= 85:
        color = "#f9f504"
    elif temp > 85 and temp <= 90:
        color = "#f97304"
    else:
        color = "#ff0000"

    return color

def humd_to_color(humd):
    color = "#FFFFFF"

    if humd <= 25:
        color = "#FFFFFF"
    elif humd > 25 and humd <= 50:
        color = "#9999BB"
    elif humd > 50 and humd <= 75:
        color = "#9999DD"
    else:
        color = "#9999FF"

    return color

def get_data(name):
    output = None

    data = aio.get_data(name, fields=['created_at'])
    if data['success']:
        output = data['results'][0]
        output['value'] = int(output['value'])
        output['created_at'] = arrow.get(output['created_at']).to("US/Eastern")

    return output

@blynk.handle_event('read V{}'.format(T_VPIN))
def read_handler(vpin):
    temperature = None
    humidity    = None

    try:
        temperature = get_data('temperature')
        temp_low = get_data('temperature-low')
        temp_high = get_data('temperature-high')
        humidity = get_data('humidity')

        # change widget values and colors according read results
        if temperature['value'] != 0.0 and humidity['value'] != 0.0:
            blynk.set_property(T_VPIN, 'color', temp_to_color(temperature['value']))
            blynk.set_property(H_VPIN, 'color', humd_to_color(humidity['value']))

            print(F"OK ... T[{temperature['value']}] H[{humidity['value']}]")

            blynk.virtual_write(T_VPIN, temperature['value'])
            blynk.virtual_write(T_VPIN+1, temperature['created_at'].format("MM-DD-YYYY hh:mma"))

            blynk.set_property(5, 'color', temp_to_color(temp_low['value']))
            blynk.virtual_write(5, temp_low['value'])
            blynk.virtual_write(7, temp_low['created_at'].format("MM-DD-YYYY hh:mma"))

            blynk.set_property(6, 'color', temp_to_color(temp_high['value']))
            blynk.virtual_write(6, temp_high['value'])
            blynk.virtual_write(8, temp_high['created_at'].format("MM-DD-YYYY hh:mma"))

            blynk.virtual_write(H_VPIN, humidity['value'])
            blynk.virtual_write(H_VPIN+1, humidity['created_at'].format("MM-DD-YYYY hh:mma"))
        else:
            print(F"NOK ... T[{temperature['value']}] H[{humidity['value']}]")
            # show widgets aka 'disabled' that mean we had errors during read sensor operation
            blynk.set_property(T_VPIN, 'color', ERR_COLOR)
            blynk.set_property(H_VPIN, 'color', ERR_COLOR)
    except Exception as e:
        print(F"Error: {e}")


while True:
    blynk.run()






#
