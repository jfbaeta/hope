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

def detect_fss():
	pass

def create_multipath_conf():

	detect_luns()

	str_mulitpaths = ''

	for purpose in purposes:
		
		print 'Type current LUN(s) to be used for %s:' % (purpose),
		pvs = re.findall('\d+', raw_input())
		pv_amount = len(pvs)

		print 'Type Physical Volume name prefix for %s:' % (purpose),
		pv_prefix = raw_input()

		pv_count = 1
		for pv in pvs:
			
			if purpose in ('rootvg', '/usr/sap') and pv_amount == 1:
				pv_new_name = pv_prefix
			else:
				pv_suffix = str(pv_count)
				pv_new_name = pv_prefix + pv_suffix
			pv_count+=1
			
			for lun in luns.get():
				
				if lun.index == pv:
					print 'LUN Purpose:   %s' % (purpose)
					print 'LUN Choosed:   %s %s %s %s %s' % (lun.index, lun.wwid, lun.vendor, lun.product, lun.size)
					lun.name = pv_new_name
					print 'New LUN Name:  %s' % (lun.name)
					str_mulitpaths += '\tmultipath {\n\t\twwid %s\n\t\talias %s\n\t}\n' % (lun.wwid, lun.name)

	tpl_multipath_file = open('templates/template_multipath.txt', 'r')
	
	tpl_multipath_str = Template(tpl_multipath_file.read())
	
	new_multipath_str = tpl_multipath_str.safe_substitute(new_multipaths=str_mulitpaths)
	
	tpl_multipath_file.close()

	with open('/etc/multipath.conf', 'w') as new_multipath_file:
		new_multipath_file.write(new_multipath_str)
		new_multipath_file.close()

def change_lun_names():
	
	multipath_reload = 'multipath -r'
	os.system(multipath_reload)

def create_pvs():

	detect_luns()

	detect_pvs()

	print 'Type LUN names that will be used as Physical Volumes:',
	pvs = re.findall('\d+', raw_input())
	
	for pv in pvs:
	
		for lun in luns.get():

			if lun.index == pv:
				cmd_pvcreate = 'pvcreate /dev/mapper/%s' % (lun.name)
				os.system(cmd_pvcreate)

def create_vgs():

	detect_pvs()

	detect_vgs()

	for purpose in purposes[1:]:

		print 'Type Volume Group name for %s:' % (purpose),
		vg_name = raw_input()
		
		print 'Type Physical Volume names for %s:' % (vg_name),
		pv_names = re.findall('\w{1,}', raw_input())
		pv_names_str = ' /dev/mapper/'.join(pv_names)
		
		if purpose == '/usr/sap':
			cmd_vgcreate = 'vgcreate %s /dev/mapper/%s' % (vg_name, pv_names_str)
		else:
			cmd_vgcreate = 'vgcreate -s 1M --dataalignment 1M %s /dev/mapper/%s' % (vg_name, pv_names_str)
		
		os.system(cmd_vgcreate)

def create_lvs():

	detect_vgs()

	detect_lvs()

	for purpose in purposes[1:]:

		print 'Type Logical Volume name for %s:' % (purpose),
		lv_name = raw_input()
		
		print 'Type Volume Group name for %s:' % (lv_name),
		vg_name = raw_input()
		
		if purpose == '/hana/data':
			cmd_lvcreate = 'lvcreate -i 4 -I 256K -l 100%%VG -n %s %s' % (lv_name, vg_name)
		else:
			cmd_lvcreate = 'lvcreate -l 100%%VG -n %s %s' % (lv_name, vg_name)
		
		os.system(cmd_lvcreate)

def create_fss():

	detect_lvs()

	detect_fss()

	print 'Type the SID for this system:',
	sid = raw_input()

	for purpose in purposes[1:]:

		print 'Type Logical Volume number for %s:' % (purpose),
		lv_name = raw_input()

		if purpose == '/usr/sap':
			fs_type = 'ext3'
			fs_args = ''
		else:
			fs_type = 'xfs'
			fs_args = '-b size=4096 -s size=4096'

		for lv in lvs:
				
			if str(lv.get_index()) == lv_name:
				
				cmd_mkfs = 'mkfs.%s %s /dev/mapper/%s-%s' % (fs_type, fs_args, lv.get_vgname(), lv.get_lvname())
				os.system(cmd_mkfs)
	
				cmd_mkdir = 'mkdir -p %s' % (purpose)
				os.system(cmd_mkdir)
	
				cmd_add_fstab = 'echo \"/dev/%s/%s\t\t%s\t%s\tdefaults\t0 0\" >> /etc/fstab' % (lv.get_vgname(), lv.get_lvname(), purpose, fs_type)
				os.system(cmd_add_fstab)
	
				cmd_mount = 'mount %s' % (purpose)
				os.system(cmd_mount)
	
				cmd_mkdir_sid = 'mkdir -p %s/%s' % (purpose, sid)
				os.system(cmd_mkdir_sid)

	cmd_df = 'df -h'
	os.system(cmd_df)

def reset_multipaths():
	
	os.remove('/etc/multipath.conf')

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
		print '(11) Create Storage LUN'
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
			create_multipath_conf()
		elif (option == '6'):
			change_lun_names()
		elif (option == '7'):
			create_pvs()
		elif (option == '8'):
			create_vgs()
		elif (option == '9'):
			create_lvs()
		elif (option == '10'):
			create_fss()
		elif (option == '11'):
			create_lun()
		elif (option == '666'):
			reset_multipaths()
		elif (option in [ 'q' , 'Q' , 'e' , 'E' ]):
			break
		else:
			print 'Invalid Option!'

menu()