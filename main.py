#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from models.models import *
from models.Formatter import Formatter
from models.Lun import Lun
from models.PhysicalVolume import PhysicalVolume
from models.VolumeGroup import VolumeGroup
from models.LogicalVolume import LogicalVolume
from models.FileSystem import FileSystem
from string import Template
import re
import os
import subprocess

purposes = ['rootvg', '/usr/sap', '/hana/data', '/hana/log', '/hana/shared']

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
		print '(Q,q,E,e) Quit/Exit'
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
		elif (option in [ 'q' , 'Q' , 'e' , 'E' ]):
			break
		else:
			print 'Invalid Option!'

menu()