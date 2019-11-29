noop:
	@echo "Weather Station 2"

all: lib/secrets.py

lib/secrets.py: .secrets
	./bin/gen_secrets.py

clean:
	find . -name "*.pyc" -exec rm -rf {} +
	find . -name "*.mpy" -exec rm -rf {} +

.PHONY: noop clean
