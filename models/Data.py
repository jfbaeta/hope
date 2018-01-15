# -*- coding: UTF-8 -*-

class Data(object):
	
	"""class Data"""
	
	vg_physical_extent_size = '1M'
	vg_data_alignment       = '1M'
	lv_stripes              = '4'
	lv_stripe_size          = '4'
	fs_block_size           = '4096'
	fs_sector_size          = '4096'
	fs_type                 = 'xfs'
	fs_mount_point          = '/hana/data'
	
	def __init__(self):
		super(Data, self).__init__()