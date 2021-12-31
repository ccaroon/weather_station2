default:
	@echo "Weather Station #2 -- Server"
	@echo "---------------------------"
	@echo "-- Debugging Commands -- "
	@echo "* get-log       - Retrieve and print Device Log File"
	@echo "* get-state     - Retrieve and print Device State File"
	@echo "* inspect       - get-log && get-state"
	@echo "* get-log-dev   - Retrieve and print Device DEV Log File"
	@echo "* get-state-dev - Retrieve and print Device DEV State File"
	@echo "* inspect-dev   - get-log-dev && get-state-dev"
	@echo "--Misc Commands--"
	@echo "* shell - Micropython REPL on Device"
	@echo "* clean - Clean Up"

include Ports.mk
include FileMgmt.mk

# NOTE: boot and main **must** be .py files ... not .mpy
BOOT = boot.pyc
APP  = main.pyc
LIBS = ../lib/adafruit_io.mpy ../lib/secrets.mpy lib/chronos.mpy lib/indicator.mpy lib/wifi.mpy lib/file_utils.mpy lib/sensor.mpy lib/weather_station.mpy

# Order matters - This include must come after above vars are set.
include App.mk

get-log:
	@make get-file FILE=weather-station.log

get-log-dev:
	@make get-file FILE=weather-station-dev.log

get-state:
	@make get-file FILE=weather-station.json

get-state-dev:
	@make get-file FILE=weather-station-dev.json

inspect: get-log get-state

inspect-dev: get-log-dev get-state-dev

shell:
	picocom $(PORT) -b115200

clean:
	find . -name "*.pyc" -exec rm -rf {} +
	find . -name "*.mpy" -exec rm -rf {} +
