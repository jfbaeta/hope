# -*- coding: UTF-8 -*-

from Formatter import Formatter
import re
import os
import subprocess

class FileSystem(object):
	
	"""class FileSystem"""
	
	index_header  = 'Index:'
	path_header   = 'Path:'
	lvname_header = 'Logical Volume:'
	name_header   = 'Name:'

	max_index_header  = len(index_header)
	max_path_header   = len(path_header)
	max_lvname_header = len(lvname_header)
	max_name_header   = len(name_header)

	list_headers = []
	
	list_headers.append(index_header)
	list_headers.append(path_header)
	list_headers.append(lvname_header)
	list_headers.append(name_header)

	def __init__(self, index='', path='', lvname='', name=''):
		super(FileSystem, self).__init__()
		self.__list  = []
		self.__index  = index
		self.__path   = path
		self.__lvname = lvname
		self.__name   = name

	@property
	def index(self):
		return self.__index

	@property
	def path(self):
		return self.__path

	@property
	def lvname(self):
		return self.__lvname

	@property
	def name(self):
		return self.__name

	@property
	def all(self):
		
		list_all = []

		list_all.append(self.__index)
		list_all.append(self.__path)
		list_all.append(self.__lvname)
		list_all.append(self.__name)

		return list_all

	@property
	def lengths(self):
		
		self.list_max_lenghts = []

		if len(self.__index) > self.max_index_header:
			self.max_index_header = len(self.__index)
		if len(self.__path) > self.max_path_header:
			self.max_path_header = len(self.__path)
		if len(self.__vgname) > self.max_vgname_header:
			self.max_lvname_header = len(self.__lvname)
		if len(self.__name) > self.max_name_header:
			self.max_name_header = len(self.__name)

		self.list_max_lenghts.append(self.max_index_header)
		self.list_max_lenghts.append(self.max_path_header)
		self.list_max_lenghts.append(self.max_lvname_header)
		self.list_max_lenghts.append(self.max_name_header)

		return self.list_max_lenghts

	def add(self, resource):
		self.__list.append(resource)

	def get(self):
		return self.__list

	def detect(self):
		pass
		
	def show(self):
		self.detect()
		return Formatter().show(self)

	def create(self):

		self.detect()

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