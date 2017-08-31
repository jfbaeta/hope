# -*- coding: UTF-8 -*-

from models import *
import re

def detect_lun_amount():

	file = open('multi-grep.txt', 'r')
	regex_uuid = re.compile(r'\w{33}')
	uuids = re.findall(regex_uuid, file.read())
	
	print 'Total amount of LUNs: %s' % len(uuids)

def detect_luns():

	file = open('multi-grep.txt', 'r')
	regex_name = re.compile(r'(\w+)(?:\s\()')
	names = re.findall(regex_name, file.read())
	file.close()
	print names
	for name in names:
		print name

	file = open('multi-grep.txt', 'r')
	regex_uuid = re.compile(r'\w{33}')
	uuids = re.findall(regex_uuid, file.read())
	file.close()
	print uuids
	for uuid in uuids:
		print uuid

	file = open('multi-grep.txt', 'r')
	regex_sysfs = re.compile(r'dm-\d{1,3}')
	sysfss = re.findall(regex_sysfs, file.read())
	file.close()
	print sysfss
	for sysfs in sysfss:
		print sysfs

	file = open('multi-grep.txt', 'r')
	regex_vendor = re.compile(r'(\w+)(?:,)')
	vendors = re.findall(regex_vendor, file.read())
	file.close()
	print vendors
	for vendor in vendors:
		print vendor

	file = open('multi-grep.txt', 'r')
	regex_product = re.compile(r'(?:,)(\w+)')
	products = re.findall(regex_product, file.read())
	file.close()
	print products
	for product in products:
		print product

	file = open('multi-grep.txt', 'r')
	regex_size_n = re.compile(r'(?:size=)(\d+\.?\d*?)')
	sizes_n = re.findall(regex_size_n, file.read())
	file.close()
	print sizes_n
	for size_n in sizes_n:
		print size_n

	file = open('multi-grep.txt', 'r')
	regex_size_m = re.compile(r'([MGT])(?:[\s])')
	sizes_m = re.findall(regex_size_m, file.read())
	file.close()
	print sizes_m
	for size_m in sizes_m:
		print size_m

def detect_pvs():

	luns = []
	lun_dict = {}
	print 'Detecting Multipath LUNs...'
	
	file = open('multi-grep.txt', 'r')

	regex_name = re.compile(r'(^\w+)(?:\s)')
	regex_uuid = re.compile(r'\w{33}')
	regex_sysfs = re.compile(r'dm-\d{1,3}')
	regex_vendor = re.compile(r'(\w+)(?:,)')
	regex_product = re.compile(r'(?:,)(\w+)')
	regex_size_n = re.compile(r'(?:size=)(\d+\.?\d*?)')
	regex_size_m = re.compile(r'([MGT])(?:[\s])')
	regex_discard = re.compile(r'(\:|\+)')

	for line in file:

		name = re.findall(regex_name, line)
		if name:
			name = str(name[0])
			lun_dict['name_key'] = name
			
		uuid = re.findall(regex_uuid, line)
		if uuid:
			uuid = str(uuid[0])
			lun_dict['uuid_key'] = uuid
			
		sysfs = re.findall(regex_sysfs, line)
		if sysfs:
			sysfs = str(sysfs[0])
			lun_dict['sysfs_key'] = sysfs
			
		vendor = re.findall(regex_vendor, line)
		if vendor:
			vendor = str(vendor[0])
			lun_dict['vendor_key'] = vendor
			
		product = re.findall(regex_product, line)
		if product:
			product = str(product[0])
			lun_dict['product_key'] = product
			
		size_n = re.findall(regex_size_n, line)
		if size_n:
			size_n = str(size_n[0])
			lun_dict['size_n_key'] = size_n
			
		size_m = re.findall(regex_size_m, line)
		if size_m:
			size_m = str(size_m[0])
			lun_dict['size_m_key'] = size_m
			
		if len(lun_dict) == 7:
			luns.append(PhysicalVolume(name=name, uuid=uuid, sysfs=sysfs, vendor=vendor, product=product, size_n=size_n, size_m=size_m))

	for i in luns:
		i.show_lun_name()

	#luns.append(PhysicalVolume(name=name, uuid=uuid, wwid='', sysfs=sysfs, vendor=vendor, product=product, size_n=size_n, size_m=size_m))

		#lun = PhysicalVolume(name=name, uuid=uuid, wwid='', sysfs=sysfs, vendor=vendor, product=product, size_n=size_n, size_m=size_m)
		#print lun.name
		#print lun.uuid
		#print lun.sysfs
		#print lun.vendor
		#print lun.product
		#print lun.size_n
		#print lun.size_m
		#luns.append(lun)

		#print 'Nome da Lun: %s' % (name[0])
		#print 'UUID da Lun: %s' % (uuid[0])
		#print 'DM da Lun: %s' % (sysfs[0])
		#print 'Vendor do Storage: %s' % (vendor[0])
		#print 'Modelo do Storage: %s' % (product[0])
		#print 'Tamanho da Lun: %s%s' % (size_n[0], size_m[0])

	file.close()

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
#detect_pvs()
detect_luns()


