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
info:
	@echo "install audok with: \"sudo make install all PREFIX=/usr APPDIR=/opt/audok\""


all: desktop


install:
	-mkdir -p $(BINDIR)
	-mkdir -p $(APPDIR)
	-mkdir -p $(SHAREAPPDIR)
	-mkdir -p $(SHAREICODIR)

	cp audok/*.png                                    ${APPDIR}
	cp audok/*.py                                     ${APPDIR}

	cp share/applications/com.github.kalibari.audok.desktop               ${SHAREAPPDIR}/com.github.kalibari.audok.desktop
	cp share/icons/hicolor/256x256/apps/com.github.kalibari.audok.png     ${SHAREICODIR}/com.github.kalibari.audok.png

	ln -s ${APPDIR}/audok.py $(BINDIR)/audok

	chmod 755 ${APPDIR}
	chmod 644 ${APPDIR}/*
	chmod 755 ${APPDIR}/audok.py
	chmod 644 ${SHAREICODIR}/com.github.kalibari.audok.png


desktop:
	gtk-update-icon-cache -f $(PREFIX)/share/icons/hicolor
	desktop-file-install ${SHAREAPPDIR}/com.github.kalibari.audok.desktop


uninstall:
	-rm -f ${SHAREAPPDIR}/com.github.kalibari.audok.desktop
	-rm -f ${SHAREICODIR}/com.github.kalibari.audok.png
	-rm -f ${BINDIR}/audok
	-rm -f ${APPDIR}/*
	-rmdir ${APPDIR}

