# -*- coding: UTF-8 -*-

from models import *
from string import Template
import re

def create_lun():
	
	disco = PhysicalVolume(name='mpathA', wwid='360050768028101875000000000000fff', devmap='dm-10', vendor='IBM', product='2145', size_n='512', size_m='G')

	disco.get_name()

	disco.change_name('mpathB')

	disco.get_name()

	disco.change_name(name='mpathC')

	disco.get_name()

	exit()

def detect_luns():

	global luns
	luns = []

	temp_lun_list = []

	regex_list = [
		re.compile(r'(\w+)(?:\s\()'),\
		re.compile(r'\w{33}'),\
		re.compile(r'dm-\d{1,3}'),\
		re.compile(r'(\w+)(?:,)'),\
		re.compile(r'(?:,)(\w+)'),\
		re.compile(r'(?:size=)(\d+\.?\d*)'),\
		re.compile(r'([MGT])(?:[\s])')
		]
	
	for regex_index in regex_list:
		file = open('multi-grep.txt', 'r')
		regex_result = re.findall(regex_index, file.read())
		temp_lun_list.append(regex_result)
		file.close()

	lun_list = zip(*temp_lun_list)

	for lun_index in lun_list:
		lun_name = lun_index[0]
		lun_wwid = lun_index[1]
		lun_devmap = lun_index[2]
		lun_vendor = lun_index[3]
		lun_product = lun_index[4]
		lun_size_n = lun_index[5]
		lun_size_m = lun_index[6]
		luns.append(PhysicalVolume(name=lun_name, wwid=lun_wwid, devmap=lun_devmap, vendor=lun_vendor, product=lun_product, size_n=lun_size_n, size_m=lun_size_m))

	for lun in luns:
		print '%s %s %s %s %s %s%s' % (lun.get_name(), lun.get_wwid(), lun.get_devmap(), lun.get_vendor(), lun.get_product(), lun.get_size_n(), lun.get_size_m())

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

def create_pvs():

	detect_luns()

	pvs_data = []
	pvs_log = []
	pvs_shared = []

	print 'Type current LUN(s) to be used for rootvg:',
	rootvg_old_name = raw_input()

	print 'Type new LUN name(s) for rootvg:',
	rootvg_new_name = raw_input()

	for lun in luns:
		lun_name_target = lun.get_name()
		if lun_name_target == rootvg_old_name:
			print 'LUN Choosed:  %s %s %s %s %s %s%s' % (lun.get_name(), lun.get_wwid(), lun.get_devmap(), lun.get_vendor(), lun.get_product(), lun.get_size_n(), lun.get_size_m())
			alias_pv_rootvg = rootvg_new_name
			print 'New LUN Name: %s %s %s %s %s %s%s' % (alias_pv_rootvg, lun.get_wwid(), lun.get_devmap(), lun.get_vendor(), lun.get_product(), lun.get_size_n(), lun.get_size_m())

	print 'Type current LUN(s) to be used for /usr/sap:',
	usr_sap_old_name = raw_input()

	print 'Type new LUN name(s) for /usr/sap:',
	usr_sap_new_name = raw_input()

	for lun in luns:
		lun_name_target = lun.get_name()
		if lun_name_target == usr_sap_old_name:
			print 'LUN Choosed:  %s %s %s %s %s %s%s' % (lun.get_name(), lun.get_wwid(), lun.get_devmap(), lun.get_vendor(), lun.get_product(), lun.get_size_n(), lun.get_size_m())
			alias_pv_usr_sap = usr_sap_new_name
			print 'New LUN Name: %s %s %s %s %s %s%s' % (alias_pv_usr_sap, lun.get_wwid(), lun.get_devmap(), lun.get_vendor(), lun.get_product(), lun.get_size_n(), lun.get_size_m())

	print 'Type current LUN(s) to be used for /hana/data:',
	pv_names = re.findall('\w{1,}', raw_input())
	pv_amount = len(pv_names)

	print 'Type Physical Volume name prefix for /hana/data:',
	pv_prefix = raw_input()

	pv_count = 1
	for pv_name in pv_names:
		pv_suffix = str(pv_count)
		pv_new_name = pv_prefix + pv_suffix
		pvs_data.append(pv_new_name)
		pv_count+=1
		for lun in luns:
			lun_name_target = lun.get_name()
			if lun_name_target == pv_name:
				print 'LUN Choosed:   %s %s %s %s %s %s%s' % (lun.get_name(), lun.get_wwid(), lun.get_devmap(), lun.get_vendor(), lun.get_product(), lun.get_size_n(), lun.get_size_m())
				print 'New LUN Name:  %s %s %s %s %s %s%s' % (pv_new_name, lun.get_wwid(), lun.get_devmap(), lun.get_vendor(), lun.get_product(), lun.get_size_n(), lun.get_size_m())

	alias_pv_hana_data_01 = pvs_data[0]
	alias_pv_hana_data_02 = pvs_data[1]
	alias_pv_hana_data_03 = pvs_data[2]
	alias_pv_hana_data_04 = pvs_data[3]
	
	print 'Type current LUN(s) to be used for /hana/log:',
	pv_names = raw_input()
	pv_names_list = re.findall('\w{1,}', pv_names)
	print pv_names_list
	pv_amount = len(pv_names_list)

	print 'Type Physical Volume name prefix for /hana/log:',
	pv_prefix = raw_input()

	pv_count = 1
	while (pv_count <= pv_amount):
		pv_suffix = str(pv_count)
		pv_name = pv_prefix + pv_suffix
		pvs_log.append(pv_name)
		print 'Creating Physical Volume %s...' % (pv_name)
		pv_count+=1

	alias_pv_hana_log_01 = pvs_log[0]

	print 'Type current LUN(s) to be used for /hana/shared:',
	pv_names = raw_input()
	pv_names_list = re.findall('\w{1,}', pv_names)
	print pv_names_list
	pv_amount = len(pv_names_list)

	print 'Type Physical Volume name prefix for /hana/shared:',
	pv_prefix = raw_input()

	pv_count = 1
	while (pv_count <= pv_amount):
		pv_suffix = str(pv_count)
		pv_name = pv_prefix + pv_suffix
		pvs_shared.append(pv_name)
		print 'Creating Physical Volume %s...' % (pv_name)
		pv_count+=1

	alias_pv_hana_shared_01 = pvs_shared[0]

	wwid_pv_rootvg = luns[0].get_wwid()
	wwid_pv_usr_sap = luns[1].get_wwid()
	wwid_pv_hana_data_01 = luns[2].get_wwid()
	wwid_pv_hana_data_02 = luns[3].get_wwid()
	wwid_pv_hana_data_03 = luns[4].get_wwid()
	wwid_pv_hana_data_04 = luns[5].get_wwid()
	wwid_pv_hana_log_01 = luns[6].get_wwid()
	wwid_pv_hana_shared_01 = luns[7].get_wwid()

	tpl_multipath_file = open('template_multipath.txt', 'r')
	tpl_multipath_read = tpl_multipath_file.read()
	tpl_multipath_str = Template(tpl_multipath_read)

	new_multipath_str = tpl_multipath_str.safe_substitute(
		alias_pv_rootvg=alias_pv_rootvg,
		alias_pv_usr_sap=alias_pv_usr_sap,
		alias_pv_hana_data_01=alias_pv_hana_data_01,
		alias_pv_hana_data_02=alias_pv_hana_data_02,
		alias_pv_hana_data_03=alias_pv_hana_data_03,
		alias_pv_hana_data_04=alias_pv_hana_data_04,
		alias_pv_hana_log_01=alias_pv_hana_log_01,
		alias_pv_hana_shared_01=alias_pv_hana_shared_01,
		wwid_pv_rootvg=wwid_pv_rootvg,
		wwid_pv_usr_sap=wwid_pv_usr_sap,
		wwid_pv_hana_data_01=wwid_pv_hana_data_01,
		wwid_pv_hana_data_02=wwid_pv_hana_data_02,
		wwid_pv_hana_data_03=wwid_pv_hana_data_03,
		wwid_pv_hana_data_04=wwid_pv_hana_data_04,
		wwid_pv_hana_log_01=wwid_pv_hana_log_01,
		wwid_pv_hana_shared_01=wwid_pv_hana_shared_01)

	tpl_multipath_file.close()

	with open('multipath.conf', 'w') as new_multipath_file:
		new_multipath_file.write(new_multipath_str)
		new_multipath_file.close()

	exit()

