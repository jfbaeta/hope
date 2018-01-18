# -*- coding: UTF-8 -*-

class Data(object):
	
	"""class Data"""

	name                    = '/hana/data'

	vg_physical_extent_size = '-s 1M'
	vg_data_alignment       = '--dataalignment 1M'
	vg_args                 = vg_physical_extent_size + ' ' + vg_data_alignment
	
	lv_stripes              = '-i 4'
	lv_stripe_size          = '-I 256'
	lv_size                 = '-l 100%VG'
	lv_args                 = lv_stripes + ' ' + lv_stripe_size + ' ' + lv_size
	
	fs_block_size           = '-b size=4096'
	fs_sector_size          = '-s size=4096'
	fs_type                 = 'xfs'
	fs_mount_point          = '/hana/data'
	fs_args                 = fs_block_size + ' ' + fs_sector_size
	
	def __init__(self):
		super(Data, self).__init__()