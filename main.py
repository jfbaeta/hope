# -*- coding: UTF-8 -*-

from models import *
from string import Template
import re
import os
import subprocess

purposes = ['rootvg', '/usr/sap', '/hana/data', '/hana/log', '/hana/shared']

def detect_luns():

	global luns
	luns = []

	temp_lun_list = []

	reg_exps = [
		re.compile(r'\w{33}'),\
		re.compile(r'dm-\d{1,3}'),\
		re.compile(r'(\w+)(?:,)'),\
		re.compile(r'(?:,)(\w+)'),\
		re.compile(r'(?:size=)(\d+\.?\d*)'),\
		re.compile(r'([MGT])(?:[\s])')
		]
	
	for reg_exp in reg_exps:
		multipath_cmd  = subprocess.Popen(['multipath -ll | grep dm- -A 1'], stdout=subprocess.PIPE, shell=True)
		reg_exp_result = re.findall(reg_exp, multipath_cmd.stdout.read())
		temp_lun_list.append(reg_exp_result)

	lun_list = zip(*temp_lun_list)

	for lun_index in lun_list:
		lun_wwid    = lun_index[0]
		lun_devmap  = lun_index[1]
		lun_vendor  = lun_index[2]
		lun_product = lun_index[3]
		lun_size_n  = lun_index[4]
		lun_size_m  = lun_index[5]
		luns.append(StorageVolume(wwid=lun_wwid, devmap=lun_devmap, vendor=lun_vendor, product=lun_product, size_n=lun_size_n, size_m=lun_size_m))

	for lun in luns:
		print '%s %s %s %s %s%s' % (lun.get_devmap(), lun.get_wwid(), lun.get_vendor(), lun.get_product(), lun.get_size_n(), lun.get_size_m())

#	lun0 = '| %s %s %s %s %s %s%s |' % (luns[0].get_name(), luns[0].get_wwid(), luns[0].get_devmap(), luns[0].get_vendor(), luns[0].get_product(), luns[0].get_size_n(), luns[0].get_size_m())
#	lun1 = '| %s %s %s %s %s %s%s |' % (luns[1].get_name(), luns[1].get_wwid(), luns[1].get_devmap(), luns[1].get_vendor(), luns[1].get_product(), luns[1].get_size_n(), luns[1].get_size_m())
#	lun2 = '| %s %s %s %s %s %s%s |' % (luns[2].get_name(), luns[2].get_wwid(), luns[2].get_devmap(), luns[2].get_vendor(), luns[2].get_product(), luns[2].get_size_n(), luns[2].get_size_m())
#		
#	list_length = []
#	for i in luns:
#		lun_length = (len(i.get_name() + i.get_wwid() + i.get_devmap() + i.get_vendor() + i.get_product() + i.get_size_n() + i.get_size_m()))
#		list_length.append(lun_length)
#
#	header = '+' + (('-' * (max(list_length) + 7))) + '+'
#	
#	print header
#	print lun0
#	print lun1
#	print lun2
#	print header

def detect_pvs():
	pass

def detect_vgs():
	pass

def detect_lvs():
	pass

def detect_fss():
	pass

def create_multipath_conf():

	detect_luns()

	str_mulitpaths = ''

	for purpose in purposes:
		
		print 'Type current LUN(s) to be used for %s:' % (purpose),
		pvs = re.findall('dm-\d*', raw_input())
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
			
			for lun in luns:
				
				lun_target_devmap = lun.get_devmap()
				
				if lun_target_devmap == pv:
					lun.change_purpose(purpose)
					print 'LUN Purpose:   %s' % (lun.get_purpose())
					print 'LUN Choosed:   %s %s %s %s %s%s' % (lun.get_devmap(), lun.get_wwid(), lun.get_vendor(), lun.get_product(), lun.get_size_n(), lun.get_size_m())
					lun.change_name(pv_new_name)
					print 'New LUN Name:  %s' % (lun.get_name())
					str_mulitpaths += '\tmultipath {\n\t\twwid %s\n\t\talias %s\n\t}\n' % (lun.get_wwid(), lun.get_name())

	tpl_multipath_file = open('../templates/template_multipath.txt', 'r')
	
	tpl_multipath_str = Template(tpl_multipath_file.read())
	
	new_multipath_str = tpl_multipath_str.safe_substitute(new_multipaths=str_mulitpaths)
	
	tpl_multipath_file.close()

	with open('/etc/multipath.conf', 'w') as new_multipath_file:
		new_multipath_file.write(new_multipath_str)
		new_multipath_file.close()

def change_lun_names():
	
	# cmd = 'multipath -r'
	# os.system(cmd)
	cmd = 'ls -l'
	os.system(cmd)

