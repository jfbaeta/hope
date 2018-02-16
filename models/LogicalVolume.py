# -*- coding: UTF-8 -*-

from Formatter import Formatter
from VolumeGroup import VolumeGroup
from Root import Root
from UsrSap import UsrSap
from Data import Data
from Log import Log
from Shared import Shared
import json, os, re, subprocess

class LogicalVolume(object):
	'''
	Class used for List, Creation and Removal of Logical Volumes.
	Attributes and methods are used by Formatter Class to output results.
	'''
	general_header = 'Logical Volumes:'
	index_header   = 'Index:'
	path_header    = 'Path:'
	vgname_header  = 'Volume Group:'
	name_header    = 'Name:'

	max_index_header  = len(index_header)
	max_path_header   = len(path_header)
	max_vgname_header = len(vgname_header)
	max_name_header   = len(name_header)

	list_headers = []
	
	list_headers.append(index_header)
	list_headers.append(path_header)
	list_headers.append(vgname_header)
	list_headers.append(name_header)

	def __init__(self, index='', path='', vgname='', name=''):
		super(LogicalVolume, self).__init__()
		self.__list  = []
		self.__index  = index
		self.__path   = path
		self.__vgname = vgname
		self.__name   = name

	@property
	def index(self):
		return self.__index

	@property
	def path(self):
		return self.__path

	@property
	def vgname(self):
		return self.__vgname

	@property
	def name(self):
		return self.__name

	@property
	def all(self):
		
		list_all = []

		list_all.append(self.__index)
		list_all.append(self.__path)
		list_all.append(self.__vgname)
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
			self.max_vgname_header = len(self.__vgname)
		if len(self.__name) > self.max_name_header:
			self.max_name_header = len(self.__name)

		self.list_max_lenghts.append(self.max_index_header)
		self.list_max_lenghts.append(self.max_path_header)
		self.list_max_lenghts.append(self.max_vgname_header)
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
		Method to detect current LVM Logical Volumes.
		It relies on 'lvs' output.
		'''		
		temp_lvs_list = []

		reg_exps = [
			re.compile(r'(\/dev\/.*\/.*?)(?::)'),\
			re.compile(r'(?::)(.*)(?::)'),\
			re.compile(r'(?:.*:)(.*)'),\
		]
		
		cmd_lvs_list = subprocess.Popen(['lvs -o lv_path,vg_name,lv_name --noheadings --unbuffered --separator : 2> /dev/null'], stdout=subprocess.PIPE, shell=True).communicate()[0]

		for reg_exp in reg_exps:
			reg_exp_result = re.findall(reg_exp, cmd_lvs_list)
			temp_lvs_list.append(reg_exp_result)

		lvs_list = zip(*temp_lvs_list)

		lv_index = 0
		for lv_list in lvs_list:
			lv_path = lv_list[0]
			vg_name = lv_list[1]
			lv_name = lv_list[2]
			self.add(LogicalVolume(index=str(lv_index), path=lv_path, vgname=vg_name, name=lv_name))
			lv_index+=1
		
	def show(self):
		'''
		Method to show current LVM Logical Volumes.
		It uses detect method to parse results and Formatter class to output it.
		'''
		self.detect()
		return Formatter().show(self)

	def create(self):
		'''
		Method to create LVM Logical Volumes based on interactive user input.
		It relies on 'lvcreate' command.
		'''
		usrsap   = UsrSap()
		data     = Data()
		log      = Log()
		shared   = Shared()
		vgs      = VolumeGroup()
		purposes = [usrsap, data, log, shared]

		vgs.show()

		for purpose in purposes:

			print 'Type Logical Volume \033[1mNAME\033[0m for %s:' % (purpose.fs_mount_point),
			lv_name = raw_input()
			
			print 'Type Volume Group \033[1mINDEX\033[0m for %s (comma-separated):' % (lv_name),
			vg_indexes = re.findall('\d+', raw_input())
			vg_index = vg_indexes[0]

			for vg in vgs.get():

				if vg.index == vg_index:

					cmd_lvcreate = 'lvcreate %s -n %s %s' % (purpose.lv_args, lv_name, vg.name)
					os.system(cmd_lvcreate)

		self.show()

	def create_from_config_file(self):
		'''
		Method to create LVM Volume Groups based on a JSON config file.
		It relies on 'vgcreate' command.
		'''
		usrsap   = UsrSap()
		data     = Data()
		log      = Log()
		shared   = Shared()
		purposes = [usrsap, data, log, shared]

		with open('/opt/hope/config/config.json', 'r') as config_file:
			config = json.load(config_file)

		for purpose in purposes:

			for purpose_key, purpose_value in config.items():

				if purpose_key == purpose.name:

					os.system('lvcreate %s -n %s %s' % (purpose.lv_args, purpose_value['lv'], purpose_value['vg']))

		self.show()

	def remove(self):
		'''
		Method to remove LVM Logical Volumes file and reload multipaths.
		It doesn't detect if there's LVM in place neither asks for user confirmation.
		'''
		lvs = LogicalVolume()

		self.show()

		print 'Type Logical Volume \033[1mINDEXES\033[0m to remove (comma-separated):',
		lv_indexes = re.findall('\d+', raw_input())

		for lv_index in lv_indexes:

			for lv in self.get():

				if lv.index == lv_index:

					cmd_lvremove = 'lvremove -f %s/%s' % (lv.vgname, lv.name)
					os.system(cmd_lvremove)

		lvs.show()
