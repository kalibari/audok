###############################################################################
#
# Installation DIRECTORIES
#

PREFIX        = /usr
BINDIR	      = $(PREFIX)/bin
APPDIR	      = /opt/audok
SHAREAPPDIR   = $(PREFIX)/share/applications
SHAREICODIR   = $(PREFIX)/share/icons/hicolor/256x256/apps

ICON         := $(shell echo $(SHAREICODIR) | sed -r 's/\//\\\//g')
EXEC         := $(shell echo $(BINDIR) | sed -r 's/\//\\\//g')

###############################################################################
#
# TARGETS
#  
all:
	@echo "run \"make install PREFIX=/usr APPDIR=/opt/audok\" to install audok"

install:
	-mkdir -p $(BINDIR)
	-mkdir -p $(APPDIR)
	-mkdir -p $(SHAREAPPDIR)
	-mkdir -p $(SHAREICODIR)

	cp audok/*.png                                    ${APPDIR}
	cp audok/*.py                                     ${APPDIR}

	cp share/applications/audok.desktop               ${SHAREAPPDIR}/audok.desktop
	cp share/icons/hicolor/256x256/apps/audok.png     ${SHAREICODIR}/audok.png

	ln -s ${APPDIR}/audok.py $(BINDIR)/audok

	sed -i "s/^Icon=.*/Icon=$(ICON)\/audok.png/g" ${SHAREAPPDIR}/audok.desktop
	sed -i "s/^Exec=.*/Exec=$(EXEC)\/audok %u/g" ${SHAREAPPDIR}/audok.desktop
	sed -i "s/^TryExec=.*/TryExec=$(EXEC)\/audok/g" ${SHAREAPPDIR}/audok.desktop

	chmod 755 ${APPDIR}
	chmod 644 ${APPDIR}/*
	chmod 755 ${APPDIR}/audok.py
	chmod 644 ${SHAREICODIR}/audok.png

	desktop-file-install ${SHAREAPPDIR}/audok.desktop




uninstall:
	-rm -f ${SHAREAPPDIR}/audok.desktop
	-rm -f ${SHAREICODIR}/audok.png
	-rm -f ${BINDIR}/audok
	-rm -f ${APPDIR}/*
	-rmdir ${APPDIR}