def create_pvs():

	detect_luns()

	detect_pvs()

	print 'Type LUN names that will be used as Physical Volumes:',
	pv_names = re.findall('\w{1,}', raw_input())
	for pv_name in pv_names:
		# cmd = 'pvcreate /dev/mapper/%s' % (pv_name)
		# os.system(cmd)
		print 'pvcreate /dev/mapper/%s' % (pv_name)

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
			# cmd = 'vgcreate %s /dev/mapper/%s' % (vg_name, pv_names_str)
			# os.system(cmd)
			print 'vgcreate %s /dev/mapper/%s' % (vg_name, pv_names_str)
		else:
			# cmd = 'vgcreate -s 1M --dataalignment 1M %s /dev/mapper/%s' % (vg_name, pv_names_str)
			# os.system(cmd)
			print 'vgcreate -s 1M --dataalignment 1M %s /dev/mapper/%s' % (vg_name, pv_names_str)

def create_lvs():

	detect_vgs()

	detect_lvs()

	for purpose in purposes[1:]:

		print 'Type Logical Volume name for %s:' % (purpose),
		lv_name = raw_input()
		
		print 'Type Volume Group name for %s:' % (lv_name),
		vg_name = raw_input()
		
		if purpose == '/usr/sap':
			# cmd = 'lvcreate -l 100%VG -n %s %s' % (lv_name, vg_name)
			# os.system(cmd)
			print 'lvcreate -l 100%%VG -n %s %s' % (lv_name, vg_name)
		else:
			# cmd = 'lvcreate -i 4 -I 256K -l 100%VG -n %s %s' % (lv_name, vg_name)
			# os.system(cmd)
			print 'lvcreate -i 4 -I 256K -l 100%%VG -n %s %s' % (lv_name, vg_name)

def create_fss():

	detect_lvs()

	detect_fss()

	print 'Type the SID for this system:',
	sid = raw_input()

	for purpose in purposes[1:]:

		print 'Type Logical Volume name for %s:' % (purpose),
		lv_name = raw_input()
		
		if purpose == '/usr/sap':
			fs_type = 'ext3'
			fs_args = ''
		else:
			fs_type = 'xfs'
			fs_args = '-b size=4096 -s size=4096'

		# cmd = 'mkfs.%s %s /dev/mapper/%s-%s' % (fs_type, fs_args, vg_name, lv_name)
		# os.system(cmd)
		print 'mkfs.%s %s /dev/mapper/%s-%s' % (fs_type, fs_args, 'vg', lv_name)
		
		# cmd = 'mkdir -p %s' % (purpose)
		# os.system(cmd)
		print 'mkdir -p %s' % (purpose)

		# cmd = 'echo \"/dev/%s/%s\t\t%s\t%s\tdefaults\t0 0\" >> /etc/fstab' % (vg_name, lv_name, purpose, fs_type)
		# os.system(cmd)
		print 'echo \"/dev/%s/%s\t\t%s\t%s\tdefaults\t0 0\" >> /etc/fstab' % ('vg', lv_name, purpose, fs_type)

		# cmd = 'mount %s' % (purpose)
		# os.system(cmd)
		print 'mount %s' % (purpose)

		# cmd = 'mkdir -p %s/%s' % (purpose, sid)
		# os.system(cmd)
		print 'mkdir -p %s/%s' % (purpose, sid)

	# cmd = 'df -h'
	# os.system(cmd)
	print 'df -h'

def reset_multipaths():
	
	os.remove('/etc/multipath.conf')

def menu():

	option = True
	
	while option:
		print '(1) Detect Storage Volumes'
		print '(2) Create multipath.conf'
		print '(3) Change Storage Volume Names'
		print '(4) Create Physical Volumes'
		print '(5) Create Volume Groups'
		print '(6) Create Logical Volumes'
		print '(7) Create File Systems'
		print '(8) Create Storage LUN'
		print '(666) RESET MULTPATHS!'
		print '(Q,q,E,e) Quit/Exit'
		print 'Choose your Option:',
		option = raw_input()

		if (option == '1'):
			detect_luns()
		elif (option == '2'):
			create_multipath_conf()
		elif (option == '3'):
			change_lun_names()
		elif (option == '4'):
			create_pvs()
		elif (option == '5'):
			create_vgs()
		elif (option == '6'):
			create_lvs()
		elif (option == '7'):
			create_fss()
		elif (option == '8'):
			create_lun()
		elif (option == '666'):
			reset_multipaths()
		elif (option in [ 'q' , 'Q' , 'e' , 'E' ]):
			break
		else:
			print 'Invalid Option!'

menu()