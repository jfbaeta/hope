# -*- coding: UTF-8 -*-

class PhysicalVolume(object):
	"""class PhysicalVolume"""
	def __init__(self, name, devmap, wwid, vendor, product, size_n, size_m):
		super(PhysicalVolume, self).__init__()
		self.__name = name
		self.__devmap = devmap
		self.__wwid = wwid
		self.__vendor = vendor
		self.__product = product
		self.__size_n = size_n
		self.__size_m = size_m

	def get_name(self):
		return self.__name

	def get_devmap(self):
		return self.__devmap

	def get_wwid(self):
		return self.__wwid

	def get_vendor(self):
		return self.__vendor

	def get_product(self):
		return self.__product

	def get_size_n(self):
		return self.__size_n

	def get_size_m(self):
		return self.__size_m

	def get_all(self):
		return self.__name, self.__devmap, self.__wwid, self.__vendor, self.__product, self.__vendor, self.__size_n, self.__size_m

	def change_name(self, name):
		self.__name = name

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