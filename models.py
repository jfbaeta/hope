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

class Formatter(object):
	
	"""class Formatter"""
	
	def __init__(self):
		super(Formatter, self).__init__()

	def show(self, resource):

		first_resource         = resource.get()[0]
		resources              = resource.get()
		first_resource_headers = first_resource.list_headers
		number_of_fields       = len(first_resource_headers)

		list_of_lists = []
		for j in resources:
			list_of_lists.append(j.lengths)

		list_of_lists_2 = zip(*list_of_lists)

		max_lengths = []

		for i in list_of_lists_2:
			max_lengths.append(max(i))

		total_len = sum(max_lengths)

		left_corner     = '+-'
		right_corner    = '-+'
		left_column     = "| "
		right_column    = "|"
		horizontal_line = left_corner + '-' * (total_len + ((number_of_fields * 2) + 4)) + right_corner
		normal_string   = '%s'
		bold_string     = '\033[1m%s\033[0m'

		print horizontal_line
		loop_item_count = 0
		for i in first_resource_headers:
			print left_column + (bold_string) % (i.ljust(max_lengths[loop_item_count])),
			loop_item_count+=1
		print right_column
		print horizontal_line
		for i in resources:
			loop_item_count = 0
			for j in i.all:
				print left_column + (normal_string) % (j.ljust(max_lengths[loop_item_count])),
				loop_item_count+=1
			print right_column
		print horizontal_line
