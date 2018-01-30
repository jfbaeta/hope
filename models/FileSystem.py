# -*- coding: UTF-8 -*-

from Formatter import Formatter
from LogicalVolume import LogicalVolume
from Root import Root
from UsrSap import UsrSap
from Data import Data
from Log import Log
from Shared import Shared
import json, os, re, subprocess, sys

class FileSystem(object):
	'''
	Class used for List, Creation and Removal of File Systems.
	Attributes and methods are used by Formatter Class to output results.
	'''
	general_header = 'File Systems:'
	index_header   = 'Index:'
	lvname_header  = 'Logical Volume:'
	size_header    = 'Size:'
	name_header    = 'Mount Point:'

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

	@property
	def header(self):
		return self.general_header

	def add(self, resource):
		self.__list.append(resource)

	def get(self):
		return self.__list

	def detect(self):
		'''
		Method to detect current File Systems.
		It relies on 'df' output. It doesn't check /etc/fstab yet.
		'''		
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
		'''
		Method to show current File Systems.
		It uses detect method to parse results and Formatter class to output it.
		'''
		self.detect()
		return Formatter().show(self)

	def check_is_sid_is_ok(self, sid):
		'''
		Method to check if SAP System ID (SID) is alpha-numeric and has three characters.
		'''
		sid = sid
		return sid.isalnum() and len(sid) == 3

	def create(self):
		'''
		Method to create File Systems based on interactive user input.
		It creates File Systems, full-path directories with SAP SID, add it to /etc/fstab and mount it.
		'''
		usrsap = UsrSap()
		data   = Data()
		log    = Log()
		shared = Shared()

		purposes = [usrsap, data, log, shared]

		self.detect()

		lvs = LogicalVolume()
		lvs.detect()

		while True:
			print 'Type the \033[1mSID\033[0m for this system:',
			sid = raw_input().upper()
			if self.check_is_sid_is_ok(sid):
				break
			else:
				print 'SAP System ID (SID) must have 3 digits and be alpha-numeric.'

		for purpose in purposes:

			print 'Type Logical Volume \033[1mINDEX\033[0m for %s (comma-separated):' % (purpose.fs_mount_point),
			lv_index = raw_input()

			for lv in lvs.get():
					
				if lv.index == lv_index:
					
					if purpose.fs_type == 'ext3':	
						os.system('mkfs.%s %s /dev/mapper/%s-%s' % (purpose.fs_type, purpose.fs_args, lv.vgname, lv.name))
					else:
						os.system('mkfs.%s -f %s /dev/mapper/%s-%s' % (purpose.fs_type, purpose.fs_args, lv.vgname, lv.name))
					os.system('mkdir -p %s' % (purpose.fs_mount_point))
					os.system('echo \"/dev/%s/%s\t\t%s\t%s\tdefaults\t0 0\" >> /etc/fstab' % (lv.vgname, lv.name, purpose.fs_mount_point, purpose.fs_type))
					os.system('mount %s' % (purpose.fs_mount_point))
					os.system('mkdir -p %s/%s' % (purpose.fs_mount_point, sid))

		os.system('df -h')

	def create_from_config_file(self):
		'''
		Method to create LVM Volume Groups based on a JSON config file.
		It relies on 'vgcreate' command.
		'''
		usrsap = UsrSap()
		data   = Data()
		log    = Log()
		shared = Shared()

		purposes = [usrsap, data, log, shared]

		self.detect()

		lvs = LogicalVolume()
		lvs.detect()

		with open('/opt/hope/config/config.json', 'r') as config_file:
			config = json.load(config_file)

		sid = config['sid']

		if not self.check_is_sid_is_ok(sid):
			print 'Current SID in your JSON config file: \033[1m%s\033[0m' % (sid)
			print 'SAP System ID (SID) must have 3 digits and be alpha-numeric.'
			sys.exit(1)

		for purpose in purposes:

			for purpose_key, purpose_value in config.items():

				if purpose_key == purpose.name:

					if purpose.fs_type == 'ext3':
						os.system('mkfs.%s %s /dev/mapper/%s-%s' % (purpose.fs_type, purpose.fs_args, purpose_value['vg'], purpose_value['lv']))
					else:
						os.system('mkfs.%s -f %s /dev/mapper/%s-%s' % (purpose.fs_type, purpose.fs_args, purpose_value['vg'], purpose_value['lv']))
					
					os.system('mkdir -p %s' % (purpose.fs_mount_point))
					os.system('echo \"/dev/%s/%s\t\t%s\t%s\tdefaults\t0 0\" >> /etc/fstab' % (purpose_value['vg'], purpose_value['lv'], purpose.fs_mount_point, purpose.fs_type))
					os.system('mount %s' % (purpose.fs_mount_point))
					os.system('mkdir -p %s/%s' % (purpose.fs_mount_point, sid))
		
		os.system('df -h')

	def remove(self):
		'''
		Method to remove File Systems file and reload multipaths.
		It doesn't detect if there's LVM in place neither asks for user confirmation.
		'''
		self.detect()

		print 'Type File System \033[1mINDEXES\033[0m to remove (comma-separated):',
		fs_indexes = re.findall('\d+', raw_input())

		for fs_index in fs_indexes:

			for fs in self.get():

				if fs.index == fs_index:

					cmd_fuser = 'fuser -ck %s' % (fs.name)
					os.system(cmd_fuser)

					cmd_umount = 'umount -f %s' % (fs.name)
					os.system(cmd_umount)

					with open("/etc/fstab", "r+") as etc_fstab_file:
						
						etc_fstab_file_lines = etc_fstab_file.readlines()
						etc_fstab_file.seek(0)
						
						for line in etc_fstab_file_lines:
							if fs.name not in line:
								etc_fstab_file.write(line)

						etc_fstab_file.truncate()
