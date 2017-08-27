# -*- coding: UTF-8 -*-

class PhysicalVolume(object):
	"""class PhysicalVolume"""
	def __init__(self, arg):
		super(PhysicalVolume, self).__init__()
		self.arg = arg

class VolumeGroup(object):
	"""class VolumeGroup"""
	def __init__(self, arg):
		super(VolumeGroup, self).__init__()
		self.arg = arg

class LogicalVolume(object):
	"""class LogicalVolume"""
	def __init__(self, arg):
		super(LogicalVolume, self).__init__()
		self.arg = arg

class FileSystem(object):
	"""class FileSystem"""
	def __init__(self, arg):
		super(FileSystem, self).__init__()
		self.arg = arg