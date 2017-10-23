# -*- coding: UTF-8 -*-

from models import *
from string import Template
import re
import os
import subprocess

purposes = ['rootvg', '/usr/sap', '/hana/data', '/hana/log', '/hana/shared']

def detect_luns():

	global luns
	luns = Storage()

	temp_luns_list = []

	reg_exps = [
		re.compile(r'dm-\d*'),\
		re.compile(r'\w{33}'),\
		re.compile(r'(\w+)(?:,)'),\
		re.compile(r'(?:,)(\w+)'),\
		re.compile(r'(?:size=)(\d+\.?\d*[MGT])(?:[\s])'),\
		re.compile(r'(\w*)(?:\s\()'),\
	]
	
	lun_amount = len(re.findall(reg_exps[0], subprocess.Popen(['multipath -ll | grep dm- -A 1'], stdout=subprocess.PIPE, shell=True).stdout.read()))
	
	for reg_exp in reg_exps:
		cmd_multipath_list  = subprocess.Popen(['multipath -ll | grep dm- -A 1'], stdout=subprocess.PIPE, shell=True).communicate()[0]
		reg_exp_result = re.findall(reg_exp, cmd_multipath_list)
		if not reg_exp_result:
			for item in range(lun_amount):
				reg_exp_result.append('no alias assigned')
		temp_luns_list.append(reg_exp_result)

	luns_list = zip(*temp_luns_list)

	lun_index = 0
	for lun_list in luns_list:
		lun_devmap  = lun_list[0]
		lun_wwid    = lun_list[1]
		lun_vendor  = lun_list[2]
		lun_product = lun_list[3]
		lun_size    = lun_list[4]
		lun_name    = lun_list[5]
		luns.add(Lun(index=str(lun_index), devmap=lun_devmap, wwid=lun_wwid, vendor=lun_vendor, product=lun_product, size=lun_size, name=lun_name))
		lun_index+=1
	
	index_header   = 'Index:'
	devmap_header  = 'Devmap:'
	wwid_header    = 'WWID:'
	vendor_header  = 'Vendor:'
	product_header = 'Product:'
	size_header    = 'Size:'
	name_header    = 'Name:'

	Formatter().show(luns)

	max_len_index   = len(index_header)
	max_len_devmap  = len(devmap_header)
	max_len_wwid    = len(wwid_header)
	max_len_vendor  = len(vendor_header)
	max_len_product = len(product_header)
	max_len_size    = len(size_header)
	max_len_name    = len(name_header)
	
	for lun in luns.get():
		len_index = len(lun.index)
		if len_index > max_len_index:
			max_len_index = len_index
		len_devmap = len(lun.devmap)
		if len_devmap > max_len_devmap:
			max_len_devmap = len_devmap
		len_wwid = len(lun.wwid)
		if len_wwid > max_len_wwid:
			max_len_wwid = len_wwid
		len_vendor = len(lun.vendor)
		if len_vendor > max_len_vendor:
			max_len_vendor = len_vendor
		len_product = len(lun.product)
		if len_product > max_len_product:
			max_len_product = len_product
		len_size = len(lun.size)
		if len_size > max_len_size:
			max_len_size = len_size
		len_name = len(lun.name)
		if len_name > max_len_name:
			max_len_name = len_name

	total_len = max_len_index + \
				max_len_devmap + \
				max_len_wwid + \
				max_len_vendor + \
				max_len_product + \
				max_len_size + \
				max_len_name

	print '+-' + '-' * (total_len + 18) + '-+'
	print '| \033[1m%s\033[0m | \033[1m%s\033[0m | \033[1m%s\033[0m | \033[1m%s\033[0m | \033[1m%s\033[0m | \033[1m%s\033[0m | \033[1m%s\033[0m |' % \
		(index_header.ljust(max_len_index),\
		devmap_header.ljust(max_len_devmap),\
		wwid_header.ljust(max_len_wwid),\
		vendor_header.ljust(max_len_vendor),\
		product_header.ljust(max_len_product),\
		size_header.ljust(max_len_size),\
		name_header.ljust(max_len_name))
	print '+-' + '-' * (total_len + 18) + '-+'
	for lun in luns.get():
		print '| %s | %s | %s | %s | %s | %s | %s |' % \
			(lun.index.ljust(max_len_index),\
			 lun.devmap.ljust(max_len_devmap),\
			 lun.wwid.ljust(max_len_wwid),\
			 lun.vendor.ljust(max_len_vendor),\
			 lun.product.ljust(max_len_product),\
			 lun.size.ljust(max_len_size),\
			 lun.name.ljust(max_len_name))
	print '+-' + '-' * (total_len + 18) + '-+'

def detect_pvs():
	pass

def detect_vgs():
	pass

def detect_lvs():
	
	global lvs
	lvs = []

	temp_lvs_list = []

	reg_exps = [
		re.compile(r'(\/dev\/.*\/.*?)(?::)'),\
		re.compile(r'(?::)(.*)(?::)'),\
		re.compile(r'(?:.*:)(.*)'),\
	]
	
	for reg_exp in reg_exps:
		cmd_lvs_list = subprocess.Popen(['lvs -o lv_path,vg_name,lv_name --noheadings --unbuffered --separator : --config \'devices{ filter = [ "a|/dev/mapper/*|", "r|.*|" ] }\''], stdout=subprocess.PIPE, shell=True).communicate()[0]
		reg_exp_result = re.findall(reg_exp, cmd_lvs_list)
		temp_lvs_list.append(reg_exp_result)

	lvs_list = zip(*temp_lvs_list)

	lv_index = 0
	for lv_list in lvs_list:
		lv_path = lv_list[0]
		vg_name = lv_list[1]
		lv_name = lv_list[2]
		lvs.append(LogicalVolume(index=lv_index, lvpath=lv_path, vgname=vg_name, lvname=lv_name))
		lv_index+=1
	
	for lv in lvs:
		print '%s %s %s %s' % (lv.get_index(), lv.get_lvpath(), lv.get_vgname(), lv.get_lvname())

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
		print '(2) Create /etc/multipath.conf File'
		print '(3) Reload Multipath to Change Volume Names'
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