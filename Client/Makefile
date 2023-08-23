EXECUTABLE = pyside2-uic
GUIDIR = gui/ui

VERSION = 0.0.1
UIC  = $(shell which $(EXECUTABLE))
SED = $(shell which sed)

.PHONY: all clean setup

all:
	$(UIC) $(GUIDIR)/mainwindow.ui > $(GUIDIR)/ui_mainwindow.py
clean:
	$(RM) $(GUIDIR)/ui_mainwindow.py
