app-usage:
	@echo "Usage: 'include App.mk'"

install: boot.pyc main.pyc libs ../lib/secrets.py

boot.pyc: boot.py
	touch boot.pyc
	make upload-as-boot FILE=boot.py

main.pyc: main.py
	touch main.pyc
	make upload-as-main FILE=main.py

../lib/secrets.py: ../.secrets
	../bin/gen_secrets.py

libs: lib/__init__.pyc $(LIBS)

lib/__init__.pyc: lib/__init__.py
	touch $@
	ampy --port $(PORT) mkdir lib
	make upload-file FILE=lib/__init__.py DEST=lib

# These rule assume files det uploaded to the `lib` directory
%.pyc: %.py
	touch $@
	make upload-file FILE=$(CURDIR)/$< DEST=lib

%.mpy: %.py
	mpy-cross $<
	make upload-file FILE=$(CURDIR)/$@ DEST=lib

.PHONY: default install boot app libs
