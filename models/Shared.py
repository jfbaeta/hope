# -*- coding: UTF-8 -*-

class Shared(object):
	'''
	Class used for /hana/shared attributes.
	Attributes and methods are passed to other LVM Classes.
	'''
	name                    = 'shared'

	vg_physical_extent_size = '-s 1M'
	vg_data_alignment       = '--dataalignment 1M'
	vg_args                 = vg_physical_extent_size + ' ' + vg_data_alignment
	
	lv_size                 = '-l 100%VG'
	lv_args                 = lv_size
	
	fs_block_size           = '-b size=4096'
	fs_sector_size          = '-s size=4096'
	fs_type                 = 'xfs'
	fs_mount_point          = '/hana/shared'
	fs_args                 = fs_block_size + ' ' + fs_sector_size
	
	def __init__(self):
		super(Shared, self).__init__()