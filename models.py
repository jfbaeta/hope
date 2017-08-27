# -*- coding: UTF-8 -*-

class PhysicalVolume(object):
	"""class PhysicalVolume"""
	def __init__(self, name, sysfs, uuid, wwid, size):
		super(PhysicalVolume, self).__init__()
		self.name = name
		self.sysfs = sysfs
		self.uuid = uuid
		self.wwid = wwid
		self.size = size

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