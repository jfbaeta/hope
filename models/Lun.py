# -*- coding: UTF-8 -*-

from Formatter import Formatter
from string import Template
import re
import os
import subprocess

class Lun(object):
	
	"""class Lun"""
	
	index_header   = 'Index:'
	devmap_header  = 'Devmap:'
	wwid_header    = 'WWID:'
	vendor_header  = 'Vendor:'
	product_header = 'Product:'
	size_header    = 'Size:'
	name_header    = 'Name:'

	max_index_header   = len(index_header)
	max_devmap_header  = len(devmap_header)
	max_wwid_header    = len(wwid_header)
	max_vendor_header  = len(vendor_header)
	max_product_header = len(product_header)
	max_size_header    = len(size_header)
	max_name_header    = len(name_header)

	list_headers = []
	
	list_headers.append(index_header)
	list_headers.append(devmap_header)
	list_headers.append(wwid_header)
	list_headers.append(vendor_header)
	list_headers.append(product_header)
	list_headers.append(size_header)
	list_headers.append(name_header)

	def __init__(self, index='', devmap='', wwid='', vendor='', product='', size='', name=''):
		super(Lun, self).__init__()
		self.__list    = []
		self.__index   = index
		self.__devmap  = devmap
		self.__wwid    = wwid
		self.__vendor  = vendor
		self.__product = product
		self.__size    = size
		self.__name    = name

	@property
	def index(self):
		return self.__index

	@property
	def devmap(self):
		return self.__devmap

	@property
	def wwid(self):
		return self.__wwid

	@property
	def vendor(self):
		return self.__vendor

	@property
	def product(self):
		return self.__product

	@property
	def size(self):
		return self.__size

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name

	@property
	def all(self):
		
		list_all = []

		list_all.append(self.__index)
		list_all.append(self.__devmap)
		list_all.append(self.__wwid)
		list_all.append(self.__vendor)
		list_all.append(self.__product)
		list_all.append(self.__size)
		list_all.append(self.__name)

		return list_all

	@property
	def lengths(self):
		
		self.list_max_lenghts = []

		if len(self.__index) > self.max_index_header:
			self.max_index_header = len(self.__index)
		if len(self.__devmap) > self.max_devmap_header:
			self.max_devmap_header = len(self.__devmap)
		if len(self.__wwid) > self.max_wwid_header:
			self.max_wwid_header = len(self.__wwid)
		if len(self.__vendor) > self.max_vendor_header:
			self.max_vendor_header = len(self.__vendor)
		if len(self.__product) > self.max_product_header:
			self.max_product_header = len(self.__product)
		if len(self.__size) > self.max_size_header:
			self.max_size_header = len(self.__size)
		if len(self.__name) > self.max_name_header:
			self.max_name_header = len(self.__name)

		self.list_max_lenghts.append(self.max_index_header)
		self.list_max_lenghts.append(self.max_devmap_header)
		self.list_max_lenghts.append(self.max_wwid_header)
		self.list_max_lenghts.append(self.max_vendor_header)
		self.list_max_lenghts.append(self.max_product_header)
		self.list_max_lenghts.append(self.max_size_header)
		self.list_max_lenghts.append(self.max_name_header)

		return self.list_max_lenghts

	def add(self, resource):
		self.__list.append(resource)

	def get(self):
		return self.__list

	def detect(self):

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
			self.add(Lun(index=str(lun_index), devmap=lun_devmap, wwid=lun_wwid, vendor=lun_vendor, product=lun_product, size=lun_size, name=lun_name))
			lun_index+=1
	
	def show(self):
		self.detect()
		return Formatter().show(self)

	def create(self):

		purposes = ['rootvg', '/usr/sap', '/hana/data', '/hana/log', '/hana/shared']

		self.detect()

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
				
				for lun in self.get():
					
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

	def rename(self):
	
		os.system('multipath -r')

	def remove(self):

		os.remove('/etc/multipath.conf')
		os.system('multipath -r')