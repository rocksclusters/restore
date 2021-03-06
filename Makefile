#
# $Id: Makefile,v 1.23 2012/11/27 00:49:12 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.23  2012/11/27 00:49:12  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.22  2012/05/06 05:49:19  phil
# Copyright Storm for Mamba
#
# Revision 1.21  2011/07/23 02:31:16  phil
# Viper Copyright
#
# Revision 1.20  2010/09/07 23:53:24  bruno
# star power for gb
#
# Revision 1.19  2009/06/16 22:26:42  bruno
# ensure the user must manually partition a node when using the restore roll
#
# Revision 1.18  2009/05/01 19:07:21  mjk
# chimi con queso
#
# Revision 1.17  2009/03/03 23:06:18  mjk
# switch to rocks report host attr
#
# Revision 1.16  2008/10/18 00:56:13  mjk
# copyright 5.1
#
# Revision 1.15  2008/09/16 19:39:48  bruno
# - make a 'restore-contrib' package that contains all the RPMS from
#   /export/rocks/install/contrib
#
# - save the /var/named/*local files
#
# - save the node's ssh machine keys
#
# Revision 1.14  2008/08/29 19:39:20  mjk
# use new dev env
#
# Revision 1.13  2008/03/06 23:41:56  mjk
# copyright storm on
#
# Revision 1.12  2007/07/02 23:01:07  bruno
# get site.xml from the rocks command line
#
# Revision 1.11  2007/06/23 04:03:59  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:50:11  mjk
# monkey face copyright
#
# Revision 1.9  2006/09/06 21:18:33  bruno
# put site.xml back, but this time without the passwords
#
# Revision 1.8  2006/09/06 18:41:40  bruno
# for all user files, uuencode them for inclusion into their respective XML
# node files, then put in code to uudecode them.
#
# this solves the parsing error that occurs if a 'bad' character is in a
# user-specified file (for example, a control-L character of if the user
# specifies a binary file).
#
# Revision 1.7  2006/08/10 00:11:53  mjk
# 4.2 copyright
#
# Revision 1.6  2006/07/27 18:16:11  bruno
# retooled the user file part of the restore roll to be able to accept
# user post scripts
#
# Revision 1.5  2006/07/25 16:32:13  bruno
# retooled the restore roll to make a separation between system files and
# user files.
# user files need to be installed in the post section (to ensure that a
# package doesn't overwrite the user file) and system files need to be available
# as early as the pre section.
#
# Revision 1.4  2006/07/06 18:15:40  bruno
# include the local site.xml in the nodes directory
#
# Revision 1.3  2006/06/23 18:44:54  bruno
# touch ups
#
# Revision 1.2  2005/12/14 22:08:14  bruno
# new
#
# Revision 1.1  2005/12/14 21:54:01  bruno
# new
#
#
#

-include $(ROLLSROOT)/etc/Rolls.mk
include Rolls.mk

-include *-restore.mk


default: roll

pretar::
	./bin/backup-db.py > nodes/restore-node.xml
	./bin/build-user-files-node.py \
		--files="$(FILES)" --scripts="$(SCRIPTS)" \
			> nodes/restore-user-files.xml
	/opt/rocks/bin/rocks report host attr localhost | \
		grep -v Password | grep -v Server_Partitioning \
		> nodes/site.attrs
	echo "Server_Partitioning:manual" >> nodes/site.attrs
	(cd RPMS/$(ARCH) ; \
		/opt/rocks/bin/rocks create package $(CONTRIB_PKG_DIR) \
			restore-contrib version=$(CONTRIB_PKG_VER) ; \
	)
roll::
	ln -s $(ROLLNAME)*.iso restore.iso

clean::
	rm -f restore.iso
	rm -f $(ROLLNAME)*.iso
	rm -f timestamp
	rm -f *spec.mk
	rm -f nodes/restore-node.xml
	rm -f nodes/restore-user-files.xml
	rm -f nodes/site.attrs
	rm -f _os _arch

