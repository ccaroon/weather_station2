include Ports.mk
include FileMgmt.mk

noop:
	@echo "Weather Station"

# NOTE: boot and main **must** be .py files ... not .mpy
BOOT = boot.pyc
APP  = main.pyc
LIBS = ../lib/adafruit_io.mpy lib/chronos.mpy lib/indicator.mpy lib/wifi.mpy lib/file_utils.mpy lib/sensor.mpy lib/weather_station.mpy

include App.mk

get-log:
	@make get-file FILE=weather-station.log
	@echo "-------------------------------------------------"
	@cat /tmp/weather-station.log
	@echo "-------------------------------------------------"

get-log-dev:
	@make get-file FILE=weather-station-dev.log
	@echo "-------------------------------------------------"
	@cat /tmp/weather-station-dev.log
	@echo "-------------------------------------------------"

get-state:
	@make get-file FILE=weather-station.json
	@echo "-------------------------------------------------"
	@cat /tmp/weather-station.json
	@echo "-------------------------------------------------"

get-state-dev:
	@make get-file FILE=weather-station-dev.json
	@echo "-------------------------------------------------"
	@cat /tmp/weather-station-dev.json
	@echo "-------------------------------------------------"

inspect: get-log get-state

inspect-dev: get-log-dev get-state-dev

lib/__init__.pyc: lib/__init__.py
	touch $@
	ampy --port $(PORT) mkdir lib
	make upload-file FILE=lib/__init__.py

../lib/secrets.py: lib/__init__.pyc ../.secrets
	../bin/gen_secrets.py
	mpy-cross ../lib/secrets.py
	make upload-file FILE=../lib/secrets.mpy

shell:
	picocom $(PORT) -b115200

clean:
	find . -name "*.pyc" -exec rm -rf {} +
	find . -name "*.mpy" -exec rm -rf {} +
