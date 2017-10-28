# -*- coding: UTF-8 -*-

class Storage(object):

	"""class Storage"""
	def __init__(self):
		super(Storage, self).__init__()
		self.__luns = []
	
	def add(self, lun):
		self.__luns.append(lun)

	def get(self):
		return self.__luns

class PhysicalVolume(object):
	
	"""class PhysicalVolume"""
	
	def __init__(self, name):
		super(PhysicalVolume, self).__init__()
		self.__name = name

	def mkpv():
		pass

class VolumeGroup(object):
	
	"""class VolumeGroup"""
	
	def __init__(self, name, pvs):
		super(VolumeGroup, self).__init__()
		self.name = name
		self.pvs = pvs

	def mkvg():
		pass

class LogicalVolume(object):
	
	"""class LogicalVolume"""
	
	def __init__(self, index='', lvpath='', vgname='', lvname=''):
		super(LogicalVolume, self).__init__()
		self.__index  = index
		self.__lvpath = lvpath
		self.__vgname = vgname
		self.__lvname = lvname

	def get_index(self):
		return self.__index

	def get_lvpath(self):
		return self.__lvpath

	def get_vgname(self):
		return self.__vgname

	def get_lvname(self):
		return self.__lvname

	def mklv():
		pass

class FileSystem(object):
	
	"""class FileSystem"""
	
	def __init__(self, name, lv):
		super(FileSystem, self).__init__()
		self.name = name
		self.lv = lv

	def mkfs():
		pass

	def mkdir():
		pass

	def mount():
		pass

	def show():
		pass

	def fstab():
		pass

class Root(object):
	
	"""class Root"""
	
	def __init__(self, name):
		super(Root, self).__init__()

class UsrSap(object):
	
	"""class UsrSap"""
	
	fs_type = 'ext3'
	fs_mount_point = '/usr/sap'
	
	def __init__(self, name):
		super(UsrSap, self).__init__()

class Data(object):
	
	"""class Data"""
	
	vg_physical_extent_size = '1M'
	vg_data_alignment = '1M'
	lv_stripes = '4'
	lv_stripe_size = '4'
	fs_block_size = '4096'
	fs_sector_size = '4096'
	fs_type = 'xfs'
	fs_mount_point = '/hana/data'
	
	def __init__(self, name):
		super(Data, self).__init__()

class Log(object):
	
	"""class Log"""
	
	vg_physical_extent_size = '1M'
	vg_data_alignment = '1M'
	lv_stripes = '4'
	lv_stripe_size = '4'
	fs_block_size = '4096'
	fs_sector_size = '4096'
	fs_type = 'xfs'
	fs_mount_point = '/hana/log'
	
	def __init__(self, name):
		super(Log, self).__init__()

class Shared(object):
	
	"""class Shared"""
	
	vg_physical_extent_size = '1M'
	vg_data_alignment = '1M'
	lv_stripes = '4'
	lv_stripe_size = '4'
	fs_block_size = '4096'
	fs_sector_size = '4096'
	fs_type = 'xfs'
	fs_mount_point = '/hana/shared'
	
	def __init__(self, name):
		super(Shared, self).__init__()