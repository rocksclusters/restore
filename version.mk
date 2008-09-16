ROLLNAME	= $(shell uname -n)-restore
NAME		= roll-$(shell uname -n)-restore
VERSION		= $(shell date +%Y.%m.%d)
RELEASE		= 0
COLOR   	= orchid

REDHAT.ROOT 	= $(PWD)

CONTRIB_PKG_VER	= $(shell /opt/rocks/bin/rocks report version)
CONTRIB_PKG_DIR	= $(shell /opt/rocks/bin/rocks report distro)/contrib

#
# these are the files that will be restored when this roll is supplied
# during installation
#
FILES	+= /etc/X11/xorg.conf $(wildcard /var/named/*local)
FILES	+= $(wildcard /etc/ssh/*key*)
SCRIPTS	+=
