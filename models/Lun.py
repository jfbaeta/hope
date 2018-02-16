# -*- coding: UTF-8 -*-

from Formatter import Formatter
from Root import Root
from UsrSap import UsrSap
from Data import Data
from Log import Log
from Shared import Shared
from Linux import Linux
from string import Template
import json, os, re, subprocess

class Lun(object):
	'''
	Class used for List, Creation and Removal of Luns.
	Attributes and methods are used by Formatter Class to output results.
	'''
	general_header = 'SAN Storage Volumes:'
	index_header   = 'Index:'
	size_header    = 'Size:'
	wwid_header    = 'WWID:'
	vendor_header  = 'Vendor:'
	product_header = 'Product:'
	name_header    = 'Name:'

	max_index_header   = len(index_header)
	max_size_header    = len(size_header)
	max_wwid_header    = len(wwid_header)
	max_vendor_header  = len(vendor_header)
	max_product_header = len(product_header)
	max_name_header    = len(name_header)

	list_headers = []
	
	list_headers.append(index_header)
	list_headers.append(size_header)
	list_headers.append(wwid_header)
	list_headers.append(vendor_header)
	list_headers.append(product_header)
	list_headers.append(name_header)

	def __init__(self, index='', size='', wwid='', vendor='', product='', name=''):
		super(Lun, self).__init__()
		self.__list    = []
		self.__index   = index
		self.__size    = size
		self.__wwid    = wwid
		self.__vendor  = vendor
		self.__product = product
		self.__name    = name

	@property
	def index(self):
		return self.__index

	@property
	def size(self):
		return self.__size

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
	def name(self):
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name

	@property
	def all(self):
		
		list_all = []

		list_all.append(self.__index)
		list_all.append(self.__size)
		list_all.append(self.__wwid)
		list_all.append(self.__vendor)
		list_all.append(self.__product)
		list_all.append(self.__name)

		return list_all

	@property
	def lengths(self):
		
		self.list_max_lenghts = []

		if len(self.__index) > self.max_index_header:
			self.max_index_header = len(self.__index)
		if len(self.__size) > self.max_size_header:
			self.max_size_header = len(self.__size)
		if len(self.__wwid) > self.max_wwid_header:
			self.max_wwid_header = len(self.__wwid)
		if len(self.__vendor) > self.max_vendor_header:
			self.max_vendor_header = len(self.__vendor)
		if len(self.__product) > self.max_product_header:
			self.max_product_header = len(self.__product)
		if len(self.__name) > self.max_name_header:
			self.max_name_header = len(self.__name)

		self.list_max_lenghts.append(self.max_index_header)
		self.list_max_lenghts.append(self.max_size_header)
		self.list_max_lenghts.append(self.max_wwid_header)
		self.list_max_lenghts.append(self.max_vendor_header)
		self.list_max_lenghts.append(self.max_product_header)
		self.list_max_lenghts.append(self.max_name_header)

		return self.list_max_lenghts

	@property
	def header(self):
		return self.general_header

	def add(self, resource):
		self.__list.append(resource)

	def get(self):
		return self.__list

	def detect(self):
		'''
		Method to detect current SAN Storage Multipath LUNs.
		It relies on 'multipath -ll' output.
		'''
		temp_luns_list = []

		reg_exps = [
			re.compile(r'(?:size=)(\d+\.?\d*[MGT])(?:[\s])'),\
			re.compile(r'\w{33}'),\
			re.compile(r'(\w+)(?:,)'),\
			re.compile(r'(?:,)(\w+)'),\
			re.compile(r'(\w*)(?:\s\()'),\
		]
		
		cmd_multipath_list = subprocess.Popen(['multipath -ll | grep dm- -A 1'], stdout=subprocess.PIPE, shell=True).communicate()[0]
		
		lun_amount = len(re.findall(reg_exps[0], cmd_multipath_list))
		
		for reg_exp in reg_exps:
			reg_exp_result = re.findall(reg_exp, cmd_multipath_list)
			if not reg_exp_result:
				for item in range(lun_amount):
					reg_exp_result.append('no alias assigned')
			temp_luns_list.append(reg_exp_result)

		luns_list = zip(*temp_luns_list)

		lun_index = 0
		for lun_list in luns_list:
			lun_size    = lun_list[0]
			lun_wwid    = lun_list[1]
			lun_vendor  = lun_list[2]
			lun_product = lun_list[3]
			lun_name    = lun_list[4]
			self.add(Lun(index=str(lun_index), size=lun_size, wwid=lun_wwid, vendor=lun_vendor, product=lun_product, name=lun_name))
			lun_index+=1
	
	def show(self):
		'''
		Method to show current SAN Storage Multipath LUNs.
		It uses detect method to parse results and Formatter class to output it.
		'''
		self.detect()
		return Formatter().show(self)

	def create_multipath_conf(self, str_multipaths):
		'''
		Method to read a template file, create /etc/multipath.conf and reload multipaths.
		Currently only support IBM Storwize Storage and doesn't check if there is an existing file.
		'''
		linux = Linux()

		with open('/opt/hope/templates/template_multipath_ibm_2145.txt', 'r') as tpl_multipath_file:
			print 'Generating /etc/multipath.conf file...'
			tpl_multipath_str = Template(tpl_multipath_file.read())
			new_multipath_str = tpl_multipath_str.safe_substitute(new_multipaths=str_multipaths)

		with open('/etc/multipath.conf', 'w') as new_multipath_file:
			new_multipath_file.write(new_multipath_str)

		with open('/etc/multipath.conf', 'r') as multipath_conf:	
			print '/etc/multipath.conf file created:'
			print multipath_conf.read()

		if linux.distribution in ['SLES', 'SLES_SAP'] and linux.version == '11.4':
			os.system('multipath -r')
		else:
			os.system('systemctl reload multipathd')
			os.system('systemctl status multipathd')
			os.system('multipath -r')

	def create(self):
		'''
		Method to create /etc/multipath.conf aliases and wwids based on interactive user input.
		It puts a suffix for multiple LUNs.
		'''
		rootvg         = Root()
		usrsap         = UsrSap()
		data           = Data()
		log            = Log()
		shared         = Shared()
		new_luns       = Lun()
		final_luns     = Lun()
		purposes       = [rootvg, usrsap, data, log, shared]
		str_multipaths = ''

		self.show()

		for purpose in purposes:
			
			if purpose == rootvg:
				title = purpose.name
			else:
				title = purpose.fs_mount_point

			print 'Type current LUN \033[1mINDEXES\033[0m to be used for %s (comma-separated):' % (title),
			pvs = re.findall('\d+', raw_input())
			pv_amount = len(pvs)

			if not pvs:
				continue

			print 'Type Physical Volume name \033[1mPREFIX\033[0m for %s:' % (title),
			pv_prefix = raw_input()

			pv_count = 1
			for pv in pvs:
				
				if purpose in (rootvg, usrsap) and pv_amount == 1:
					pv_new_name = pv_prefix
				else:
					pv_suffix = str(pv_count)
					pv_new_name = pv_prefix + pv_suffix
				pv_count+=1
				
				for lun in self.get():
					
					if lun.index == pv:
						lun.name = pv_new_name
						new_luns.add(Lun(index=str(lun.index), size=lun.size, wwid=lun.wwid, vendor=lun.vendor, product=lun.product, name=lun.name))
						str_multipaths += '\tmultipath {\n\t\twwid %s\n\t\talias %s\n\t}\n' % (lun.wwid, lun.name)

			Formatter().show(new_luns)

		self.create_multipath_conf(str_multipaths)

		final_luns.show()

	def create_from_config_file(self):
		'''
		Method to create /etc/multipath.conf aliases and wwids based on a JSON config file.
		It puts a suffix for multiple LUNs.
		'''
		final_luns     = Lun()
		str_multipaths = ''

		with open('/opt/hope/config/config.json', 'r') as config_file:
			config = json.load(config_file)

		for purpose_key, purpose_value in config.items():

			if purpose_key in ['rootvg', 'usrsap', 'data', 'log', 'shared']:
				
				for lun in purpose_value['pvs']:

					str_multipaths += '\tmultipath {\n\t\twwid %s\n\t\talias %s\n\t}\n' % (lun['wwid'], lun['alias'])

		self.create_multipath_conf(str_multipaths)

		final_luns.show()

	def remove(self):
		'''
		Method to remove /etc/multipath.conf file and reload multipaths.
		It doesn't detect if there's LVM in place neither asks for user confirmation.
		'''
		linux = Linux()
		#luns  = Lun()

		self.show()

		if not os.path.exists('/etc/multipath.conf'):
			print 'There is no /etc/multipath.conf file. Skipping...'
		else:
			print 'Removing /etc/multipath.conf...'
			os.remove('/etc/multipath.conf')
			
			print 'Reloading Multipath...'
			if linux.version != '11.4':
				print 'Reloading Multipath...'
				subprocess.Popen(['systemctl reload multipathd'], stdout=subprocess.PIPE, shell=True).communicate()[0]
				print 'Checking Multipath Status...'
				subprocess.Popen(['systemctl status multipathd'], stdout=subprocess.PIPE, shell=True).communicate()[0]

			subprocess.Popen(['multipath -r'], stdout=subprocess.PIPE, shell=True).communicate()[0]

		Lun().show()
