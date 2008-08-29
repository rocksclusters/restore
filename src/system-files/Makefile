#
# $Id: Makefile,v 1.2 2008/08/29 19:39:20 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.2  2008/08/29 19:39:20  mjk
# use new dev env
#
# Revision 1.1  2006/07/25 16:32:15  bruno
# retooled the restore roll to make a separation between system files and
# user files.
# user files need to be installed in the post section (to ensure that a
# package doesn't overwrite the user file) and system files need to be available
# as early as the pre section.
#
#

REDHAT.ROOT     = $(PWD)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

-include $(ROCKSROOT)/etc/python.mk
include python.mk

-include *-restore.mk

build:


install::
	for file in $(FILES) ; do \
		mkdir -p $(ROOT)/upgrade/`dirname $$file` ; \
		cp $$file $(ROOT)/upgrade/$$file ; \
	done
		

clean::
	rm -f $(NAME).spec.in

