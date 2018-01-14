# -*- coding: UTF-8 -*-

from Formatter import Formatter
from VolumeGroup import VolumeGroup
import re
import os
import subprocess

class LogicalVolume(object):
	
	"""class LogicalVolume"""
	
	index_header  = 'Index:'
	path_header   = 'Path:'
	vgname_header = 'Volume Group:'
	name_header   = 'Name:'

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

	def add(self, resource):
		self.__list.append(resource)

	def get(self):
		return self.__list

	def detect(self):
		
		temp_lvs_list = []

		reg_exps = [
			re.compile(r'(\/dev\/.*\/.*?)(?::)'),\
			re.compile(r'(?::)(.*)(?::)'),\
			re.compile(r'(?:.*:)(.*)'),\
		]
		
		cmd_lvs_list = subprocess.Popen(['lvs -o lv_path,vg_name,lv_name --noheadings --unbuffered --separator : --config \'devices{ filter = [ "a|/dev/mapper/*|", "r|.*|" ] }\''], stdout=subprocess.PIPE, shell=True).communicate()[0]

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
		self.detect()
		return Formatter().show(self)

	def create(self):

		purposes = ['rootvg', '/usr/sap', '/hana/data', '/hana/log', '/hana/shared']

		self.detect()

		vgs = VolumeGroup()
		vgs.detect()

		for purpose in purposes[1:]:

			print 'Type Logical Volume name for %s:' % (purpose),
			lv_name = raw_input()
			
			print 'Type Volume Group name for %s:' % (lv_name),
			vg_indexes = re.findall('\d+', raw_input())
			vg_index = vg_indexes[0]

			for vg in vgs.get():

				if vg.index == vg_index:
			
					if purpose == '/hana/data':
						cmd_lvcreate = 'lvcreate -i 4 -I 256K -l 100%%VG -n %s %s' % (lv_name, vg.name)
					else:
						cmd_lvcreate = 'lvcreate -l 100%%VG -n %s %s' % (lv_name, vg.name)
			
					os.system(cmd_lvcreate)