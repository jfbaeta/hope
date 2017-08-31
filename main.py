# -*- coding: UTF-8 -*-

from models import *
import re

def detect_luns():

	luns = []

	file = open('multi-grep.txt', 'r')
	regex_name = re.compile(r'(\w+)(?:\s\()')
	names = re.findall(regex_name, file.read())
	file.close()

	file = open('multi-grep.txt', 'r')
	regex_uuid = re.compile(r'\w{33}')
	uuids = re.findall(regex_uuid, file.read())
	file.close()

	file = open('multi-grep.txt', 'r')
	regex_devmap = re.compile(r'dm-\d{1,3}')
	devmaps = re.findall(regex_devmap, file.read())
	file.close()

	file = open('multi-grep.txt', 'r')
	regex_vendor = re.compile(r'(\w+)(?:,)')
	vendors = re.findall(regex_vendor, file.read())
	file.close()

	file = open('multi-grep.txt', 'r')
	regex_product = re.compile(r'(?:,)(\w+)')
	products = re.findall(regex_product, file.read())
	file.close()

	file = open('multi-grep.txt', 'r')
	regex_size_n = re.compile(r'(?:size=)(\d+\.?\d*?)')
	sizes_n = re.findall(regex_size_n, file.read())
	file.close()

	file = open('multi-grep.txt', 'r')
	regex_size_m = re.compile(r'([MGT])(?:[\s])')
	sizes_m = re.findall(regex_size_m, file.read())
	file.close()

	lun_list_count = len(names)
	lun_list_index=0
	while lun_list_index < lun_list_count:
		name = names[lun_list_index]
		uuid = uuids[lun_list_index]
		devmap = devmaps[lun_list_index]
		vendor = vendors[lun_list_index]
		product = products[lun_list_index]
		size_n = sizes_n[lun_list_index]
		size_m = sizes_m[lun_list_index]
		luns.append(PhysicalVolume(name=name, uuid=uuid, devmap=devmap, vendor=vendor, product=product, size_n=size_n, size_m=size_m))
		lun_list_index+=1

	teste = '| Lun Name: %s | Lun UUID: %s | Storage: %s %s |' % (luns[0].name, luns[0].uuid, luns[0].vendor, luns[0].product)
	string_val = '+' + ('-' * (len(teste) -2)) + '+'
	print string_val
	print teste
	print string_val
	
	#print 'Lun Name: %s | Lun UUID: %s | Storage: %s %s' % (luns[0].name, luns[0].uuid, luns[0].vendor, luns[0].product)
	#print 'Lun Name: %s | Lun UUID: %s | Storage: %s %s' % (luns[1].name, luns[1].uuid, luns[1].vendor, luns[1].product)

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

	option =''
	
	while(option != 'Q' and option != 'q' and option != 'E' and option != 'e'):
		print 'Detect Multipath LUNs (0)'
		print 'Create Physical Volumes (1)'
		print 'Create Volume Groups (2)'
		print 'Create Logical Volumes (3)'
		print 'Create File Systems (4)'
		print 'Quit/Exit (Q,q,E,e)'
		print 'Choose your Option:',
		option = raw_input()

		if(option == '0'):
			detect_pvs()

		if(option == '1'):
			create_pvs(pvs)

		if(option == '2'):
			create_vgs(vgs)


		if(option == '3'):
			create_lvs(lvs)

		if(option == '4'):
			create_fss(fss)

		if(option != '0' and option != '1' and option != '2' and option != '3' and option != '4' and option != 'Q' and option != 'q' and option !='E' and option !='e'):
			print 'Invalid Option!'

#menu()
detect_luns()


