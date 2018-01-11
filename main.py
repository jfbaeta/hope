#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from models.models import *
from models.Formatter import Formatter
from models.LogicalVolume import LogicalVolume
from models.Lun import Lun
from models.PhysicalVolume import PhysicalVolume
from models.VolumeGroup import VolumeGroup
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
		print '(5) Create /etc/multipath.conf File'
		print '(6) Reload Multipath to Change Volume Names'
		print '(7) Create Physical Volumes'
		print '(8) Create Volume Groups'
		print '(9) Create Logical Volumes'
		print '(10) Create File Systems'
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
			Lun().create()
		elif (option == '6'):
			Lun().rename()
		elif (option == '7'):
			Lun().show()
			PhysicalVolume().create()
		elif (option == '8'):
			VolumeGroup().create()
		elif (option == '9'):
			LogicalVolume().create()
		elif (option == '10'):
			FileSystem().create()
		elif (option == '666'):
			Lun().remove()
		elif (option in [ 'q' , 'Q' , 'e' , 'E' ]):
			break
		else:
			print 'Invalid Option!'

menu()