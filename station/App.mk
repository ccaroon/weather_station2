default:
	@echo "Include me in your app. :)"

%.pyc: %.py
	touch $@
	make upload-file FILE=$(CURDIR)/$<

../lib/%.pyc: ../lib/%.py
	touch $@
	make upload-file FILE=$(CURDIR)/$<

%.mpy: %.py
	mpy-cross $<
	make upload-file FILE=$(CURDIR)/$@

../lib/%.mpy: ../lib/%.py
	mpy-cross $<
	make upload-file FILE=$(CURDIR)/$@

install: $(BOOT) $(APP) $(LIBS) ../lib/secrets.py

boot: $(BOOT)

app: $(APP)

libs: lib/__init__.pyc $(LIBS)

.PHONY: install libs clean
