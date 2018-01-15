# -*- coding: UTF-8 -*-

class Shared(object):
	
	"""class Shared"""
	
	vg_physical_extent_size = '1M'
	vg_data_alignment       = '1M'
	lv_stripes              = '4'
	lv_stripe_size          = '4'
	fs_block_size           = '4096'
	fs_sector_size          = '4096'
	fs_type                 = 'xfs'
	fs_mount_point          = '/hana/shared'
	
	def __init__(self):
		super(Shared, self).__init__()