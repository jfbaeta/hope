# -*- coding: UTF-8 -*-

class PhysicalVolume(object):
	"""class PhysicalVolume"""
	def __init__(self, name, devmap, uuid, vendor, product, size_n, size_m):
		super(PhysicalVolume, self).__init__()
		self.name = name
		self.devmap = devmap
		self.uuid = uuid
		self.vendor = vendor
		self.product = product
		self.size_n = size_n
		self.size_m = size_m

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