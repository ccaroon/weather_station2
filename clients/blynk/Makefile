default:
	@echo "Blynk Client for Weather Station #2"
	@echo "-----------------------------------"
	@echo "* install - Install the Blynk Client"
	@echo "* clean   - Clean up"

secrets:
	$(MAKE) -C ../../ secrets

install: secrets /etc/systemd/system/weather-station.service

/etc/systemd/system/weather-station.service: ./clients/blynk/conf/weather-station.service
	sudo cp ./clients/blynk/conf/weather-station.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable weather-station

clean:
	find . -name "*.pyc" -exec rm -rf {} +

.PHONY: install clean secrets
