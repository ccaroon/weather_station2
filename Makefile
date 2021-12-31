default:
	@echo "Weather Station #2"
	@echo "-----------------------------------"
	@echo "* secrets - Generate Secrets Class"
	@echo "--See Also--"
	@echo "* server/Makefile"
	@echo "* clients/blynk/Makefile"

# SHARED tasks
secrets: lib/secrets.py

lib/secrets.py: .secrets
	./bin/gen_secrets.py

clean:
	rm ./lib/secrets.py

.PHONY: clean secrets
