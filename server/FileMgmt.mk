filemgmt-usage:
	@echo "Usage: 'include FileMgmt.mk'"

upload-as-main:
ifneq ($(FILE),)
	ampy --port $(PORT) put $(FILE) main.py
else
	echo "ERROR: Must Specify a filename with FILE=filename"
endif

upload-as-boot:
ifneq ($(FILE),)
	ampy --port $(PORT) put $(FILE) boot.py
else
	echo "ERROR: Must Specify a filename with FILE=filename"
endif

upload-file:
ifneq ($(FILE),)
	ampy --port $(PORT) put $(FILE) $(DEST)/$(shell basename $(FILE))
else
	echo "ERROR: Must Specify a filename with FILE=filename"
endif

list-files:
	ampy --port $(PORT) ls

get-file:
ifneq ($(FILE),)
	ampy --port $(PORT) get $(FILE) > /tmp/$(FILE)
	@echo "+-------------------------------------------------------------------+"
	@cat /tmp/$(FILE)
	@echo "+-------------------------------------------------------------------+"
else
	echo "ERROR: Must Specify a filename with FILE=filename"
endif

rm-file:
ifneq ($(FILE),)
	ampy --port $(PORT) rm $(FILE)
else
	echo "ERROR: Must Specify a filename with FILE=filename"
endif
