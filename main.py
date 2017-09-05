# -*- coding: UTF-8 -*-

from models import *
import re

def detect_luns():

	luns = []

	temp_lun_list = []

	regex_list = [
		re.compile(r'(\w+)(?:\s\()'),\
		re.compile(r'\w{33}'),\
		re.compile(r'dm-\d{1,3}'),\
		re.compile(r'(\w+)(?:,)'),\
		re.compile(r'(?:,)(\w+)'),\
		re.compile(r'(?:size=)(\d+\.?\d*?)'),\
		re.compile(r'([MGT])(?:[\s])')
		]
	
	for regex_index in regex_list:
		file = open('multi-grep.txt', 'r')
		regex_result = re.findall(regex_index, file.read())
		temp_lun_list.append(regex_result)
		file.close()

	lun_list = zip(*temp_lun_list)

	print lun_list

	for lun_index in lun_list:
		lun_name = lun_index[0]
		lun_wwid = lun_index[1]
		lun_devmap = lun_index[2]
		lun_vendor = lun_index[3]
		lun_product = lun_index[4]
		lun_size_n = lun_index[5]
		lun_size_m = lun_index[6]
		luns.append(PhysicalVolume(name=lun_name, wwid=lun_wwid, devmap=lun_devmap, vendor=lun_vendor, product=lun_product, size_n=lun_size_n, size_m=lun_size_m))

	teste0 = '| Name: %s | WWID: %s | Storage: %s %s | Size: %s%s |' % (luns[0].name, luns[0].wwid, luns[0].vendor, luns[0].product, luns[0].size_n, luns[0].size_m)
	teste1 = '| Name: %s | WWID: %s | Storage: %s %s | Size: %s%s |' % (luns[1].name, luns[1].wwid, luns[1].vendor, luns[1].product, luns[1].size_n, luns[1].size_m)
	teste2 = '| Name: %s | WWID: %s | Storage: %s %s | Size: %s%s |' % (luns[2].name, luns[2].wwid, luns[2].vendor, luns[2].product, luns[2].size_n, luns[2].size_m)
	teste3 = '| Name: %s | WWID: %s | Storage: %s %s | Size: %s%s |' % (luns[3].name, luns[3].wwid, luns[3].vendor, luns[3].product, luns[3].size_n, luns[3].size_m)
	teste4 = '| Name: %s | WWID: %s | Storage: %s %s | Size: %s%s |' % (luns[4].name, luns[4].wwid, luns[4].vendor, luns[4].product, luns[4].size_n, luns[4].size_m)
	teste5 = '| Name: %s | WWID: %s | Storage: %s %s | Size: %s%s |' % (luns[5].name, luns[5].wwid, luns[5].vendor, luns[5].product, luns[5].size_n, luns[5].size_m)
	teste6 = '| Name: %s | WWID: %s | Storage: %s %s | Size: %s%s |' % (luns[6].name, luns[6].wwid, luns[6].vendor, luns[6].product, luns[6].size_n, luns[6].size_m)
	teste7 = '| Name: %s | WWID: %s | Storage: %s %s | Size: %s%s |' % (luns[7].name, luns[7].wwid, luns[7].vendor, luns[7].product, luns[7].size_n, luns[7].size_m)
	string_val = '+' + ('-' * (len(teste0) -2)) + '+'
	print string_val
	print teste0
	print '| Name: \033[1;32m%s\033[0m | WWID: %s | Storage: %s %s | Size: %s%s |' % (luns[0].name, luns[0].wwid, luns[0].vendor, luns[0].product, luns[0].size_n, luns[0].size_m)
	print teste1
	print teste2
	print teste3
	print teste4
	print teste5
	print teste6
	print teste7
	print string_val

def create_multipath_conf():
	detect_luns()
	for i in luns:
		h_index = luns.index(i) + 1
		print h_index, i.name , i.wwid



def create_pvs(pvs):

	print 'Type the amount of Physical Volumes for Data:',
	pv_amount = int(raw_input())

	print 'Type Physical Volume name prefix for Data:',
	pv_prefix = raw_input()

	pv_count = 1
	while (pv_count <= pv_amount):
		pv_suffix = str(pv_count)
		pv_name = pv_prefix + pv_suffix
		pvs.append(pv_name)
		print 'Creating Physical Volume %s...' % (pv_name)
		pv_count+=1

	print 'Type the amount of Physical Volumes for Log:',
	pv_amount = int(raw_input())

	print 'Type Physical Volume name prefix for Log:',
	pv_prefix = raw_input()

	pv_count = 1
	while (pv_count <= pv_amount):
		pv_suffix = str(pv_count)
		pv_name = pv_prefix + pv_suffix
		pvs.append(pv_name)
		print 'Creating Physical Volume %s...' % (pv_name)
		pv_count+=1

	print 'Type the amount of Physical Volumes for Shared:',
	pv_amount = int(raw_input())

	print 'Type Physical Volume name prefix for Shared:',
	pv_prefix = raw_input()

	pv_count = 1
	while (pv_count <= pv_amount):
		pv_suffix = str(pv_count)
		pv_name = pv_prefix + pv_suffix
		pvs.append(pv_name)
		print 'Creating Physical Volume %s...' % (pv_name)
		pv_count+=1

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

	pvs = []
	vgs = []
	lvs = []
	fss = []

	option = True
	
	while option:
		print '(1) Detect Multipath LUNs'
		print '(2) Create /etc/multipath.conf file'
		print '(3) Create Physical Volumes'
		print '(4) Create Volume Groups'
		print '(5) Create Logical Volumes'
		print '(6) Create File Systems'
		print '(Q,q,E,e) Quit/Exit'
		print 'Choose your Option:',
		option = raw_input()

		if (option == '1'):
			detect_luns()
		elif (option == '2'):
			create_multipath_conf()
		elif (option == '3'):
			create_pvs(pvs)
		elif (option == '4'):
			create_vgs(vgs)
		elif (option == '5'):
			create_lvs(lvs)
		elif (option == '6'):
			create_fss(fss)
		elif (option in [ 'q' , 'Q' , 'e' , 'E' ]):
			break
		else:
			print 'Invalid Option!'

menu()


