ROLLNAME	= $(shell uname -n)-restore
NAME		= roll-$(shell uname -n)-restore
VERSION		= $(shell date +%Y.%m.%d)
RELEASE		= 0
COLOR   	= orchid

REDHAT.ROOT 	= $(PWD)

#
# these are the files that will be restored when this roll is supplied
# during installation
#
FILES	+= /etc/X11/xorg.conf
SCRIPTS	+=
