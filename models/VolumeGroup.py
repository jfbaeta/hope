# -*- coding: UTF-8 -*-

from Formatter import Formatter
from PhysicalVolume import PhysicalVolume
from Root import Root
from UsrSap import UsrSap
from Data import Data
from Log import Log
from Shared import Shared
import re
import os
import subprocess

class VolumeGroup(object):
	
	"""class VolumeGroup"""

	index_header = 'Index:'
	name_header  = 'Name:'
	size_header  = 'Size:'
	free_header  = 'Free:'

	max_index_header = len(index_header)
	max_name_header  = len(name_header)
	max_size_header  = len(size_header)
	max_free_header  = len(free_header)

	list_headers = []
	
	list_headers.append(index_header)
	list_headers.append(name_header)
	list_headers.append(size_header)
	list_headers.append(free_header)

	def __init__(self, index='', name='', size='', free=''):
		super(VolumeGroup, self).__init__()
		self.__list  = []
		self.__index = index
		self.__name  = name
		self.__size  = size
		self.__free  = free

	@property
	def index(self):
		return self.__index

	@property
	def name(self):
		return self.__name

	@property
	def size(self):
		return self.__size

	@property
	def free(self):
		return self.__free

	@property
	def all(self):
		
		list_all = []

		list_all.append(self.__index)
		list_all.append(self.__name)
		list_all.append(self.__size)
		list_all.append(self.__free)

		return list_all

	@property
	def lengths(self):
		
		self.list_max_lenghts = []

		if len(self.__index) > self.max_index_header:
			self.max_index_header = len(self.__index)
		if len(self.__name) > self.max_name_header:
			self.max_name_header = len(self.__name)
		if len(self.__size) > self.max_size_header:
			self.max_size_header = len(self.__size)
		if len(self.__free) > self.max_free_header:
			self.max_free_header = len(self.__free)

		self.list_max_lenghts.append(self.max_index_header)
		self.list_max_lenghts.append(self.max_name_header)
		self.list_max_lenghts.append(self.max_size_header)
		self.list_max_lenghts.append(self.max_free_header)

		return self.list_max_lenghts

	@property
	def header(self):
		return "Volume Groups:"

	def add(self, resource):
		self.__list.append(resource)

	def get(self):
		return self.__list

	def detect(self):

		temp_vgs_list = []

		reg_exps = [
			re.compile(r'(\w+)(?:.*)'),\
			re.compile(r'(?::)(.*)(?::)'),\
			re.compile(r'(?:.*:)(.*)'),\
		]
		
		cmd_vgs_list = subprocess.Popen(['vgs -o vg_name,vg_size,vg_free --noheadings --unbuffered --separator : --config \'devices{ filter = [ "a|/dev/mapper/*|", "r|.*|" ] }\''], stdout=subprocess.PIPE, shell=True).communicate()[0]

		for reg_exp in reg_exps:
			reg_exp_result = re.findall(reg_exp, cmd_vgs_list)
			temp_vgs_list.append(reg_exp_result)

		vgs_list = zip(*temp_vgs_list)

		vg_index = 0
		for vg_list in vgs_list:
			vg_name = vg_list[0]
			vg_size = vg_list[1]
			vg_free = vg_list[2]
			self.add(VolumeGroup(index=str(vg_index), name=vg_name, size=vg_size, free=vg_free))
			vg_index+=1

	def show(self):
		self.detect()
		return Formatter().show(self)

	def create(self):

		rootvg = Root()
		usrsap = UsrSap()
		data   = Data()
		log    = Log()
		shared = Shared()

		purposes = [usrsap, data, log, shared]

		self.detect()

		pvs = PhysicalVolume()
		pvs.detect()

		for purpose in purposes:

			print 'Type Volume Group \033[1mNAME\033[0m for %s:' % (purpose.fs_mount_point),
			vg_name = raw_input()

			print 'Type Physical Volume \033[1mINDEXES\033[0m for %s:' % (vg_name),
			pv_indexes = re.findall('\d+', raw_input())
			pv_names = ''		

			for pv_index in pv_indexes:

				for pv in pvs.get():

					if pv.index == pv_index:
						pv_names += '%s ' % (pv.name)

			cmd_vgcreate = 'vgcreate %s %s %s' % (purpose.vg_args, vg_name, pv_names)
			os.system(cmd_vgcreate)