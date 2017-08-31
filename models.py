# -*- coding: UTF-8 -*-
import re

class PhysicalVolume(object):
	"""class PhysicalVolume"""
	def __init__(self, name, sysfs, uuid, vendor, product, size_n, size_m):
		super(PhysicalVolume, self).__init__()
		self.name = name
		self.sysfs = sysfs
		self.uuid = uuid
		self.vendor = vendor
		self.product = product
		self.size_n = size_n
		self.size_m = size_m

	@staticmethod
	def gen_luns(file_name):
		luns = []
		file = open(file_name, 'r')

		regex_name = re.compile(r'(^\w+)(?:\s)')
		regex_uuid = re.compile(r'\w{33}')
		regex_sysfs = re.compile(r'dm-\d{1,3}')
		regex_vendor = re.compile(r'(\w+)(?:,)')
		regex_product = re.compile(r'(?:,)(\w+)')
		regex_size_n = re.compile(r'(?:size=)(\d+\.?\d*?)')
		regex_size_m = re.compile(r'([MGT])(?:[\s])')
		regex_discard = re.compile(r'(\:|\+)')

		for line in file:
			name = re.findall(regex_name, line)
			if name:
				lun_dict = {}
				name = str(name[0])
				lun_dict['name_key'] = name
	
			uuid = re.findall(regex_uuid, line)
			if uuid:
				uuid = str(uuid[0])
				lun_dict['uuid_key'] = uuid
	
			sysfs = re.findall(regex_sysfs, line)
			if sysfs:
				sysfs = str(sysfs[0])
				lun_dict['sysfs_key'] = sysfs
	
			vendor = re.findall(regex_vendor, line)
			if vendor:
				vendor = str(vendor[0])
				lun_dict['vendor_key'] = vendor
	
			product = re.findall(regex_product, line)
			if product:
				product = str(product[0])
				lun_dict['product_key'] = product
	
			size_n = re.findall(regex_size_n, line)
			if size_n:
				size_n = str(size_n[0])
				lun_dict['size_n_key'] = size_n
	
			size_m = re.findall(regex_size_m, line)
			if size_m:
				size_m = str(size_m[0])
				lun_dict['size_m_key'] = size_m
			
			if len(lun_dict) == 7:
				luns.append(PhysicalVolume(*lun_dict))
				del lun_dict

		file.close
		return luns

class VolumeGroup(object):
	"""class VolumeGroup"""
	def __init__(self, name, pvs):
		super(VolumeGroup, self).__init__()
		self.name = name
		self.pvs = pvs

class LogicalVolume(object):
	"""class LogicalVolume"""
	def __init__(self, name, vg):
		super(LogicalVolume, self).__init__()
		self.name = name
		self.vg = vg

class FileSystem(object):
	"""class FileSystem"""
	def __init__(self, name, lv):
		super(FileSystem, self).__init__()
		self.name = name
		self.lv = lv