# -*- coding: UTF-8 -*-

from Formatter import Formatter
from LogicalVolume import LogicalVolume
import re
import os
import subprocess

class FileSystem(object):
	
	"""class FileSystem"""
	
	index_header  = 'Index:'
	lvname_header = 'Logical Volume:'
	size_header   = 'Size:'
	name_header   = 'Mount Point:'

	max_index_header  = len(index_header)
	max_lvname_header = len(lvname_header)
	max_size_header   = len(size_header)
	max_name_header   = len(name_header)

	list_headers = []
	
	list_headers.append(index_header)
	list_headers.append(lvname_header)
	list_headers.append(size_header)
	list_headers.append(name_header)

	def __init__(self, index='', lvname='', size='', name=''):
		super(FileSystem, self).__init__()
		self.__list   = []
		self.__index  = index
		self.__lvname = lvname
		self.__size   = size
		self.__name   = name

	@property
	def index(self):
		return self.__index

	@property
	def lvname(self):
		return self.__lvname

	@property
	def size(self):
		return self.__size

	@property
	def name(self):
		return self.__name

	@property
	def all(self):
		
		list_all = []

		list_all.append(self.__index)
		list_all.append(self.__lvname)
		list_all.append(self.__size)
		list_all.append(self.__name)

		return list_all

	@property
	def lengths(self):
		
		self.list_max_lenghts = []

		if len(self.__index) > self.max_index_header:
			self.max_index_header = len(self.__index)
		if len(self.__lvname) > self.max_lvname_header:
			self.max_lvname_header = len(self.__lvname)
		if len(self.__size) > self.max_size_header:
			self.max_size_header = len(self.__size)
		if len(self.__name) > self.max_name_header:
			self.max_name_header = len(self.__name)

		self.list_max_lenghts.append(self.max_index_header)
		self.list_max_lenghts.append(self.max_lvname_header)
		self.list_max_lenghts.append(self.max_size_header)
		self.list_max_lenghts.append(self.max_name_header)

		return self.list_max_lenghts

	def add(self, resource):
		self.__list.append(resource)

	def get(self):
		return self.__list

	def detect(self):
		
		temp_fss_list = []

		reg_exps = [
			re.compile(r'\/dev\/mapper\/[a-zA-Z0-9-_]*'),\
			re.compile(r'(?:\/dev\/mapper\/[a-zA-Z0-9-_]*\s*)(\d*.\d*[MGT])'),\
			re.compile(r'(?:%\s)(.*)')
			]

		cmd_fss_list = subprocess.Popen(['df -h -x tmpfs | grep -v Filesystem'], stdout=subprocess.PIPE, shell=True).communicate()[0]

		for reg_exp in reg_exps:
			reg_exp_result = re.findall(reg_exp, cmd_fss_list)
			temp_fss_list.append(reg_exp_result)

		fss_list = zip(*temp_fss_list)

		fs_index = 0
		for fs_list in fss_list:
			fs_lvname = fs_list[0]
			fs_size   = fs_list[1]
			fs_name   = fs_list[2]
			self.add(FileSystem(index=str(fs_index), lvname=fs_lvname, size=fs_size, name=fs_name))
			fs_index+=1
		
	def show(self):
		self.detect()
		return Formatter().show(self)

	def create(self):

		purposes = ['rootvg', '/usr/sap', '/hana/data', '/hana/log', '/hana/shared']

		self.detect()

		lvs = LogicalVolume()
		lvs.detect()

		print 'Type the SID for this system:',
		sid = raw_input()

		for purpose in purposes[1:]:

			print 'Type Logical Volume number for %s:' % (purpose),
			lv_index = raw_input()

			if purpose == '/usr/sap':
				fs_type = 'ext3'
				fs_args = ''
			else:
				fs_type = 'xfs'
				fs_args = '-b size=4096 -s size=4096'

			for lv in lvs.get():
					
				if lv.index == lv_index:
					
					cmd_mkfs = 'mkfs.%s %s /dev/mapper/%s-%s' % (fs_type, fs_args, lv.vgname, lv.name)
					os.system(cmd_mkfs)
		
					cmd_mkdir = 'mkdir -p %s' % (purpose)
					os.system(cmd_mkdir)
		
					cmd_add_fstab = 'echo \"/dev/%s/%s\t\t%s\t%s\tdefaults\t0 0\" >> /etc/fstab' % (lv.vgname, lv.name, purpose, fs_type)
					os.system(cmd_add_fstab)
		
					cmd_mount = 'mount %s' % (purpose)
					os.system(cmd_mount)
		
					cmd_mkdir_sid = 'mkdir -p %s/%s' % (purpose, sid)
					os.system(cmd_mkdir_sid)

		cmd_df = 'df -h'
		os.system(cmd_df)