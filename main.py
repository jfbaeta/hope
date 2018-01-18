#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from models.Formatter import Formatter
from models.Lun import Lun
from models.PhysicalVolume import PhysicalVolume
from models.VolumeGroup import VolumeGroup
from models.LogicalVolume import LogicalVolume
from models.FileSystem import FileSystem
from string import Template
import re
import optparse
import os
import subprocess

parser = optparse.OptionParser()

parser.add_option('-c', '--create',         '--cr',             help='Creates')
parser.add_option('-l', '--list',           '--ls',             help='List')
parser.add_option('-r', '--remove',         '--rm',             help='Remove')
parser.add_option('-v', '--version',                            help='Version')
#parser.add_option('-h', '--help',                               help='Help')
parser.add_option('-m', '--menu',                               help='Menu')
parser.add_option('-S', '--sanvolume',      '--svol',   '--sv', help='SAN Volume')
parser.add_option('-P', '--physicalvolume', '--pvol',   '--pv', help='Physical Volume')
parser.add_option('-V', '--volumegroup',    '--volgrp', '--vg', help='Volume Group')
parser.add_option('-L', '--logicalvolume',  '--lvol',   '--lv', help='Logical Volume')
parser.add_option('-F', '--filesystem',     '--fs',             help='File System')
parser.add_option('-U', '--usrsap',         '--sap',            help='/usr/sap')
parser.add_option('-D', '--hanadata',       '--data',           help='/hana/data')
parser.add_option('-G', '--hanalog',        '--log',            help='/hana/log')
parser.add_option('-H', '--hanashared',     '--shared',         help='/hana/shared')
parser.add_option('-a', '--all',                                help='All')

(opts, args) = parser.parse_args()

def menu():

	option = True
	
	while option:
		print '(1) Detect Storage Volumes'
		print '(2) Detect Physical Volumes'
		print '(3) Detect Volume Groups'
		print '(4) Detect Logical Volumes'
		print '(5) Detect File Systems'
		print '(6) Create /etc/multipath.conf File'
		print '(7) Reload Multipath to Change Volume Names'
		print '(8) Create Physical Volumes'
		print '(9) Create Volume Groups'
		print '(10) Create Logical Volumes'
		print '(11) Create File Systems'
		print '(666) RESET MULTPATHS!'
		print '(Q,q,E,e,X,x) Quit/Exit'
		print 'Choose your Option:',
		option = raw_input()

		if (option == '1'):
			Lun().show()
		elif (option == '2'):
			PhysicalVolume().show()
		elif (option == '3'):
			VolumeGroup().show()
		elif (option == '4'):
			LogicalVolume().show()
		elif (option == '5'):
			FileSystem().show()
		elif (option == '6'):
			Lun().create()
		elif (option == '7'):
			Lun().rename()
		elif (option == '8'):
			PhysicalVolume().create()
		elif (option == '9'):
			VolumeGroup().create()
		elif (option == '10'):
			LogicalVolume().create()
		elif (option == '11'):
			FileSystem().create()
		elif (option == '666'):
			Lun().remove()
		elif (option in [ 'q' , 'Q' , 'e' , 'E', 'X', 'x' ]):
			break
		else:
			print 'Invalid Option!'

menu()