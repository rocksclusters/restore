#!/opt/rocks/bin/python
#
# $Id: backup-db.py,v 1.19 2008/03/06 23:41:56 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# $Log: backup-db.py,v $
# Revision 1.19  2008/03/06 23:41:56  mjk
# copyright storm on
#
# Revision 1.18  2007/06/23 04:03:59  mjk
# mars hill copyright
#
# Revision 1.17  2007/06/12 19:52:05  bruno
# use the rocks command line to help build the restore roll
#
# Revision 1.16  2006/09/13 22:23:03  bruno
# delete the uuencoded file when done
#
# Revision 1.15  2006/09/11 22:50:11  mjk
# monkey face copyright
#
# Revision 1.14  2006/09/07 00:51:49  bruno
# don't embed site.xml, make an XML file and copy it into /tmp inside the
# CGI that calls 'screengen'
#
# Revision 1.13  2006/09/06 18:55:55  bruno
# remove full pathname to uuencode and uudecode. this will make it easier
# to call them in either the 'pre' or 'post' section by manipuating the PATH
# variable.
#
# Revision 1.12  2006/09/06 18:41:41  bruno
# for all user files, uuencode them for inclusion into their respective XML
# node files, then put in code to uudecode them.
#
# this solves the parsing error that occurs if a 'bad' character is in a
# user-specified file (for example, a control-L character of if the user
# specifies a binary file).
#
# Revision 1.11  2006/08/11 20:09:07  bruno
# tweak for rocks 4.1 frontends
#
# Revision 1.10  2006/08/10 00:11:53  mjk
# 4.2 copyright
#
# Revision 1.9  2006/07/10 20:05:39  bruno
# get all the files under /export/home/install/site-profiles (all but
# skeleton.xml)
#
# Revision 1.8  2006/07/06 23:39:46  bruno
# touch ups
#
# Revision 1.7  2006/07/03 23:25:00  bruno
# check is the file is a directory before trying to read it.
#
# Revision 1.6  2006/07/03 20:56:33  bruno
# closer with the restore roll
#
# Revision 1.5  2006/01/16 06:49:13  mjk
# fix python path for source built foundation python
#
# Revision 1.4  2005/12/17 17:26:47  bruno
# get the ssh keys permissions correct
#
# Revision 1.3  2005/12/15 05:53:39  bruno
# better
#
# Revision 1.2  2005/12/14 22:49:42  bruno
# make sure the user-specific files are put back on the disk under /upgrade
#
# Revision 1.1  2005/12/13 23:13:18  bruno
# closer
#
#
import xml.sax.saxutils
import os
import rocks.file

def writeFile(input_filename, output_filename, perms='', owner=''):
	if os.path.isdir(input_filename):
		return

	str = '<file name="%s.uuencode" ' % (output_filename)
	if perms != '':
		str += 'perms="%s" ' % (perms)
	if owner != '':
		str += 'owner="%s" ' % (owner)
	str += '>'
	print str
	
	#
	# uuencode the file
	#
	cmd = 'uuencode --base64 %s /dev/stdout' % (input_filename)
	for line in os.popen(cmd).readlines():
		print "%s" % (line[:-1])

	print '</file>'

	#
	# now uudecode the file
	#
	str = '<file name="%s" ' % (output_filename)
	if perms != '':
		str += 'perms="%s" ' % (perms)
	if owner != '':
		str += 'owner="%s" ' % (owner)
	str += 'expr="uudecode -o %s %s.uuencode" ' \
		% (output_filename, output_filename)
	str += '/>'
	print str

	#
	# delete the uuencoded file
	#
	print 'rm -f %s.uuencode' % (output_filename)

	return


def getSiteProfiles():
	#
	# get all the files under site-profiles
	#
	print '<post>'
	tree = rocks.file.Tree('/export/home/install/site-profiles/')

	for dir in tree.getDirs():
		for file in tree.getFiles(dir):
			#
			# don't get skeleton.xml
			#
			if file.getName() == 'skeleton.xml':
				continue

			writeFile(file.getFullName(), file.getFullName(),
				'0400', 'root.apache')

	print '</post>'
	return
	

print '<?xml version="1.0" standalone="no"?>'
print '<kickstart>'

print '<description>'
print '</description>'

print '<changelog>'
print '</changelog>'

print '<pre>'
#
# the path to uudecode. this is only needed in the pre section, because
# in the post section, uudecode will have already been installed on the hard
# disk and the path to uudecode will be set correctly.
#
print 'PATH=$PATH:/tmp/updates/usr/bin'
writeFile('/etc/fstab', '/upgrade/etc/fstab', '0644')
print '</pre>\n'

print '<post>'

for line in os.popen('/opt/rocks/bin/rocks dump').readlines():
	print "%s" % (line[:-1])

print '\n'

for file in os.listdir('/root/.ssh'):
	filename = '/root/.ssh/' + file
	writeFile(filename, filename, '0400')

print 'chmod a+r /root/.ssh/*pub'

print '</post>'

getSiteProfiles()

print '</kickstart>'

