default:
	@echo "Weather Station #2"

all: lib/secrets.py

lib/secrets.py: .secrets
	./bin/gen_secrets.py

service: /etc/systemd/system/blynk-ws.service

/etc/systemd/system/blynk-ws.service: ./conf/blynk-ws.service
	sudo cp ./conf/blynk-ws.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable blynk-ws

clean:
	find . -name "*.pyc" -exec rm -rf {} +
	find . -name "*.mpy" -exec rm -rf {} +

.PHONY: default all clean
