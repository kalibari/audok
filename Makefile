###############################################################################
#
# Installation DIRECTORIES
#
# 
# make PREFIX=/app DESTDIR=/app


PREFIX        = /usr
BINDIR	      = $(PREFIX)/bin
DESTDIR	      = /opt
SHAREAPPDIR   = $(PREFIX)/share/applications
SHAREICODIR   = $(PREFIX)/share/icons/hicolor/256x256/apps

ICON         := $(shell echo $(SHAREICODIR) | sed -r 's/\//\\\//g')
EXEC         := $(shell echo $(BINDIR) | sed -r 's/\//\\\//g')

###############################################################################
#
# TARGETS
#

install:
	-mkdir -p $(BINDIR)
	-mkdir -p $(DESTDIR)
	-mkdir -p $(SHAREAPPDIR)
	-mkdir -p $(SHAREICODIR)

	install -m 644 audok/*.png                                    ${DESTDIR}/audok
	install -m 644 audok/*.py                                     ${DESTDIR}/audok

	install -m 644 share/applications/audok.desktop               ${SHAREAPPDIR}/audok.desktop
	install -m 644 share/icons/hicolor/256x256/apps/audok.png     ${SHAREICODIR}/audok.png
	install -m 755 bin/audok                                      ${BINDIR}/audok

	chmod 755 ${DESTDIR}/audok/audok

	sed -i "s/^Icon=.*/Icon=$(ICON)\/audok.png/g" ${SHAREAPPDIR}/audok.desktop
	sed -i "s/^Exec=.*/Exec=$(EXEC)\/audok.py %u/g" ${SHAREAPPDIR}/audok.desktop
	sed -i "s/^TryExec=.*/TryExec=$(EXEC)\/audok.py/g" ${SHAREAPPDIR}/audok.desktop


uninstall:
	-rm -f ${SHAREAPPDIR}/audok.desktop
	-rm -f ${BINDIR}/audok.desktop



###############################################################################
#
# UTILITIES
#

clean:
	#-rm -f `find . -name "*.o"` ../bin/* ../plugins/*
	#-rm -f `find .. -name "*~"`
	#-rm -f *.bak core score.srt
	#-rm -f *.bb *.bbg *.da *-ann gmon.out bb.out
	#-rm -f `find .. -name "*.class"`

backup:		clean
	(cd ../../;							\
	tar czf `date '+../backup/ladspa_sdk.%Y%m%d%H%M.tgz'` ladspa_sdk/)

###############################################################################

