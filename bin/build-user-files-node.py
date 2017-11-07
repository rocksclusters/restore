#!/opt/rocks/bin/python
#
# $Id: build-user-files-node.py,v 1.21 2012/11/27 00:49:12 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# $Log: build-user-files-node.py,v $
# Revision 1.21  2012/11/27 00:49:12  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.20  2012/05/06 05:49:19  phil
# Copyright Storm for Mamba
#
# Revision 1.19  2011/07/23 02:31:16  phil
# Viper Copyright
#
# Revision 1.18  2010/09/07 23:53:24  bruno
# star power for gb
#
# Revision 1.17  2009/05/01 19:07:21  mjk
# chimi con queso
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
# Revision 1.14  2008/03/06 23:41:56  mjk
# copyright storm on
#
# Revision 1.13  2007/06/23 04:03:59  mjk
# mars hill copyright
#
# Revision 1.12  2006/09/15 02:38:22  mjk
# removed ROCK_ROOT variable, #80 (trac.rocksclusters.org)
#
# Revision 1.11  2006/09/14 18:49:48  bruno
# need to set a variable to insert-ethers so all the plugins will be
# correctly run.
#
# Revision 1.10  2006/09/13 22:23:03  bruno
# delete the uuencoded file when done
#
# Revision 1.9  2006/09/12 20:36:44  bruno
# in the last post section of the last XML node of the restore roll, call
# insert-ethers to refresh all the configuration files under rocks control.
#
# this ensures that any changes made to the database by the user scripts
# will be reflected on the node's first boot.
#
# Revision 1.8  2006/09/11 22:50:11  mjk
# monkey face copyright
#
# Revision 1.7  2006/09/06 18:55:55  bruno
# remove full pathname to uuencode and uudecode. this will make it easier
# to call them in either the 'pre' or 'post' section by manipuating the PATH
# variable.
#
# Revision 1.6  2006/09/06 18:47:38  bruno
# tweak
#
# Revision 1.5  2006/09/06 18:41:41  bruno
# for all user files, uuencode them for inclusion into their respective XML
# node files, then put in code to uudecode them.
#
# this solves the parsing error that occurs if a 'bad' character is in a
# user-specified file (for example, a control-L character of if the user
# specifies a binary file).
#
# Revision 1.4  2006/08/10 00:11:53  mjk
# 4.2 copyright
#
# Revision 1.3  2006/07/27 23:13:26  anoop
# Build user files is now a little more flexible. It can handle different
# types of scripts and also a nochroot environment.
#
# Revision 1.2  2006/07/27 18:16:13  bruno
# retooled the user file part of the restore roll to be able to accept
# user post scripts
#
# Revision 1.1  2006/07/25 16:32:14  bruno
# retooled the restore roll to make a separation between system files and
# user files.
# user files need to be installed in the post section (to ensure that a
# package doesn't overwrite the user file) and system files need to be available
# as early as the pre section.
#
#
#
import xml.sax.saxutils
import os
import sys
import stat
import string
import rocks.app
import time


class App(rocks.app.Application):
	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)

		self.files = []
		self.scripts = []

		self.getopt.l.extend([
			('files=', ''),
			('scripts=', '')
                        ])
		

		return


	def parseArg(self, c):
		if rocks.app.Application.parseArg(self, c):
			return 1
		elif c[0] == '--files':
			self.files = string.split(c[1])
		elif c[0] == '--scripts':
			self.scripts = string.split(c[1])
		else:
			return 0

		return 1


	def writeHeader(self):
		print '<?xml version="1.0" standalone="no"?>'
		print '<kickstart>'
		print '<description>'
		print '</description>'
		print '<changelog>'
		print '</changelog>'
		return


	def writeFooter(self):
		print '</kickstart>'
		return


	def writeFile(self, filename):
		if os.path.isdir(filename):
			return

		#
		# get file metadata
		#
		try:
			filestat = os.stat(filename)
		except:
			return
		perms = filestat[stat.ST_MODE]
		userid = '%s' % (filestat[stat.ST_UID])
		groupid = '%s' % (filestat[stat.ST_GID])
		mtime = filestat[stat.ST_MTIME]

		str = '<file name="%s.uuencode" ' % (filename)
		str += 'perms="%o" ' % (int(stat.S_IMODE(perms)))
		str += 'owner="%s.%s"' % (userid, groupid)
		str += '>'
		print str
		
		#
		# uuencode the file
		#
		cmd = 'uuencode --base64 %s /dev/stdout' % (filename)
		for line in os.popen(cmd).readlines():
			print "%s" % (line[:-1])

		print '</file>'

		#
		# now uudecode the file
		#
		str = '<file name="%s" ' % (filename)
		str += 'perms="%o" ' % (int(stat.S_IMODE(perms)))
		str += 'owner="%s.%s" ' % (userid, groupid)
		str += 'expr="uudecode -o %s %s.uuencode" ' \
			% (filename, filename)
		str += '/>'
		print str

		#
		# set the original modification time
		#
		mtimestr = time.strftime('%Y%m%d%H%M.%S', time.localtime(mtime))
		print 'touch -t %s %s' % (mtimestr, filename)

		#
		# delete the uuencoded file
		#
		print 'rm -f %s.uuencode' % (filename)

		return


	def writeScript(self, filename):
		if os.path.isdir(filename):
			return
		
		try:
			file = open(filename, 'r')
		except:
			return

		line = file.readline()
		if line.startswith("#!"):
			interpreter = line.lstrip("#!")
			interpreter = interpreter.strip()
			line = file.readline()
		else:
			interpreter = self.getSuffix(filename)
		arg = ""
		if interpreter != "":
			arg += "--interpreter %s" % (interpreter)
		while (line):
			if line.strip() == "":
				line = file.readline()
				continue
			elif (line.startswith("#") and line.find("nochroot") != -1):
				arg += " --nochroot"
				break
			else:
				break
			
		if arg != "":
			print "<post arg=\"%s\">" % (arg)
		else:
			print "<post>"

		while line:
			l = xml.sax.saxutils.escape(line)
			print l[:-1]
			line = file.readline()

		file.close()
		print "</post>"

		return


	def getSuffix(self,filename):
		suffix_dict = {'py':'/opt/rocks/bin/python','csh':'/bin/tcsh','pl':'/usr/bin/perl'}
		suffix = filename.split('.')[-1]
		try:
			interpreter = suffix_dict[suffix]
		except KeyError:
			interpreter = ""

		return interpreter
		
	def run(self):
		self.writeHeader()
		# Write a single post section for all the 
		# files that need to be created. Populate 
		# all the files in.
		print '<post>'
		for file in self.files:
			self.writeFile(file)
			print ''
		print '</post>'
		print ''
		
		# Fill up the rest of the xml file with the 
		# remaining post section scripts
		for script in self.scripts:
			self.writeScript(script)
			print ''

		#
		# and finally, refresh all the configuration files under
		# rocks control
		#
		print '<post>'
		print '/opt/rocks/bin/rocks sync config'
		print '</post>'
		print ''

		self.writeFooter()


app = App(sys.argv)             
app.parseArgs()                 
app.run()

