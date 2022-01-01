default:
	@echo "Weather Station #2"
	@echo "-----------------------------------"
	@echo "* secrets - Generate Secrets Class"
	@echo "* clean   - Clean up"
	@echo
	@echo "-- See Also --"
	@echo "* server/Makefile"
	@echo "* clients/blynk/Makefile"

# SHARED tasks
secrets: lib/secrets.py

lib/secrets.py: .secrets
	./bin/gen_secrets.py

clean:
	rm -f ./lib/secrets.py
	find . -name "*.pyc" -exec rm -rf {} +
	find . -name "*.mpy" -exec rm -rf {} +

.PHONY: clean secrets
