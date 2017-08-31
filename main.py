# -*- coding: UTF-8 -*-

from models import *
import re

def detect_pvs():
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
			lun_dict = {}
			name = str(name[0])
			lun_dict['name_key'] = name
			print lun_dict

		uuid = re.findall(regex_uuid, line)
		if uuid:
			uuid = str(uuid[0])
			lun_dict['uuid_key'] = uuid
			print lun_dict

		sysfs = re.findall(regex_sysfs, line)
		if sysfs:
			sysfs = str(sysfs[0])
			lun_dict['sysfs_key'] = sysfs
			print lun_dict

		vendor = re.findall(regex_vendor, line)
		if vendor:
			vendor = str(vendor[0])
			lun_dict['vendor_key'] = vendor
			print lun_dict

		product = re.findall(regex_product, line)
		if product:
			product = str(product[0])
			lun_dict['product_key'] = product
			print lun_dict

		size_n = re.findall(regex_size_n, line)
		if size_n:
			size_n = str(size_n[0])
			lun_dict['size_n_key'] = size_n
			print lun_dict

		size_m = re.findall(regex_size_m, line)
		if size_m:
			size_m = str(size_m[0])
			lun_dict['size_m_key'] = size_m
			print lun_dict

		print len(lun_dict)
		if len(lun_dict) == 7:
			print 'Igual a 7'
			luns.append(PhysicalVolume(name=name, uuid=uuid, wwid='', sysfs=sysfs, vendor=vendor, product=product, size_n=size_n, size_m=size_m))
			del lun_dict

		cnt+=1
	print len(luns)
	print type(luns)
	print luns.name



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
luns = PhysicalVolume.gen_luns('multi-grep.txt')

print len(luns)
print luns[0]
print luns[1]
print luns[2]
print luns[3]
print luns[4]
print luns[5]
print luns[6]
print luns[7]