def create_vgs(vgs):
	print 'Type Volume Group name for Data:',
	vg = raw_input()
	vgs.append(vg)
	print 'Volume Group for Data will be %s' % (vg)

	print 'Type Volume Group name for Log:',
	vg = raw_input()
	vgs.append(vg)
	print 'Volume Group for Log will be %s' % (vg)

	print 'Type Volume Group name for Shared:',
	vg = raw_input()
	vgs.append(vg)
	print 'Volume Group for Shared will be %s' % (vg)

	print 'Creating Volume Group %s...' % (vgs[0])
	print 'Creating Volume Group %s...' % (vgs[1])
	print 'Creating Volume Group %s...' % (vgs[2])

	exit()

def create_lvs(lvs):
	print 'Type Logical Volume name for Data:',
	lv = raw_input()
	lvs.append(lv)
	print 'Logical Volume for Data will be %s' % (lv)

	print 'Type Logical Volume name for Log:',
	lv = raw_input()
	lvs.append(lv)
	print 'Logical Volume for Log will be %s' % (lv)

	print 'Type Logical Volume name for Shared:',
	lv = raw_input()
	lvs.append(lv)
	print 'Logical Volume for Shared will be %s' % (lv)

	print 'Creating Logical Volume %s...' % (lvs[0])
	print 'Creating Logical Volume %s...' % (lvs[1])
	print 'Creating Logical Volume %s...' % (lvs[2])

	exit()

def create_fss(fss):
	print 'Type File System name for Data:',
	fs = raw_input()
	fss.append(fs)
	print 'File System for Data will be %s.' % (fs)
	
	print 'Type File System name for Log:',
	fs = raw_input()
	fss.append(fs)
	print 'File System for Log will be %s.' % (fs)

	print 'Type File System name for Shared:',
	fs = raw_input()
	fss.append(fs)
	print 'File System for Shared will be %s.' % (fs)

	print 'Creating File System %s...' % (fss[0])
	print 'Creating File System %s...' % (fss[1])
	print 'Creating File System %s...' % (fss[2])

	exit()

def menu():

	vgs = []
	lvs = []
	fss = []

	option = True
	
	while option:
		print '(1) Detect Multipath LUNs'
		print '(2) Create Physical Volumes'
		print '(3) Create Volume Groups'
		print '(4) Create Logical Volumes'
		print '(5) Create File Systems'
		print '(6) Create Storage LUN'
		print '(Q,q,E,e) Quit/Exit'
		print 'Choose your Option:',
		option = raw_input()

		if (option == '1'):
			detect_luns()
		elif (option == '2'):
			create_pvs()
		elif (option == '3'):
			create_vgs(vgs)
		elif (option == '4'):
			create_lvs(lvs)
		elif (option == '5'):
			create_fss(fss)
		elif (option == '6'):
			create_lun()
		elif (option in [ 'q' , 'Q' , 'e' , 'E' ]):
			break
		else:
			print 'Invalid Option!'

menu()