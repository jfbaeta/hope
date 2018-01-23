# -*- coding: UTF-8 -*-

from Formatter import Formatter
from Lun import Lun
from Root import Root
from UsrSap import UsrSap
from Data import Data
from Log import Log
from Shared import Shared
import json, os, re, subprocess

class PhysicalVolume(object):
	
	"""class PhysicalVolume"""
	
	general_header = 'Physical Volumes:'
	index_header   = 'Index:'
	name_header    = 'Name:'
	size_header    = 'Size:'
	free_header    = 'Free:'

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
		super(PhysicalVolume, self).__init__()
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
		return self.general_header

	def add(self, resource):
		self.__list.append(resource)

	def get(self):
		return self.__list

	def detect(self):

		temp_pvs_list = []

		reg_exps = [
			re.compile(r'(\/dev\/.*\/.*?)(?::)'),\
			re.compile(r'(?::)(.*)(?::)'),\
			re.compile(r'(?:.*:)(.*)(?:\s)'),\
		]
		
		cmd_pvs_list = subprocess.Popen(['pvs -o pv_name,pv_size,pv_free --noheadings --unbuffered --separator : --config \'devices{ filter = [ "a|/dev/mapper/*|", "r|.*|" ] }\''], stdout=subprocess.PIPE, shell=True).communicate()[0]

		for reg_exp in reg_exps:
			reg_exp_result = re.findall(reg_exp, cmd_pvs_list)
			temp_pvs_list.append(reg_exp_result)

		pvs_list = zip(*temp_pvs_list)

		pv_index = 0
		for pv_list in pvs_list:
			pv_name = pv_list[0]
			pv_size = pv_list[1]
			pv_free = pv_list[2]
			self.add(PhysicalVolume(index=str(pv_index), name=pv_name, size=pv_size, free=pv_free))
			pv_index+=1

	def show(self):
		self.detect()
		return Formatter().show(self)

	def create(self):

		self.detect()

		luns = Lun()
		luns.detect()

		print 'Type Lun \033[1mINDEXES\033[0m that will be used as Physical Volumes:',
		pvs = re.findall('\d+', raw_input())
		
		for pv in pvs:
		
			for lun in luns.get():

				if lun.index == pv:

					cmd_pvcreate = 'pvcreate /dev/mapper/%s' % (lun.name)
					os.system(cmd_pvcreate)

	def create_from_config_file(self):

		with open('/opt/hope/config/config.json', 'r') as config_file:
			config = json.load(config_file)

		for purpose_key, purpose_value in config.items():

			if purpose_key not in ['sid', 'rootvg']:

				for resource_key, resource_value in purpose_value.items():

					if resource_key == 'pvs':

						for lun in resource_value:
							cmd_pvcreate = 'pvcreate /dev/mapper/%s' % (lun['alias'])
							os.system(cmd_pvcreate)

	def remove(self):
		
		self.detect()

		print 'Type Physical Volume \033[1mINDEXES\033[0m to remove:',
		pv_indexes = re.findall('\d+', raw_input())

		for pv_index in pv_indexes:

			for pv in self.get():

				if pv.index == pv_index:

					cmd_pvremove = 'pvremove -f %s' % (pv.name)
					os.system(cmd_pvremove)

